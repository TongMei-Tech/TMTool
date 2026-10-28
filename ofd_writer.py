# -*- coding: utf-8 -*-
"""
双层 OFD 生成器（严格遵循 GB/T 33190-2016）。

将 PDF 转换为双层 OFD：
  - 图像层：每页渲染为 JPEG 底图（ImageObject + CTM），保留视觉外观；
  - 文本层：从 PDF 提取文本，逐字生成 TextObject，含 CGTransform 字形映射、
    嵌入字体子集（fontTools 子集化）、DeltaX 字间距，实现可检索/可选中/可复制。

XML 层级严格对齐规范样本：Page > Area(PhysicalBox) + Content > Layer > Objects。
命名空间 http://www.ofdspec.org/2016。依赖 PyMuPDF(fitz)、Pillow、fontTools，无页数限制。
"""

import io
import os
import zipfile
from xml.sax.saxutils import escape

OFD_NS = 'http://www.ofdspec.org/2016'
PT_TO_MM = 0.3528  # PDF点(pt)转毫米(mm)


def make_layered_ofd(pdf_path, ofd_path, dpi=150, jpeg_quality=80):
    """将双层 PDF 转换为双层 OFD。返回 (成功?, 页数, 错误信息)。"""
    try:
        try:
            import pymupdf as fitz  # PyMuPDF >=1.24 (fitz别名已弃用)
        except ImportError:
            import fitz  # 旧版 PyMuPDF
        from PIL import Image
        from fontTools.ttLib import TTFont
    except ImportError as e:
        return False, 0, '缺少依赖 PyMuPDF/Pillow/fontTools: %s' % e

    try:
        if not os.path.exists(pdf_path):
            return False, 0, 'PDF 文件不存在: %s' % pdf_path

        doc = fitz.open(pdf_path)
        if doc.page_count == 0:
            doc.close()
            return False, 0, 'PDF 无页面'

        scale = dpi / 72.0
        pages = []  # [(img_bytes, w_mm, h_mm, [(x0,y0,x1,y1,text,size_mm), ...])]
        all_chars = set()  # 全文用到的字符（用于字体子集化）
        for page in doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
            img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
            ib = io.BytesIO()
            img.save(ib, 'JPEG', quality=jpeg_quality)
            ib = ib.getvalue()

            wm = round(page.rect.width * PT_TO_MM, 3)
            hm = round(page.rect.height * PT_TO_MM, 3)

            spans = []
            for block in page.get_text('dict').get('blocks', []):
                if 'lines' not in block:
                    continue
                for line in block['lines']:
                    for span in line.get('spans', []):
                        t = span['text']
                        if not t.strip():
                            continue
                        x0 = round(span['bbox'][0] * PT_TO_MM, 3)
                        y0 = round(span['bbox'][1] * PT_TO_MM, 3)
                        x1 = round(span['bbox'][2] * PT_TO_MM, 3)
                        y1 = round(span['bbox'][3] * PT_TO_MM, 3)
                        sz = round(span['size'] * PT_TO_MM, 3)
                        spans.append((x0, y0, x1, y1, t, sz))
                        all_chars.update(t)
            pages.append((ib, wm, hm, spans))
        doc.close()

        _write_ofd(ofd_path, pages, all_chars)
        return True, len(pages), ''
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, 0, str(e)


def _fmt(v):
    s = ('%f' % v).rstrip('0').rstrip('.')
    return s if s else '0'


def _build_font_subset(chars, out_ttf_path):
    """
    用系统 SimSun 字体生成包含指定字符的子集字体。
    返回 (子集字体, {字符: 子集内字形数字索引})。
    """
    from fontTools.ttLib import TTFont
    from fontTools.subset import Subsetter, Options

    src = 'C:/Windows/Fonts/simsun.ttc'
    if not os.path.exists(src):
        src = 'C:/Windows/Fonts/msyh.ttc'
    sub = TTFont(src, fontNumber=0)
    subsetter = Subsetter()
    subsetter.populate(unicodes=[ord(c) for c in chars if ord(c) > 31])
    subsetter.subset(sub)
    opt = Options()
    opt.flavor = 'ttf'
    sub.save(out_ttf_path)

    # 子集内字形索引映射
    sub2 = TTFont(out_ttf_path)
    glyph_order = sub2.getGlyphOrder()
    cmap = sub2.getBestCmap()
    char_to_gid = {}
    for ch in chars:
        if ord(ch) <= 31:
            continue
        gname = cmap.get(ord(ch))
        if gname and gname in glyph_order:
            char_to_gid[ch] = glyph_order.index(gname)
    return char_to_gid


