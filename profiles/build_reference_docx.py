#!/usr/bin/env python3
"""Build profiles/<name>/reference.docx from pandoc's default reference document.

The reference document carries styles, page geometry, header and footer; pandoc ignores its body.
Inputs are pandoc's default reference.docx and the PROFILES table below, so the output is reproducible.
Change a profile here, rebuild, re-measure its calibration, and record the new line in its profile.md.

Usage: python3 profiles/build_reference_docx.py [plain]
"""
import os
import re
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))

PROFILES = {
    # Plain: A4, one-inch margins, Calibri 12 pt body, 16/13 pt headings, page number footer.
    "plain": {
        "page": (11906, 16838),
        "margins": {"top": 1440, "right": 1440, "bottom": 1440, "left": 1440, "header": 720, "footer": 720},
        "font": "Calibri", "color": "1A1A1A", "size": 24, "lang": "en-US", "justify": False,
        "line": 264, "body_after": 120, "list_before": 0, "list_after": 60,
        "title": {"size": 36, "color": "1A1A1A", "bold": True, "after": 60},
        "subtitle": {"size": 26, "color": "555555", "italic": True, "after": 240},
        "h1": {"size": 32, "color": "1A1A1A", "bold": True, "before": 240, "after": 80},
        "h2": {"size": 26, "color": "1A1A1A", "bold": True, "before": 160, "after": 60},
        "h3": {"size": 24, "color": "1A1A1A", "bold": True, "italic": True, "before": 120, "after": 40},
        "table": {"rule": "808080", "inner": "D0D0D0", "head_fill": None, "head_color": None},
        "link": "1F4E79",
        "header": None,
        "footer": {"align": "center", "runs": [("field", "PAGE")], "size": 18, "color": "777777", "border": None},
    },
}

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" ' \
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'


def rpr(font=None, size=None, color=None, bold=False, italic=False, lang=None):
    x = ""
    if font:
        x += f'<w:rFonts w:ascii="{font}" w:eastAsia="{font}" w:hAnsi="{font}" w:cs="{font}"/>'
    if bold:
        x += "<w:b/><w:bCs/>"
    if italic:
        x += "<w:i/><w:iCs/>"
    if color:
        x += f'<w:color w:val="{color}"/>'
    if size:
        x += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    if lang:
        x += f'<w:lang w:val="{lang}" w:eastAsia="en-US" w:bidi="ar-SA"/>'
    return f"<w:rPr>{x}</w:rPr>"


def pstyle(sid, name, based, nxt, ppr, rp, extra=""):
    b = f'<w:basedOn w:val="{based}"/>' if based else ""
    n = f'<w:next w:val="{nxt}"/>' if nxt else ""
    return (f'<w:style w:type="paragraph" w:styleId="{sid}"{" w:default=\"1\"" if sid == "Normal" else ""}>'
            f'<w:name w:val="{name}"/>{b}{n}{extra}<w:qFormat/><w:pPr>{ppr}</w:pPr>{rp}</w:style>')


def spacing(before=0, after=0, line=None):
    ln = f' w:line="{line}" w:lineRule="auto"' if line else ""
    return f'<w:spacing w:before="{before}" w:after="{after}"{ln}/>'


def heading(p, key, sid, name, level):
    h = p[key]
    ppr = "<w:keepNext/><w:keepLines/>" + spacing(h["before"], h["after"], h.get("line")) + \
          f'<w:jc w:val="left"/><w:outlineLvl w:val="{level}"/>'
    return pstyle(sid, name, "Normal", "BodyText", ppr,
                  rpr(p["font"], h["size"], h["color"], h.get("bold"), h.get("italic")),
                  f'<w:uiPriority w:val="9"/>')


