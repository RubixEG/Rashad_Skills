from __future__ import annotations
import os,subprocess

def installed_families():
    try:
        out=subprocess.check_output(['fc-list',':','family'],text=True,stderr=subprocess.DEVNULL,timeout=8)
        fam=set()
        for line in out.splitlines():
            for x in line.split(','): fam.add(x.strip().lower())
        return fam
    except Exception:return set()

def check_brand_fonts(required=('Montserrat Arabic','Montserrat'),allow_test_fallback=False):
    fam=installed_families(); missing=[x for x in required if x.lower() not in fam]
    allow=allow_test_fallback or os.getenv('RASHAD_TEST_ALLOW_FONT_FALLBACK')=='1'
    return {'status':'PASS' if not missing or allow else 'BLOCKED','required':list(required),'missing':missing,'test_fallback_waiver':bool(missing and allow),'rule':'Production release cannot render with fallback fonts. Test fallback is certification-only and must be explicit.'}
