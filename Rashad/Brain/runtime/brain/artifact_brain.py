from __future__ import annotations
from pathlib import Path
import hashlib, json, re

HERE=Path(__file__).resolve(); CONFIG=HERE.parents[2]/'config'/'artifact_brain_expert_universe_v3.json'
REGISTRY=json.loads(CONFIG.read_text(encoding='utf-8'))

MINIMAL={'STATEMENT_LED','NUMBER_LED','EVIDENCE_LED','TABLE_LED','COMPARISON_LED','DECISION_LED','QUESTION_LED'}
DIAGRAM={'SEQUENCE_LED','PROCESS_LED','SYSTEM_LED','ARCHITECTURE_LED','MAP_LED','JOURNEY_LED','CONTROL_TOWER_LED'}
QUANT={'NUMBER_LED','CHART_LED','TABLE_LED','MATRIX_LED','COMPARISON_LED','TRADEOFF_LED','SCORECARD_LED'}

STRATEGIES={
 'STATEMENT_LED':('MINIMAL','Single conclusion with restrained proof support',1),
 'NUMBER_LED':('MINIMAL','One decisive metric or ratio with its implication',1),
 'EVIDENCE_LED':('ANALYTICAL','Claim-to-proof composition',2),
 'TABLE_LED':('ANALYTICAL','Structured evidence table with analytical emphasis',2),
 'CHART_LED':('ANALYTICAL','Quantitative pattern or comparison',2),
 'COMPARISON_LED':('ANALYTICAL','Two or more alternatives, states, or interpretations',2),
 'MATRIX_LED':('ANALYTICAL','Two-dimensional prioritization or classification',3),
 'DECISION_LED':('MINIMAL','Decision, gates, conditions, and next action',2),
 'QUESTION_LED':('MINIMAL','One executive question resolved by tightly bounded evidence',1),
 'SEQUENCE_LED':('RELATIONAL','Ordered stages where order materially matters',3),
 'PROCESS_LED':('RELATIONAL','Operational flow with ownership or handoffs',3),
 'SYSTEM_LED':('RELATIONAL','Interdependent system with multiple material relationships',4),
 'ARCHITECTURE_LED':('RELATIONAL','Layered technical or operating architecture',4),
 'IMAGE_LED':('CREATIVE','Image carries the primary idea; text remains minimal',2),
 'HYBRID_EXHIBIT':('HYBRID','Deliberate combination of evidence and one relationship system',3),
 'SCENARIO_LED':('ANALYTICAL','Alternative futures or cases with implications',3),
 'TRADEOFF_LED':('ANALYTICAL','Explicit option trade-offs and consequences',3),
 'BEFORE_AFTER':('ANALYTICAL','Current versus future state',2),
 'CAUSE_EFFECT':('RELATIONAL','Causal chain with evidence-backed links',3),
 'PORTFOLIO_LED':('ANALYTICAL','Portfolio distribution, segmentation, or prioritization',3),
 'MAP_LED':('RELATIONAL','Spatial or ecosystem relationship map',3),
 'JOURNEY_LED':('RELATIONAL','Experience or lifecycle journey',3),
 'CONTROL_TOWER_LED':('HYBRID','Decision cockpit around a small set of governed indicators',3),
 'SCORECARD_LED':('ANALYTICAL','Compact status, gate, readiness, or KPI scorecard tied to a decision',2),
}

def _flatten_text(obj):
    if obj is None:return ''
    if isinstance(obj,str):return obj
    if isinstance(obj,(int,float)):return str(obj)
    if isinstance(obj,dict):return ' '.join(_flatten_text(v) for v in obj.values())
    if isinstance(obj,(list,tuple,set)):return ' '.join(_flatten_text(v) for v in obj)
    return str(obj)

def _fingerprint(content_pack,graph):
    raw=(_flatten_text(content_pack)+'|'+_flatten_text(graph)).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()[:12]

