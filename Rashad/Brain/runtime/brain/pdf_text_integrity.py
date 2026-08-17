from __future__ import annotations
from pathlib import Path
import re, hashlib

def _norm(s):
    s=str(s or '').replace('\u0640','')
    s=re.sub(r'[\u064b-\u065f\u0670]','',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s

def inspect_pdf_text_layer(pdf_path,expected_samples=None):
    import fitz
    p=Path(pdf_path); blockers=[]; warnings=[]
    if not p.exists(): return {'status':'BLOCKED','blockers':['PDF_NOT_FOUND']}
    try: doc=fitz.open(p); pages=[page.get_text('text') for page in doc]
    except Exception as e: return {'status':'BLOCKED','blockers':['PDF_TEXT_EXTRACTION_FAILED'],'error':repr(e)}
    full=_norm('\n'.join(pages)); samples=[_norm(x) for x in (expected_samples or []) if _norm(x)]
    missing=[]; reversed_negation=[]
    for s in samples:
        if s not in full:
            missing.append(s[:160])
            if 'لا ' in s:
                alt=s.replace('لا ','ال ',1)
                if alt in full: reversed_negation.append({'expected':s[:160],'observed':alt[:160]})
    # Conservative heuristic only for common negation phrases. It is not a substitute for expected-text proof.
    suspect=re.findall(r'(?<![\u0600-\u06ff])ال\s+(?:تتحمل|يتحمل|يمكن|يجوز|يشمل|توجد|يوجد|يتم|تقبل|يقبل|تسمح|يسمح)\b',full)
    if reversed_negation: blockers.append('PDF_LAM_ALEF_NEGATION_REVERSAL_PROVEN')
    if suspect: warnings.append('PDF_SUSPICIOUS_REVERSED_NEGATION_SEQUENCE')
    if samples and missing: blockers.append('PDF_EXPECTED_TEXT_LAYER_SAMPLE_MISSING')
    if not samples: warnings.append('PDF_EXPECTED_TEXT_SAMPLES_NOT_SUPPLIED_HEURISTIC_ONLY')
    return {'status':'PASS' if not blockers else 'BLOCKED','pdf_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'page_count':len(pages),'expected_sample_count':len(samples),'missing_samples':missing[:30],'reversed_negation_matches':reversed_negation,'suspicious_sequences':suspect[:30],'blockers':blockers,'warnings':warnings}
