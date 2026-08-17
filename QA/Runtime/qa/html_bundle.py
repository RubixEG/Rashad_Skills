from pathlib import Path
from bs4 import BeautifulSoup
import base64, mimetypes, re

def _data(path:Path):
    mime=mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode()

def inline_html(path:Path)->str:
    path=Path(path).resolve(); html=path.read_text(encoding='utf-8')
    soup=BeautifulSoup(html,'html.parser')
    for img in soup.find_all('img'):
        src=img.get('src','')
        if src and not re.match(r'^(data:|https?:|blob:)',src):
            p=(path.parent/src).resolve()
            if p.exists() and p.is_file(): img['src']=_data(p)
    # inline local stylesheets
    for link in list(soup.find_all('link')):
        if (link.get('rel') and 'stylesheet' in link.get('rel')):
            href=link.get('href','')
            if href and not re.match(r'^(data:|https?:)',href):
                p=(path.parent/href).resolve()
                if p.exists():
                    st=soup.new_tag('style'); st.string=p.read_text(encoding='utf-8'); link.replace_with(st)
    return str(soup)
