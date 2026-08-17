from pathlib import Path
import json
from jsonschema import Draft202012Validator

HERE=Path(__file__).resolve().parents[1]
RELATIONS={"ENABLES","DEPENDS_ON","FLOWS_TO","CONTROLS","MEASURES","EVIDENCES","RISKS","PRIORITIZES","OWNS","APPROVES","FEEDS_BACK","THRESHOLD_FOR","MAPS_TO","BLOCKS"}

def load(name): return json.loads((HERE/'schemas'/name).read_text())

def validate_schema(obj,name):
    errs=sorted(Draft202012Validator(load(name)).iter_errors(obj),key=lambda e:list(e.path))
    return [f"{'.'.join(map(str,e.path)) or '$'}: {e.message}" for e in errs]

def validate_graph(obj):
    errs=validate_schema(obj,'relationship-graph-v6.schema.json')
    ids=[n.get('id') for n in obj.get('nodes',[])]
    eids=[e.get('id') for e in obj.get('edges',[])]
    if len(ids)!=len(set(ids)): errs.append('duplicate node id')
    if len(eids)!=len(set(eids)): errs.append('duplicate edge id')
    S=set(ids)
    for e in obj.get('edges',[]):
        if e.get('source') not in S: errs.append(f"edge {e.get('id')} source missing: {e.get('source')}")
        if e.get('target') not in S: errs.append(f"edge {e.get('id')} target missing: {e.get('target')}")
        if e.get('source')==e.get('target'): errs.append(f"edge {e.get('id')} self-loop requires explicit modelling review")
        if e.get('relation') not in RELATIONS: errs.append(f"invalid relation {e.get('relation')}")
    return errs


def validate_evidence_ledger(obj): return validate_schema(obj,'evidence-ledger.schema.json')
def validate_firewall(obj): return validate_schema(obj,'execution-firewall.schema.json')
