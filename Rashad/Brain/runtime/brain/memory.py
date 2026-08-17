from __future__ import annotations
from .utils import new_id,obj_hash

class EngagementMemory:
    # Append-only engagement memory. It never silently rewrites evidence or decisions.
    def __init__(self): self.records=[]
    def append(self,kind,payload,depends_on=None):
        rec={'record_id':new_id('MEM'),'kind':kind,'payload':payload,'depends_on':depends_on or [],'payload_hash':obj_hash(payload),'status':'ACTIVE'}
        self.records.append(rec); return rec
    def invalidate(self,record_ids,reason):
        ids=set(record_ids)
        for r in self.records:
            if r['record_id'] in ids: r['status']='STALE'; r['stale_reason']=reason
    def active(self,kind=None): return [r for r in self.records if r['status']=='ACTIVE' and (kind is None or r['kind']==kind)]