def analyze_page_problem(graph,content_pack):
    # Classify the communication problem from page meaning, not from metadata such as evidence locators.
    # Otherwise every grounded consulting page would be misclassified as EVIDENCE/TABLE-led.
    semantic_keys=('title','management_question','evaluator_question','answer','answer_first_thesis','thesis','so_what','executive_implication','counterargument','summary','body_text','decision_supported')
    semantic={k:content_pack.get(k) for k in semantic_keys if isinstance(content_pack,dict) and content_pack.get(k) is not None}
    text=_flatten_text(semantic if semantic else content_pack).lower(); nodes=(graph or {}).get('nodes',[]) or []; edges=(graph or {}).get('edges',[]) or []
    relations={str(e.get('relation','')).upper() for e in edges if isinstance(e,dict)}
    nums=re.findall(r'(?<![A-Za-z])\d+(?:\.\d+)?%?',text)
    decision=(bool(re.search(r'\b(?:go|no-go|hold|decision|recommend|recommendation|recommended)\b',text)) or any(k in text for k in ['قرار','دخول','تعليق القرار','شرط']))
    compare=any(k in text for k in ['versus',' vs ','compare','comparison','مقارنة','مقابل','تعارض','conflict','trade-off','tradeoff'])
    timeline=any(k in text for k in ['timeline','phase','stage','journey','roadmap','month','week','مرحلة','شهر','أسبوع','رحلة','جدول زمني'])
    evidence=any(k in text for k in ['evidence','source','proof','document','دليل','مصدر','مستند','إثبات'])
    architecture=any(k in text for k in ['architecture','platform','api','integration','data','cyber','cloud','infrastructure','معمار','منصة','تكامل','بيانات','أمن'])
    financial=any(k in text for k in ['cost','margin','price','cash','commercial','payment','boq','guarantee','سعر','تكلفة','هامش','دفعات','مالي','تجاري','ضمان'])
    people=any(k in text for k in ['team','resource','staff','role','people','فريق','موارد','كوادر','دور'])
    role_text=' '.join(str(content_pack.get(k,'') or '') for k in ('page_role','rfp_role','role','page_family','title','eyebrow')).lower() if isinstance(content_pack,dict) else ''
    page_family='COVER' if any(k in role_text for k in ['cover','الغلاف']) else ('SECTION_OPENER' if any(k in role_text for k in ['section','opener','الفصل']) else 'ANALYTICAL')
    image_cue=page_family in {'COVER','SECTION_OPENER'} or any(k in text for k in ['vision','future','experience','identity','culture','city','رؤية','مستقبل','تجربة','هوية','ثقافة']) or str((content_pack or {}).get('imagery_mode','')).upper() in {'RASTER_AUGMENTED','GOLDEN_VISUAL_MASTER'}
    has_rel=len(edges)>=2; complex_rel=len(edges)>=4 or len(relations)>=3
    system_earned=complex_rel and (architecture or {'ENABLES','DEPENDS_ON','CONTROLS','FEEDS_BACK','MAPS_TO'} & relations)
    return {'page_fingerprint':_fingerprint(content_pack,graph),'text':text,'number_count':len(nums),'numbers':nums[:12],'decision':decision,'compare':compare,'timeline':timeline,'evidence':evidence,'architecture':architecture,'financial':financial,'people':people,'page_family':page_family,'image_cue':bool(image_cue),'node_count':len(nodes),'edge_count':len(edges),'relations':sorted(relations),'has_relationships':has_rel,'system_complexity_earned':bool(system_earned)}

