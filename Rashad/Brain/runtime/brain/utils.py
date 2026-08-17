from __future__ import annotations
import json, hashlib, uuid
from pathlib import Path

def canon(obj): return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def obj_hash(obj): return hashlib.sha256(canon(obj).encode('utf-8')).hexdigest()
def file_hash(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def new_id(prefix): return f"{prefix}-{uuid.uuid4().hex[:16].upper()}"
def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def dump(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8'); return p
