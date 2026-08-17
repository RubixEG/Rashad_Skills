from __future__ import annotations
from pathlib import Path
import re,subprocess
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

AR=re.compile(r'[\u0600-\u06ff]')
LAT_TOKEN=re.compile(r'[A-Za-z][A-Za-z0-9._/-]*')

def _font_file():
    try:
        p=subprocess.check_output(['fc-match','-f','%{file}','DejaVu Sans'],text=True,timeout=5).strip()
        if p and Path(p).exists(): return p
    except Exception: pass
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf']:
        if Path(p).exists(): return p
    return None

def logical_text_lines(content_pack,semantic_graph=None):
    vals=[]
    for k in ('eyebrow','title','management_question','thesis','answer_first_thesis','answer','executive_implication','footer','source_note'):
        v=content_pack.get(k)
        if v: vals.append(str(v))
    for k in ('proof_points','evidence_points','bullets'):
        for x in content_pack.get(k) or []:
            vals.append(str(x.get('text') if isinstance(x,dict) else x))
    for n in (semantic_graph or {}).get('nodes',[]) or []:
        if isinstance(n,dict) and (n.get('label') or n.get('name')): vals.append(str(n.get('label') or n.get('name')))
    out=[]
    for x in vals:
        x=re.sub(r'\s+',' ',x).strip()
        if x and x not in out: out.append(x)
    return out

def build_searchable_image_pdf(image_path,out_path,logical_lines,width=1920,height=1080):
    """Pixel-authoritative PDF + invisible logical text layer.

    Arabic prose is inserted in reverse display order because PDF extractors apply
    bidi on the text object. The resulting ToUnicode extraction is logical Arabic
    (including lam-alef). Latin technical tokens are also inserted separately so
    Ctrl+F/indexers can find them without relying on mixed-run bidi behavior.
    """
    ff=_font_file()
    if not ff: return {'status':'BLOCKED','reason':'PDF_TEXT_LAYER_FONT_NOT_AVAILABLE'}
    name='RashadSearchLayer'
    try: pdfmetrics.registerFont(TTFont(name,ff))
    except Exception: pass
    out=Path(out_path); out.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(out),pagesize=(width,height),pageCompression=1)
    c.drawImage(str(image_path),0,0,width=width,height=height,preserveAspectRatio=True,anchor='c')
    t=c.beginText(32,height-32); t.setFont(name,7); t.setTextRenderMode(3); t.setLeading(9)
    token_lines=[]
    for logical in logical_lines:
        logical=str(logical).strip()
        if not logical: continue
        for tok in LAT_TOKEN.findall(logical): token_lines.append(tok)
        # Strip Latin technical islands from the Arabic logical line. Arabic-Indic digits remain safe.
        arline=LAT_TOKEN.sub(' ',logical); arline=re.sub(r'\s+',' ',arline).strip()
        if AR.search(arline): t.textLine(arline[::-1])
        elif arline: t.textLine(arline)
    for tok in token_lines: t.textLine(tok)
    c.drawText(t); c.save()
    return {'status':'PASS','pdf_path':str(out),'text_layer_font':ff,'logical_line_count':len(logical_lines),'technical_token_count':len(token_lines),'rule':'Visible pixels are authoritative; invisible text layer is logical Unicode for search/copy/indexing.'}
