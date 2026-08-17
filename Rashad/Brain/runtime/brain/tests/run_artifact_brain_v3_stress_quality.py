#!/usr/bin/env python3
from __future__ import annotations
import json, random, string, sys, time
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve(); RUNTIME=HERE.parents[2]; sys.path.insert(0,str(RUNTIME))
from brain.artifact_brain import generate_communication_hypotheses, provisional_partner_selection, route_artifact_councils, DIAGRAM, STRATEGIES
from brain.actual_output_qa import evaluate_deck_output

SEED=20260816
random.seed(SEED)
results=[]
def add(name,ok,detail=None): results.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})

def suffix(n=10): return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))

def g(edges): return {'nodes':[{'id':x} for x in 'ABCDE'],'edges':edges}
complex_edges=[
 {'source':'A','target':'B','relation':'ENABLES'},
 {'source':'B','target':'C','relation':'DEPENDS_ON'},
 {'source':'C','target':'D','relation':'FEEDS_BACK'},
 {'source':'D','target':'A','relation':'CONTROLS'},
]
flow_edges=[{'source':'A','target':'B','relation':'FLOWS_TO'},{'source':'B','target':'C','relation':'FLOWS_TO'}]
scenarios=[
 ('statement','The client is buying an integrated innovation operating model, not a standalone platform.',[],'STATEMENT_LED'),
 ('decision','Management decision HOLD until evidence gaps close and conditions are met.',[],'DECISION_LED'),
 ('quant','Penalty exposure 20%, performance bond 5%, bid security 1%.',[],'NUMBER_LED'),
 ('conflict','The source document conflicts with the security annex and must be reconciled before pricing.',[],'COMPARISON_LED'),
 ('arch_simple','Platform architecture API integration data cyber cloud infrastructure.',[],'NON_DIAGRAM'),
 ('arch_complex','Platform architecture API integration data cyber cloud infrastructure.',complex_edges,'ARCHITECTURE_OR_SYSTEM'),
 ('timeline','The delivery journey moves through mobilization, assessment, build, UAT and support stage.',flow_edges,'SEQUENCE_FAMILY'),
 ('people','Team staffing roles, capacity and resource readiness drive delivery confidence.',[],'NON_DIAGRAM'),
 ('compare','Compare option A versus option B and show the trade-off in risk and feasibility.',[],'COMPARISON_LED'),
 ('evidence','Evidence from source document and proof must support every material claim.',[],'EVIDENCE_OR_TABLE'),
 ('gate','Decision readiness gates, conditions and status determine whether management can proceed.',[],'DECISION_OR_SCORECARD'),
 ('system','An operating system connects strategy, governance, delivery and measurement through feedback.',complex_edges,'SYSTEM_LED'),
]

start=time.perf_counter(); crashes=0; page_runs=2400
ids=Counter(); winners=Counter(); by_scenario={k:Counter() for k,_,_,_ in scenarios}; failures=[]
for i in range(page_runs):
    name,text,edges,expect=scenarios[i%len(scenarios)]
    cp={'thesis':text+' '+suffix(),'evidence':['DOC-X p.1'],'language':'AR'}
    try:
        r=generate_communication_hypotheses(g(edges),cp)
        if r.get('status')!='PASS' or len(r.get('hypotheses',[]))!=5 or len({h['communication_strategy'] for h in r['hypotheses']})!=5 or len({h['strategy_family'] for h in r['hypotheses']})<3 or r.get('diagram_only_search') or not r.get('contains_minimal_hypothesis'):
            failures.append({'i':i,'scenario':name,'result':r})
            continue
        rt=route_artifact_councils(g(edges),cp)
        if len(rt['active_councils'])>10 or len(rt['active_roles'])>18: failures.append({'i':i,'scenario':name,'routing':rt}); continue
        sel=provisional_partner_selection(r['hypotheses']); ids[sel['candidate_id']]+=1; winners[sel['communication_strategy']]+=1; by_scenario[name][sel['communication_strategy']]+=1
    except Exception as e:
        crashes+=1; failures.append({'i':i,'scenario':name,'exception':repr(e)})

add('stress_no_crashes',crashes==0,{'page_runs':page_runs,'crashes':crashes})
add('stress_all_page_searches_valid',not failures,failures[:5])
add('candidate_position_bias_below_35_percent',max(ids.values(),default=0)/max(1,sum(ids.values()))<0.35,dict(ids))
add('selected_strategy_diversity_at_least_8',len(winners)>=8,dict(winners))
add('no_single_strategy_dominates_over_45_percent',max(winners.values(),default=0)/max(1,sum(winners.values()))<0.45,dict(winners))
add('simple_statement_prefers_statement',by_scenario['statement']['STATEMENT_LED']/max(1,sum(by_scenario['statement'].values()))>=0.95,dict(by_scenario['statement']))
add('quant_prefers_number_led',by_scenario['quant']['NUMBER_LED']/max(1,sum(by_scenario['quant'].values()))>=0.95,dict(by_scenario['quant']))
add('comparison_prefers_comparison',by_scenario['compare']['COMPARISON_LED']/max(1,sum(by_scenario['compare'].values()))>=0.90,dict(by_scenario['compare']))
add('simple_architecture_does_not_force_diagram',sum(v for k,v in by_scenario['arch_simple'].items() if k in DIAGRAM)==0,dict(by_scenario['arch_simple']))
add('complex_architecture_earns_relational_form',sum(v for k,v in by_scenario['arch_complex'].items() if k in {'ARCHITECTURE_LED','SYSTEM_LED'})/max(1,sum(by_scenario['arch_complex'].values()))>=0.90,dict(by_scenario['arch_complex']))
add('system_relationships_select_system',by_scenario['system']['SYSTEM_LED']/max(1,sum(by_scenario['system'].values()))>=0.90,dict(by_scenario['system']))
add('timeline_prefers_sequence_family',sum(v for k,v in by_scenario['timeline'].items() if k in {'JOURNEY_LED','SEQUENCE_LED','PROCESS_LED'})/max(1,sum(by_scenario['timeline'].values()))>=0.90,dict(by_scenario['timeline']))
add('runtime_has_24_communication_strategies',len(STRATEGIES)==24,sorted(STRATEGIES))

