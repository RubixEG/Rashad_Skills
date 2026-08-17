from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REG=ROOT/'config/actor_ontology.json'

def registry(): return json.loads(REG.read_text(encoding='utf-8'))
def actor(actor_id): return next((x for x in registry()['actors'] if x['id']==actor_id),None)
def validate_actor_separation(a,b):
    aa,bb=actor(a),actor(b)
    if not aa or not bb: return {'status':'BLOCKED','reason':'UNKNOWN_ACTOR'}
    return {'status':'PASS' if a!=b and aa['type']!=bb['type'] else 'BLOCKED','actor_a_type':aa['type'],'actor_b_type':bb['type'],'reason':None if a!=b and aa['type']!=bb['type'] else 'ACTOR_ROLE_COLLISION'}
def cognitive_job(actor_id):
    a=actor(actor_id); return {'status':'PASS','actor_id':actor_id,'actor_type':a['type'],'functions':a['functions']} if a else {'status':'BLOCKED','reason':'UNKNOWN_ACTOR'}
def apply_governor_veto(violations):
    govs={x['veto']:x['id'] for x in registry()['actors'] if x['type']=='GOVERNOR' and x.get('veto')}
    hits=[{'violation':v,'governor':govs[v]} for v in violations if v in govs]
    return {'status':'BLOCKED' if hits else 'PASS','vetoes':hits,'override_allowed':False}
