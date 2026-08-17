from __future__ import annotations
import re

_AR_DIACRITICS = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]")
PROHIBITED_NORMALIZED = ("التعرض",)
ALLOWED_VISIBLE_EXCEPTIONS = {"SOURCE_QUOTATION", "HISTORICAL_SOURCE", "OWNER_APPROVED_ENGAGEMENT_EXCEPTION"}

def normalize_ar(text: str) -> str:
    return _AR_DIACRITICS.sub("", text or "")

def contains_prohibited_visible_term(text: str) -> bool:
    n=normalize_ar(text)
    return any(term in n for term in PROHIBITED_NORMALIZED)

def validate_visible_text(text: str, exception: str|None=None) -> dict:
    exception=(exception or "").upper().strip()
    hit=contains_prohibited_visible_term(text)
    allowed=hit and exception in ALLOWED_VISIBLE_EXCEPTIONS
    return {
        "status":"PASS" if (not hit or allowed) else "BLOCK",
        "prohibited_hit":hit,
        "exception":exception or None,
        "normalized":normalize_ar(text),
        "reason":"explicit_visible_exception" if allowed else ("prohibited_arabic_executive_term" if hit else "clean")
    }

def validate_page_text_elements(elements: list[dict]) -> dict:
    violations=[]; checked=0; exempted=[]
    for e in elements:
        text=str(e.get("text") or "")
        if not text.strip(): continue
        checked += 1
        data=e.get("data") or {}
        exception=data.get("visibleLanguageException") or ("SOURCE_QUOTATION" if str(data.get("sourceQuotation") or "").lower() in {"1","true","yes"} else None)
        r=validate_visible_text(text,exception)
        if r["prohibited_hit"] and r["status"]=="PASS":
            exempted.append({"idx":e.get("idx"),"text":text[:120],"exception":r["exception"]})
        elif r["status"]=="BLOCK":
            violations.append({"kind":"prohibited_arabic_executive_term","idx":e.get("idx"),"text":text[:120],"fix":"state the actual business implication: commitment, risk, financial/commercial impact, margin/cash-flow effect, guarantee, payment term, penalty, or pricing assumption"})
    return {"status":"PASS" if not violations else "FAIL","checked":checked,"violations":violations,"exempted":exempted}
