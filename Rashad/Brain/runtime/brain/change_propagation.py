from __future__ import annotations

def impact_set(changed_ids, dependency_edges):
    # Return downstream objects invalidated by changed evidence/assumptions/decisions.
    out=set(changed_ids); changed=True
    while changed:
        changed=False
        for e in dependency_edges:
            if e.get('source') in out and e.get('target') not in out:
                out.add(e.get('target')); changed=True
    return sorted(x for x in out if x is not None)

def stale_objects(changed_ids, objects):
    edges=[]
    for oid,obj in objects.items():
        for dep in obj.get('depends_on',[]): edges.append({'source':dep,'target':oid})
    impacted=set(impact_set(changed_ids,edges))
    return sorted(x for x in impacted if x not in set(changed_ids))
