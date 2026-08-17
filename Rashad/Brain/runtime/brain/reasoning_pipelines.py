from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CFG=ROOT/'config/reasoning_pipelines.json'
def pipelines(): return json.loads(CFG.read_text(encoding='utf-8'))['pipelines']
def select_pipelines(task):
    t=json.dumps(task,ensure_ascii=False).lower(); out=[]
    if any(x in t for x in ['technical','architecture','api','integration','data',' ai','cyber','cloud','تقني','تكامل','ذكاء اصطناعي']): out.append('TECHNICAL_SOLUTION')
    if any(x in t for x in ['boq','price','margin','cost','payment','commercial','سعر','تكلفة','هامش','دفعات','تجاري']): out.append('FINANCIAL_COMMERCIAL')
    return {'selected':out,'steps':{k:pipelines()[k] for k in out}}
