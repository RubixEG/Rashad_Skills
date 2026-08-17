from __future__ import annotations
from .utils import new_id,obj_hash
class Blackboard:
    def __init__(self,task):
        self.data={'session_id':new_id('BRAIN'),'task':task,'state':'INIT','route':[],'invocations':[],'findings':[],'decisions':[],'hash_chain':[],'release':{'status':'NOT_EVALUATED'}}; self._append_hash('INIT')
    def _append_hash(self,event):
        prev=self.data['hash_chain'][-1]['hash'] if self.data['hash_chain'] else None
        payload={'event':event,'prev':prev,'state':self.data['state'],'task':self.data['task'],'invocation_count':len(self.data['invocations']),'finding_count':len(self.data['findings'])}
        self.data['hash_chain'].append({'event':event,'prev':prev,'hash':obj_hash(payload)})
    def state(self,s): self.data['state']=s; self._append_hash('STATE:'+s)
    def add_invocation(self,x): self.data['invocations'].append(x); self._append_hash('INVOCATION')
    def add_findings(self,council_id,function,inv):
        for f in inv.get('findings',[]):
            self.data['findings'].append({'finding_id':new_id('FND'),'council_id':council_id,'function':function,'status':f.get('status','FINDING'),'claim':f.get('claim',''),'evidence_refs':f.get('evidence_refs',[]),'severity':f.get('severity','MEDIUM'),'disposition':f.get('disposition','RESOLVED' if f.get('status')=='NO_MATERIAL_OBJECTION' else 'OPEN'),'invocation_id':inv.get('invocation_id'),'input_hash':inv.get('input_hash')})
        self._append_hash('FINDINGS')