def route_artifact_councils(graph,content_pack,language='AR',stage='PRE_CONCEPT'):
    f=analyze_page_problem(graph,content_pack)
    stage=str(stage or 'PRE_CONCEPT').upper()
    if stage=='PRE_CONCEPT':
        ids=['ARGUMENT_COUNCIL','EVIDENCE_EPISTEMIC_COUNCIL','COMMUNICATION_STRATEGY_COUNCIL','SIMPLICITY_COUNCIL','INFORMATION_DESIGN_COUNCIL','META_EXPERTISE_ROUTER','ARTIFACT_RED_TEAM']
        if f['number_count']>=2 or f['financial']: ids.append('QUANTITATIVE_EXHIBIT_COUNCIL')
        if f['architecture'] or f['system_complexity_earned']: ids.append('SYSTEMS_ARCHITECTURE_COUNCIL')
        if f['decision']: ids.append('EXECUTIVE_AUDIENCE_COUNCIL')
        if any(k in f['text'] for k in ['rfp','evaluation','evaluator','tender','منافسة','تقييم','كراسة']): ids.append('EVALUATOR_COUNCIL')
        if language.upper().startswith('AR'): ids.append('ARABIC_RTL_COUNCIL')
    elif stage=='ART_DIRECTION':
        ids=['ART_DIRECTION_COUNCIL','SIMPLICITY_COUNCIL','INFORMATION_DESIGN_COUNCIL','CREATIVE_VISUAL_COUNCIL','BRAND_COUNCIL']
        if language.upper().startswith('AR'): ids.append('ARABIC_RTL_COUNCIL')
        if f['number_count']>=2 or f['financial']: ids.append('QUANTITATIVE_EXHIBIT_COUNCIL')
        if f['architecture'] or f['system_complexity_earned']: ids.append('SYSTEMS_ARCHITECTURE_COUNCIL')
    elif stage=='PRODUCTION_READINESS':
        ids=['PRODUCTION_COUNCIL','BRAND_COUNCIL','USER_VISIBLE_DELIVERY_COUNCIL','META_EXPERTISE_ROUTER']
        if language.upper().startswith('AR'): ids.append('ARABIC_RTL_COUNCIL')
    elif stage=='DECK_REVIEW':
        ids=['DECK_ARTISTIC_DIRECTOR_COUNCIL','SIMPLICITY_COUNCIL','ARTIFACT_RED_TEAM','USER_VISIBLE_DELIVERY_COUNCIL']
        if language.upper().startswith('AR'): ids.append('ARABIC_RTL_COUNCIL')
    else:
        return {'status':'BLOCKED','reason':'UNKNOWN_ARTIFACT_COUNCIL_STAGE','stage':stage}
    ids=list(dict.fromkeys(ids))[:REGISTRY['runtime_activation_policy']['max_active_councils_per_page']]
    councils={c['id']:c for c in REGISTRY['councils']}; roles=[]
    for cid in ids:
        if cid not in councils: return {'status':'BLOCKED','reason':'UNKNOWN_ARTIFACT_COUNCIL','council_id':cid,'stage':stage}
        for rid in councils[cid]['roles']:
            if rid not in roles: roles.append(rid)
    roles=roles[:REGISTRY['runtime_activation_policy']['max_active_roles_per_page']]
    return {'status':'PASS','stage':stage,'page_features':f,'active_councils':ids,'active_roles':roles,'registered_council_count':len(REGISTRY['councils']),'registered_role_count':len(REGISTRY['roles']),'bounded_activation':True}


def _score(strategy,f):
    family,_,complexity=STRATEGIES[strategy]; s=50.0
    # simplicity preference: lower complexity wins when equally explanatory
    s += (5-complexity)*3
    if strategy=='STATEMENT_LED': s+=10
    if strategy=='IMAGE_LED' and f.get('image_cue'): s+=32
    if strategy=='IMAGE_LED' and f.get('page_family') in {'COVER','SECTION_OPENER'}: s+=18
    if strategy=='IMAGE_LED' and not f.get('image_cue'): s-=20
    if f['number_count']>=1 and strategy=='NUMBER_LED': s+=24
    if f['number_count']>=3 and strategy in {'TABLE_LED','CHART_LED'}: s+=18
    if f['evidence'] and strategy in {'EVIDENCE_LED','TABLE_LED'}: s+=18
    if f['compare'] and strategy in {'COMPARISON_LED','TRADEOFF_LED','BEFORE_AFTER'}: s+=22
    if f['decision'] and strategy=='DECISION_LED': s+=26
    if f['decision'] and strategy=='SCORECARD_LED': s+=20
    if f['timeline'] and strategy in {'SEQUENCE_LED','JOURNEY_LED','PROCESS_LED'}: s+=22
    if f['architecture'] and strategy=='ARCHITECTURE_LED': s+=24
    if f['people'] and strategy in {'NUMBER_LED','TABLE_LED','PORTFOLIO_LED','SCORECARD_LED'}: s+=14
    if f['system_complexity_earned'] and strategy=='SYSTEM_LED': s+=24
    if not f['system_complexity_earned'] and strategy in {'SYSTEM_LED','ARCHITECTURE_LED'}: s-=28
    if not f['has_relationships'] and strategy in DIAGRAM: s-=30
    # quality floor: do not reward visually impoverished statement-only treatment for a rich analytical problem.
    richness=(f.get('number_count',0)>=2)+(f.get('evidence',False))+(f.get('architecture',False))+(f.get('compare',False))+(f.get('timeline',False))+(f.get('image_cue',False))
    if richness>=3 and strategy in {'STATEMENT_LED','QUESTION_LED'}: s-=14
    return round(max(0,min(100,s)),1)