def styles_for(p):
    jc = '<w:jc w:val="both"/>' if p["justify"] else '<w:jc w:val="left"/>'
    t = p["table"]
    head_tc = ""
    if t["head_fill"]:
        head_tc = f'<w:shd w:val="clear" w:color="auto" w:fill="{t["head_fill"]}"/>'
    head_rpr = rpr(bold=True, color=t["head_color"])
    return {
        "Normal": pstyle("Normal", "Normal", None, None, spacing(0, 0, p["line"]) + '<w:jc w:val="left"/>', rpr()),
        # keepLines on body and list paragraphs: no paragraph splits across pages (E-3, V0.2.1).
        "BodyText": pstyle("BodyText", "Body Text", "Normal", None, "<w:keepLines/>" + spacing(0, p["body_after"]) + jc, rpr(),
                           '<w:link w:val="BodyTextChar"/>'),
        "FirstParagraph": pstyle("FirstParagraph", "First Paragraph", "BodyText", "BodyText", "", rpr()),
        "Compact": pstyle("Compact", "Compact", "BodyText", None,
                          "<w:keepLines/>" + spacing(p["list_before"], p["list_after"]) + '<w:jc w:val="left"/>', rpr()),
        "Title": pstyle("Title", "Title", "Normal", "BodyText",
                        spacing(0, p["title"]["after"], 240) + '<w:jc w:val="left"/>',
                        rpr(p["font"], p["title"]["size"], p["title"]["color"], p["title"].get("bold")),
                        '<w:link w:val="TitleChar"/><w:uiPriority w:val="10"/>'),
        "Subtitle": pstyle("Subtitle", "Subtitle", "Title", "BodyText",
                           spacing(0, p["subtitle"]["after"], 259) + '<w:jc w:val="left"/>',
                           rpr(p["font"], p["subtitle"]["size"], p["subtitle"]["color"], False,
                               p["subtitle"].get("italic")),
                           '<w:link w:val="SubtitleChar"/><w:uiPriority w:val="11"/>'),
        "Heading1": heading(p, "h1", "Heading1", "heading 1", 0),
        "Heading2": heading(p, "h2", "Heading2", "heading 2", 1),
        "Heading3": heading(p, "h3", "Heading3", "heading 3", 2),
        "Hyperlink": (f'<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/>'
                      f'<w:basedOn w:val="BodyTextChar"/>{rpr(color=p["link"])}</w:style>'),
        "Table": (
            '<w:style w:type="table" w:default="1" w:styleId="Table"><w:name w:val="Table"/>'
            '<w:basedOn w:val="TableNormal"/><w:uiPriority w:val="59"/><w:qFormat/>'
            # keepNext on every cell paragraph keeps small tables on one page (Word still splits a table
            # taller than a page); rendered-page QA checks the rest.
            f'<w:pPr><w:keepNext/>{spacing(0, 0, 240)}<w:jc w:val="left"/></w:pPr>'
            '<w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblBorders>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{t["rule"]}"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{t["rule"]}"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{t["inner"]}"/>'
            '</w:tblBorders><w:tblCellMar><w:top w:w="50" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
            '<w:bottom w:w="50" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr>'
            f'<w:tblStylePr w:type="firstRow">{head_rpr}<w:tcPr><w:tcBorders>'
            f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="{t["rule"]}"/></w:tcBorders>'
            f'{head_tc}<w:vAlign w:val="bottom"/></w:tcPr></w:tblStylePr></w:style>'),
    }


def replace_style(xml, sid, new):
    pat = re.compile(r'<w:style [^>]*w:styleId="%s"[^>]*>.*?</w:style>' % sid, re.S)
    if pat.search(xml):
        return pat.sub(lambda _: new, xml, count=1)
    return xml.replace("</w:styles>", new + "</w:styles>")


def build_styles(xml, p):
    dd = ('<w:docDefaults><w:rPrDefault>'
          + rpr(p["font"], p["size"], p["color"], lang=p["lang"])
          + '</w:rPrDefault><w:pPrDefault><w:pPr>' + spacing(0, 0) + '</w:pPr></w:pPrDefault></w:docDefaults>')
    xml = re.sub(r"<w:docDefaults>.*?</w:docDefaults>", lambda _: dd, xml, count=1, flags=re.S)
    for sid, new in styles_for(p).items():
        xml = replace_style(xml, sid, new)
    return xml


