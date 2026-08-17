from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qa_v4.arabic_executive_terminology import validate_visible_text

def run():
    cases=[
      ('visible_title_diacritic','التعرّض التجاري والمالي',None,'BLOCK'),
      ('visible_subsection','مصادر التعرّض',None,'BLOCK'),
      ('visible_callout','التعرّض المالي مرتفع',None,'BLOCK'),
      ('source_quote','ورد في المصدر: التعرّض المالي','SOURCE_QUOTATION','PASS'),
      ('approved_default','الالتزامات والمخاطر التجارية والمالية',None,'PASS'),
      ('approved_profit','الالتزامات المالية والتجارية وأثرها على الربحية',None,'PASS'),
      ('specific_impact','الأثر المالي والتجاري',None,'PASS'),
    ]
    out=[]
    for name,text,exc,expected in cases:
        got=validate_visible_text(text,exc)['status']; out.append((name,got,expected)); assert got==expected,(name,got,expected)
    assert 'COMMERCIAL_EXPOSURE'=='COMMERCIAL_EXPOSURE'
    return out

if __name__=='__main__':
    print(run())