def _write_ofd(ofd_path, pages, all_chars):
    """组装 OFD (zip)。"""
    import hashlib
    from datetime import datetime

    # 1. 生成字体子集 + 字形索引映射
    # FontFile 路径相对于 PublicRes 的 BaseLoc="Res"，故只写文件名
    font_file_name = 'font_0.ttf'
    font_path_in_zip = 'Res/' + font_file_name
    tmp_ttf = os.path.join(os.path.dirname(ofd_path) or '.',
                           '_tmp_subset_%d.ttf' % os.getpid())
    try:
        char_to_gid = _build_font_subset(all_chars, tmp_ttf)
        with open(tmp_ttf, 'rb') as f:
            font_bytes = f.read()
    finally:
        if os.path.exists(tmp_ttf):
            os.remove(tmp_ttf)

    # ID 分配
    _uid = [0]
    def nid():
        _uid[0] += 1
        return _uid[0]

    n_pages = len(pages)
    color_id = nid()
    font_id = nid()       # 字体资源 ID
    mm_ids = [nid() for _ in range(n_pages)]
    page_ids = [nid() for _ in range(n_pages)]
    content_ids = [nid() for _ in range(n_pages)]
    layer_ids = [nid() for _ in range(n_pages)]
    img_obj_ids = [nid() for _ in range(n_pages)]
    total_spans = sum(len(s) for _, _, _, s in pages)
    max_unit_id = _uid[0] + total_spans

    doc_id = hashlib.md5((os.path.abspath(ofd_path) + str(max_unit_id)).encode('utf-8')).hexdigest().lower()
    today = datetime.now().strftime('%Y-%m-%d')

    with zipfile.ZipFile(ofd_path, 'w', zipfile.ZIP_DEFLATED) as z:
        # OFD.xml
        z.writestr('OFD.xml',
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<ofd:OFD xmlns:ofd="%s" Version="1.0" DocType="OFD">\n'
            '  <ofd:DocBody>\n'
            '    <ofd:DocInfo>\n'
            '      <ofd:DocID>%s</ofd:DocID>\n'
            '      <ofd:Creator>TMAI</ofd:Creator>\n'
            '      <ofd:CreationDate>%s</ofd:CreationDate>\n'
            '    </ofd:DocInfo>\n'
            '    <ofd:DocRoot>Doc_0/Document.xml</ofd:DocRoot>\n'
            '  </ofd:DocBody>\n'
            '</ofd:OFD>\n' % (OFD_NS, doc_id, today))

        # Document.xml
        wm0, hm0 = pages[0][1], pages[0][2]
        page_xml = ''.join(
            '    <ofd:Page ID="%d" BaseLoc="Pages/Page_%d/Content.xml" />\n' % (page_ids[i], i)
            for i in range(n_pages))
        z.writestr('Doc_0/Document.xml',
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<ofd:Document xmlns:ofd="%s">\n'
            '  <ofd:Pages>\n%s  </ofd:Pages>\n'
            '  <ofd:CommonData>\n'
            '    <ofd:MaxUnitID>%d</ofd:MaxUnitID>\n'
            '    <ofd:PageArea><ofd:PhysicalBox>0 0 %s %s</ofd:PhysicalBox></ofd:PageArea>\n'
            '    <ofd:PublicRes>PublicRes.xml</ofd:PublicRes>\n'
            '    <ofd:DocumentRes>DocumentRes.xml</ofd:DocumentRes>\n'
            '  </ofd:CommonData>\n'
            '</ofd:Document>\n' % (OFD_NS, page_xml, max_unit_id, _fmt(wm0), _fmt(hm0)))

        # DocumentRes.xml (图像资源)
        mms = ''.join(
            '  <ofd:MultiMedias>\n'
            '    <ofd:MultiMedia Type="image" ID="%d" Format="jpg">\n'
            '      <ofd:MediaFile>Image_%d.jpg</ofd:MediaFile>\n'
            '    </ofd:MultiMedia>\n'
            '  </ofd:MultiMedias>\n' % (mm_ids[i], i)
            for i in range(n_pages))
        z.writestr('Doc_0/DocumentRes.xml',
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<ofd:Res BaseLoc="Res" xmlns:ofd="%s">\n%s</ofd:Res>\n' % (OFD_NS, mms))

        # PublicRes.xml (颜色空间 + 嵌入字体)
        z.writestr('Doc_0/PublicRes.xml',
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<ofd:Res BaseLoc="Res" xmlns:ofd="%s">\n'
            '  <ofd:ColorSpaces>\n'
            '    <ofd:ColorSpace Type="RGB" BitsPerComponent="8" ID="%d"/>\n'
            '  </ofd:ColorSpaces>\n'
            '  <ofd:Fonts>\n'
            '    <ofd:Font FontName="SimSun" FamilyName="SimSun" ID="%d">\n'
            '      <ofd:FontFile>%s</ofd:FontFile>\n'
            '    </ofd:Font>\n'
            '  </ofd:Fonts>\n'
            '</ofd:Res>\n' % (OFD_NS, color_id, font_id, font_file_name))
        z.writestr('Doc_0/' + font_path_in_zip, font_bytes)

        # 每页 Content.xml + 图像
        for i, (ib, wm, hm, spans) in enumerate(pages):
            img_id = img_obj_ids[i]
            img_obj = ('      <ofd:ImageObject ID="%d" Boundary="0 0 %s %s" '
                       'CTM="%s 0 0 %s 0 0" ResourceID="%d"/>\n'
                       % (img_id, _fmt(wm), _fmt(hm), _fmt(wm), _fmt(hm), mm_ids[i]))
            txt_xml = []
            for (x0, y0, x1, y1, t, sz) in spans:
                w = max(round(x1 - x0, 3), round(sz * len(t) * 0.5, 3))
                h = max(round(y1 - y0, 3), round(sz, 3))
                baseline_y = round(sz * 0.8, 3)
                tid = nid()
                n_chars = len(t)
                # CGTransform: 字形索引序列（子集字体内的 glyph index）
                glyphs = [str(char_to_gid.get(c, 0)) for c in t]
                cgtrans = ('<ofd:CGTransform GlyphCount="%d" CodeCount="%d" CodePosition="0">'
                           '<ofd:Glyphs>%s</ofd:Glyphs></ofd:CGTransform>'
                           % (n_chars, n_chars, ' '.join(glyphs)))
                # DeltaX: N字 N-1个间距
                if n_chars > 1:
                    char_dx = round(w / n_chars, 3) if w > 0 else round(sz, 3)
                    deltax = ' '.join([_fmt(char_dx)] * (n_chars - 1))
                    textcode = '<ofd:TextCode X="0" Y="%s" DeltaX="%s">%s</ofd:TextCode>' \
                               % (_fmt(baseline_y), deltax, escape(t))
                else:
                    textcode = '<ofd:TextCode X="0" Y="%s">%s</ofd:TextCode>' \
                               % (_fmt(baseline_y), escape(t))
                txt_xml.append(
                    '      <ofd:TextObject ID="%d" Boundary="%s %s %s %s" Size="%s" '
                    'CTM="1 0 0 1 0 0" Fill="true" Font="%d">\n'
                    '        <ofd:FillColor Value="0 0 0" Alpha="0"/>\n'
                    '        %s\n'
                    '        %s\n'
                    '      </ofd:TextObject>\n'
                    % (tid, _fmt(x0), _fmt(y0), _fmt(w), _fmt(h),
                       _fmt(sz), font_id, cgtrans, textcode))
            z.writestr('Doc_0/Pages/Page_%d/Content.xml' % i,
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                '<ofd:Page xmlns:ofd="%s">\n'
                '  <ofd:Area><ofd:PhysicalBox>0 0 %s %s</ofd:PhysicalBox></ofd:Area>\n'
                '  <ofd:Content ID="%d">\n'
                '    <ofd:Layer ID="%d">\n'
                '%s%s'
                '    </ofd:Layer>\n'
                '  </ofd:Content>\n'
                '</ofd:Page>\n' % (OFD_NS, _fmt(wm), _fmt(hm), content_ids[i], layer_ids[i],
                                   img_obj, ''.join(txt_xml)))
            z.writestr('Doc_0/Res/Image_%d.jpg' % i, ib)