def hf_part(tag, spec):
    align = spec["align"]
    runs = ""
    base = {"size": spec["size"], "color": spec["color"]}
    for r in spec["runs"]:
        if r[0] == "text":
            o = {**base, **(r[2] if len(r) > 2 else {})}
            runs += f'<w:r>{rpr(size=o["size"], color=o["color"], bold=o.get("bold"))}' \
                    f'<w:t xml:space="preserve">{r[1]}</w:t></w:r>'
        else:
            fr = rpr(size=base["size"], color=base["color"])  # complex field: every run carries the size
            runs += (f'<w:r>{fr}<w:fldChar w:fldCharType="begin"/></w:r>'
                     f'<w:r>{fr}<w:instrText xml:space="preserve"> {r[1]} </w:instrText></w:r>'
                     f'<w:r>{fr}<w:fldChar w:fldCharType="separate"/></w:r><w:r>{fr}<w:t>1</w:t></w:r>'
                     f'<w:r>{fr}<w:fldChar w:fldCharType="end"/></w:r>')
    border = ""
    if spec.get("border"):
        border = f'<w:pBdr><w:bottom w:val="single" w:sz="4" w:space="6" w:color="{spec["border"]}"/></w:pBdr>'
    ppr = f'<w:pPr>{border}{spacing(0, 0)}<w:jc w:val="{align}"/>{rpr(size=base["size"], color=base["color"])}</w:pPr>'
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:{tag} {W}><w:p>{ppr}{runs}</w:p></w:{tag}>'


def build(name):
    p = PROFILES[name]
    base = subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                          capture_output=True, check=True).stdout
    src = zipfile.ZipFile(__import__("io").BytesIO(base))
    files = {n: src.read(n) for n in src.namelist()}

    files["word/styles.xml"] = build_styles(files["word/styles.xml"].decode("utf-8"), p).encode("utf-8")

    rels = files["word/_rels/document.xml.rels"].decode("utf-8")
    ctypes = files["[Content_Types].xml"].decode("utf-8")
    refs = ""
    for tag, part, rid, ctype in (("hdr", "header", "rIdGdawHeader", "header"),
                                  ("ftr", "footer", "rIdGdawFooter", "footer")):
        spec = p[part]
        if not spec:
            continue
        files[f"word/{part}1.xml"] = hf_part(tag, spec).encode("utf-8")
        rels = rels.replace("</Relationships>",
                            f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                            f'relationships/{part}" Target="{part}1.xml"/></Relationships>')
        ctypes = ctypes.replace("</Types>",
                                f'<Override PartName="/word/{part}1.xml" ContentType="application/'
                                f'vnd.openxmlformats-officedocument.wordprocessingml.{ctype}+xml"/></Types>')
        refs += f'<w:{part}Reference w:type="default" r:id="{rid}"/>'
    files["word/_rels/document.xml.rels"] = rels.encode("utf-8")
    files["[Content_Types].xml"] = ctypes.encode("utf-8")

    m = p["margins"]
    sect = (f'<w:sectPr>{refs}<w:pgSz w:w="{p["page"][0]}" w:h="{p["page"][1]}"/>'
            f'<w:pgMar w:top="{m["top"]}" w:right="{m["right"]}" w:bottom="{m["bottom"]}" w:left="{m["left"]}" '
            f'w:header="{m["header"]}" w:footer="{m["footer"]}" w:gutter="0"/>'
            f'<w:footnotePr><w:numRestart w:val="eachSect"/></w:footnotePr></w:sectPr>')
    doc = files["word/document.xml"].decode("utf-8")
    doc = re.sub(r"<w:sectPr>.*?</w:sectPr>", lambda _: sect, doc, count=1, flags=re.S)
    if 'xmlns:r=' not in doc.split(">", 2)[1]:
        doc = doc.replace("<w:document ", '<w:document xmlns:r="http://schemas.openxmlformats.org/'
                                         'officeDocument/2006/relationships" ', 1)
    files["word/document.xml"] = doc.encode("utf-8")

    out = os.path.join(HERE, name, "reference.docx")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in src.namelist() + [f for f in files if f not in src.namelist()]:
            info = zipfile.ZipInfo(n, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, files[n])
    print("written", os.path.relpath(out))


if __name__ == "__main__":
    for n in sys.argv[1:] or PROFILES:
        build(n)