# Deck quality stress: valid varied decks should pass when actual pixel review is present.
base=['STATEMENT_LED','SYSTEM_LED','TABLE_LED','NUMBER_LED','ARCHITECTURE_LED','COMPARISON_LED','DECISION_LED','CHART_LED','SCORECARD_LED','EVIDENCE_LED','JOURNEY_LED','HYBRID_EXHIBIT']
def page(i,s,cid=None,comp=None,pixel=True,hsh=None):
    hs=[
      {'communication_strategy':'STATEMENT_LED','strategy_family':'MINIMAL'},
      {'communication_strategy':'NUMBER_LED','strategy_family':'MINIMAL'},
      {'communication_strategy':'EVIDENCE_LED','strategy_family':'ANALYTICAL'},
      {'communication_strategy':'COMPARISON_LED','strategy_family':'ANALYTICAL'},
      {'communication_strategy':'SYSTEM_LED','strategy_family':'RELATIONAL'},
    ]
    return {'page_id':f'P{i:02d}','selected_render_hash':hsh or f'RH-{i}-{suffix(5)}','selected_strategy':s,'selected_candidate_id':cid or f'H{(i%5)+1}','composition_logic':comp or f'C{i}-{suffix(4)}','hypotheses':hs,'actual_pixel_review':{'status':'PASS' if pixel else 'NOT_EXECUTED'}}

deck_runs=300; good_fail=[]
for d in range(deck_runs):
    order=base[:]; random.shuffle(order)
    pages=[page(i+1,s) for i,s in enumerate(order)]
    r=evaluate_deck_output(pages)
    if r['status']!='PASS': good_fail.append({'deck':d,'result':r,'strategies':order})
add('varied_deck_quality_stress_300_pass',not good_fail,good_fail[:3])

# Adversarial deck mutations must all block / downgrade as designed.
attacks=[]
def attack(name,pages,required):
    r=evaluate_deck_output(pages); attacks.append({'name':name,'blocked':required in r.get('blockers',[]),'result':r})
attack('diagram_overuse',[page(i+1,'SYSTEM_LED',cid=f'H{(i%5)+1}') for i in range(12)],'DECK_DIAGRAM_OVERUSE')
attack('same_strategy_run',[page(i+1,'TABLE_LED',cid=f'H{(i%5)+1}') for i in range(8)],'FOUR_CONSECUTIVE_SAME_COMMUNICATION_STRATEGY')
attack('position_bias',[page(i+1,base[i%len(base)],cid='H1') for i in range(12)],'POSITIONAL_HYPOTHESIS_WINNER_BIAS')
attack('render_reuse',[page(i+1,base[i%len(base)],hsh='SAME') for i in range(6)],'CROSS_PAGE_RENDER_HASH_REUSE')
attack('generic_composition',[page(i+1,base[i%len(base)],comp='SAME') for i in range(8)],'GENERIC_COMPOSITION_REPETITION')
add('adversarial_deck_attacks_blocked',all(x['blocked'] for x in attacks),attacks)
partial=evaluate_deck_output([page(i+1,base[i],pixel=False) for i in range(6)])
add('missing_pixel_review_never_full_pass',partial['status']=='DRAFT_QA_PARTIAL' and partial['actual_pixel_reviews']==0,partial)

elapsed=round(time.perf_counter()-start,3)
out={'suite':'Rashad Artifact Intelligence Brain v3.3 Stress & Quality','status':'PASS' if all(x['status']=='PASS' for x in results) else 'FAIL','seed':SEED,'page_runs':page_runs,'deck_runs':deck_runs,'adversarial_deck_attacks':len(attacks),'crashes':crashes,'elapsed_seconds':elapsed,'selected_candidate_id_distribution':dict(ids),'selected_strategy_distribution':dict(winners),'scenario_winner_distributions':{k:dict(v) for k,v in by_scenario.items()},'passed':sum(x['status']=='PASS' for x in results),'total':len(results),'tests':results}
Path(__file__).with_name('ARTIFACT_BRAIN_V3_STRESS_QUALITY_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:out[k] for k in ['suite','status','page_runs','deck_runs','adversarial_deck_attacks','crashes','elapsed_seconds','passed','total','selected_candidate_id_distribution','selected_strategy_distribution']},ensure_ascii=False,indent=2))
raise SystemExit(0 if out['status']=='PASS' else 1)