def _candidate_pool(f):
    pool=['STATEMENT_LED']
    if f.get('image_cue'): pool+=['IMAGE_LED']
    if f['number_count']>=1: pool+=['NUMBER_LED']
    if f['decision']: pool+=['DECISION_LED','SCORECARD_LED']
    if f['compare']: pool+=['COMPARISON_LED','TRADEOFF_LED']
    if f['evidence']: pool+=['EVIDENCE_LED','TABLE_LED']
    if f['number_count']>=3: pool+=['TABLE_LED','CHART_LED']
    if f['people']: pool+=['PORTFOLIO_LED','TABLE_LED']
    if f['timeline']: pool+=['SEQUENCE_LED','JOURNEY_LED']
    if f['architecture']: pool+=['ARCHITECTURE_LED']
    if f['system_complexity_earned']: pool+=['SYSTEM_LED']
    if f['has_relationships']: pool+=['CAUSE_EFFECT','HYBRID_EXHIBIT']
    pool+=['QUESTION_LED','COMPARISON_LED','EVIDENCE_LED','HYBRID_EXHIBIT']
    out=[]
    for x in pool:
        if x not in out: out.append(x)
    return out


def _visual_concept_brief(strategy,f,content_pack):
    thesis=(content_pack.get('thesis') or content_pack.get('answer_first_thesis') or content_pack.get('answer') or '').strip()
    focal={
      'STATEMENT_LED':'one answer first; proof stays subordinate',
      'NUMBER_LED':'one quantified truth dominates; implication is secondary',
      'EVIDENCE_LED':'claim and proof are visually inseparable',
      'TABLE_LED':'scanable structure reveals comparison or obligation',
      'CHART_LED':'pattern is visible before labels are read',
      'COMPARISON_LED':'difference, trade-off or contrast is the focal logic',
      'MATRIX_LED':'priority emerges from two explicit axes',
      'DECISION_LED':'decision and conditions are visible before detail',
      'SCORECARD_LED':'status/gates create immediate management action',
      'SEQUENCE_LED':'order and transition are the message',
      'PROCESS_LED':'handoffs/ownership are the message',
      'SYSTEM_LED':'interdependence and feedback are the message',
      'ARCHITECTURE_LED':'layers and interfaces are the message',
      'IMAGE_LED':'visual metaphor/sector image carries the idea, not decoration',
      'HYBRID_EXHIBIT':'one analytical proof structure plus one earned relationship',
    }.get(strategy,'one page-specific thesis with the simplest adequate visual form')
    proof='quantified evidence' if f['number_count'] else ('source/evidence' if f['evidence'] else '2–4 bounded proof points')
    return {
      'focal_rule':focal,
      'page_specific_thesis':thesis,
      'proof_encoding':proof,
      'negative_space_role':'protect focal hierarchy; never empty filler',
      'anti_template_rule':'composition must be derived from this page thesis/evidence; label-swap reuse is a hard fail',
      'renderer_constraint':'geometry is downstream; cards/boxes are optional supporting surfaces only',
      'complexity_rule':'use the least complex form that preserves the business relationship',
    }

