#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime'))
from brain.visual_search import generate_hypotheses
from brain.reference_grammar_library import retrieve
from artifact.exhibit_engine import build as exhibit_build
from rfp_summary_orchestrator import _mutate
from brain.composition_spec import build_page_composition_spec
from brain.quality_floors_v7_3 import get

def row(name,ok,detail=None): return {'name':name,'status':'PASS' if ok else 'FAIL','detail':detail}
def graph(edges=2):
 ns=[{'id':'A','label':'بيانات','type':'ASSET'},{'id':'B','label':'قرار','type':'DECISION'},{'id':'C','label':'تشغيل','type':'PROCESS'}]
 es=[{'id':'E1','source':'A','target':'B','relation':'ENABLES'},{'id':'E2','source':'B','target':'C','relation':'DEPENDS_ON'}][:edges]
 return {'nodes':ns,'edges':es}
def main():
 rows=[]
 cover={'page_id':'P01','language':'AR','page_role':'COVER','title':'منصة الذكاء الاصطناعي','thesis':'رؤية مستقبلية لقدرة مؤسسية محكومة'}
 r=generate_hypotheses(graph(1),cover); strategies=[x.get('communication_strategy') for x in r.get('hypotheses',[])]
 rows.append(row('IMAGE_LED_reachable_for_cover',r.get('status')=='PASS' and 'IMAGE_LED' in strategies,strategies))
 tech={'page_id':'P02','language':'AR','page_role':'ANALYTICAL','title':'المعمارية التقنية','thesis':'المنصة تربط البيانات والتكامل والأمن والتشغيل ضمن حوكمة واحدة'}
 rt=generate_hypotheses(graph(2),tech); st=[x.get('communication_strategy') for x in rt.get('hypotheses',[])]
 rows.append(row('rich_technical_problem_not_minimal_only',rt.get('status')=='PASS' and any(x in {'ARCHITECTURE_LED','SYSTEM_LED','HYBRID_EXHIBIT'} for x in st),st))
 refs=retrieve('COVER','IMAGE_LED'); rows.append(row('reference_grammar_retrieval_executes',bool(refs) and all(x.get('id') for x in refs),refs))
 ex=exhibit_build(graph(2),tech); rows.append(row('exhibit_engine_no_KeyError',ex.get('status')=='PASS' and ex.get('winner') is None,{'status':ex.get('status'),'refs':ex.get('reference_grammar_ids')}))
 hs=rt.get('hypotheses',[])[:2]; muts=_mutate(hs,tech,graph(2)); logics=[m.get('composition_logic') for m in muts]
 sf=[m for m in muts if m.get('composition_logic')=='SHIFT_FOCAL_POINT']; shifted=bool(sf) and all((m.get('composition_spec') or {}).get('focal_anchor') for m in sf)
 rows.append(row('SHIFT_FOCAL_POINT_reachable_and_physical',shifted,logics))
 # Structural memory may not depend on content words.
 h={'id':'H','communication_strategy':'DECISION_LED','strategy_family':'MINIMAL'}
 s1=build_page_composition_spec(h,{'page_id':'P','title':'أ','thesis':'قرار أول'},graph(1),variant_index=1)
 s2=build_page_composition_spec(h,{'page_id':'P','title':'ب','thesis':'قرار مختلف تمامًا'},graph(1),variant_index=1)
 rows.append(row('composition_signature_excludes_content_hash',s1['structural_signature']==s2['structural_signature'],[s1['structural_signature'],s2['structural_signature']]))
 # Current diagram ceiling single source parity.
 manifest=json.loads((ROOT/'Rashad/Skill/ACTIVE_AUTHORITY_MANIFEST.json').read_text())
 mval=manifest.get('artifact_deck_diagram_ratio_hard_block_above')
 qval=json.loads((ROOT/'QA/Runtime/config/profile_v4.json').read_text())['thresholds']['diagram_ratio_hard_block']
 rows.append(row('diagram_ratio_threshold_parity',mval is not None and float(qval)==float(get('diagram_ratio_hard_block'))==float(mval),{'profile':qval,'brain':get('diagram_ratio_hard_block'),'manifest':mval}))
 # Co-brand composer contract remains one physical-left LTR cluster with Rubix before client.
 # Assert semantic/physical contract, not obsolete absolute child coordinates.
 comp=(ROOT/'Rashad/Brain/runtime/brain/production/composer.py').read_text()
 cluster_left='.cobrand{{position:absolute;left:58px' in comp
 cluster_ltr='display:flex;direction:ltr' in comp
 rub=comp.find('class="brand-logo"'); cli=comp.find('class="client-logo"')
 rows.append(row('cobrand_physical_left_order_contract',cluster_left and cluster_ltr and rub>=0 and cli>=0 and rub<cli,{'cluster_left':cluster_left,'cluster_ltr':cluster_ltr,'rubix_markup':rub,'client_markup':cli}))
 out={'suite':'Rashad v7.3 Artifact Brain Regression','status':'PASS' if all(x['status']=='PASS' for x in rows) else 'FAIL','passed':sum(x['status']=='PASS' for x in rows),'total':len(rows),'rows':rows}
 (ROOT/'QA/Certification/ARTIFACT_BRAIN_REGRESSION_V7_3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