def generate_communication_hypotheses(graph,content_pack,count=5):
    f=analyze_page_problem(graph,content_pack); pool=_candidate_pool(f)
    ranked=sorted(pool,key=lambda x:(-_score(x,f),STRATEGIES[x][2],x))
    selected=[]; families=set()
    # first, strongest candidate
    for st in ranked:
        fam=STRATEGIES[st][0]
        if not selected or fam not in families or len(selected)>=3:
            selected.append(st); families.add(fam)
        if len(selected)==count: break
    for st in ranked:
        if len(selected)>=count: break
        if st not in selected: selected.append(st); families.add(STRATEGIES[st][0])
    # Always force a minimal/non-diagram hypothesis into the search.
    if not any(s in MINIMAL for s in selected): selected[-1]='STATEMENT_LED'
    # At least 3 communication families; fallback with non-diagram analytical options.
    fallback=['STATEMENT_LED','EVIDENCE_LED','COMPARISON_LED','TABLE_LED','HYBRID_EXHIBIT']
    while len(set(STRATEGIES[s][0] for s in selected))<3:
        for st in fallback:
            if st not in selected:
                selected[-1]=st; break
        else: break
    # Deterministically permute ids by page fingerprint so candidate position carries no semantics.
    shift=int(f['page_fingerprint'][:2],16)%len(selected); ordered=selected[shift:]+selected[:shift]
    hs=[]
    for i,st in enumerate(ordered,1):
        fam,desc,complexity=STRATEGIES[st]; fit=_score(st,f)
        sig=f"{st}|{fam}|C{complexity}|{hashlib.sha1((st+'|'+fam+'|'+str(complexity)).encode()).hexdigest()[:8]}"
        hs.append({'id':f'H{i}','communication_strategy':st,'strategy_family':fam,'communication_intent':desc,'complexity_level':complexity,'partner_fit_score':fit,'simplicity_score':round(100-complexity*12,1),'page_fingerprint':f['page_fingerprint'],'structural_signature':sig,'visual_concept_id':'VC-'+hashlib.sha1((st+f['page_fingerprint']+str(i)).encode()).hexdigest()[:10].upper(),'visual_concept_brief':_visual_concept_brief(st,f,content_pack),'system_complexity_earned':f['system_complexity_earned'],'visual_thesis':content_pack.get('thesis') or content_pack.get('answer_first_thesis') or '', 'selection_basis':'ANSWER_EVIDENCE_AUDIENCE_SIMPLEST_FORM'})
    return {'status':'PASS' if len(hs)==count and len({h['communication_strategy'] for h in hs})==count and len({h['strategy_family'] for h in hs})>=3 else 'FAIL','hypotheses':hs,'page_features':f,'distinct_communication_strategies':len({h['communication_strategy'] for h in hs}),'distinct_strategy_families':len({h['strategy_family'] for h in hs}),'contains_minimal_hypothesis':any(h['communication_strategy'] in MINIMAL for h in hs),'diagram_only_search':all(h['communication_strategy'] in DIAGRAM for h in hs),'winner':None,'selection_status':'PENDING_RENDER_AND_JUDGMENT'}

def partner_skeptic_test(hypothesis,page_features):
    st=hypothesis['communication_strategy']; reasons=[]
    if st in DIAGRAM and not page_features['has_relationships']: reasons.append('DIAGRAM_WITHOUT_MATERIAL_RELATIONSHIPS')
    if st in {'SYSTEM_LED','ARCHITECTURE_LED'} and not page_features['system_complexity_earned'] and not page_features['architecture']: reasons.append('COMPLEXITY_NOT_EARNED')
    return {'status':'PASS' if not reasons else 'REJECT','reasons':reasons,'five_second_test_required':True,'generic_layout_swap_test_required':True,'remove_diagram_test_required':st in DIAGRAM}

def provisional_partner_selection(hypotheses):
    # Provisional draft only. No positional or H1 preference; candidate id is explicitly excluded from score.
    accepted=[h for h in hypotheses]
    ranked=sorted(accepted,key=lambda h:(float(h.get('partner_fit_score',0)),float(h.get('simplicity_score',0))),reverse=True)
    w=ranked[0]
    return {'status':'PASS','candidate_id':w['id'],'communication_strategy':w['communication_strategy'],'selection_authority':'PROVISIONAL_PARTNER_HEURISTIC_NOT_INDEPENDENT','selection_reason':'Highest communication fit, then simplicity. Candidate position/id is not a scoring input.','independent':False}
