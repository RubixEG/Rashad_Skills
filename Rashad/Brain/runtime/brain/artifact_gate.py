from __future__ import annotations
from .execution_proof import validate_brain_execution_proof, validate_artifact_execution_ledger
OUTPUT_LEVELS={
    'CONTENT_DRAFT':1,
    'INTERNAL_CONCEPT_DRAFT':2,
    'USER_VISIBLE_ARTIFACT_DRAFT':3,
    'RELEASE_CANDIDATE':4,
    'RELEASED':5,
}
ALIASES={'ARTIFACT_DRAFT':'USER_VISIBLE_ARTIFACT_DRAFT'}
MINIMAL_STRATEGIES={'STATEMENT_LED','NUMBER_LED','EVIDENCE_LED','TABLE_LED','COMPARISON_LED','DECISION_LED','QUESTION_LED'}
CONCEPT_RENDER_PREFIX='COMMUNICATION_STRATEGY_CONCEPT_RENDER'


def _okobj(x): return isinstance(x,dict) and bool(x)
def _render_hashes(state): return [x.get('actual_render_hash') for x in state.get('render_evidence',[]) if isinstance(x,dict)]
def _hyp_sigs(state): return [x.get('structural_signature') for x in state.get('hypotheses',[]) if isinstance(x,dict)]

def claim_visual_binding_check(state):
    bindings=state.get('claim_visual_bindings',[]); material=state.get('material_claim_ids',[]); by={x.get('claim_id'):x for x in bindings if isinstance(x,dict)}; missing=[]
    for cid in material:
        b=by.get(cid) or {}
        if not b.get('evidence_refs') or not b.get('visual_node_ids'): missing.append(cid)
    return {'status':'PASS' if not missing else 'BLOCKED','missing_claim_bindings':missing}

def validate_concept_search(state):
    errs=[]
    for k in ('brain_session','page_contract','cognitive_packet','artifact_intent','semantic_graph','artifact_council_execution'):
        if not _okobj(state.get(k)): errs.append('MISSING_'+k.upper())
    bs=state.get('brain_session',{}) or {}
    bp=validate_brain_execution_proof(bs)
    if bp.get('status')!='PASS': errs.append('BRAIN_EXECUTION_PROOF_REQUIRED')
    ac=state.get('artifact_council_execution',{}) or {}
    if validate_artifact_execution_ledger(ac,'PRE_CONCEPT').get('status')!='PASS': errs.append('ARTIFACT_COUNCIL_EXECUTION_REQUIRED')
    ev=state.get('evidence_lineage')
    if not isinstance(ev,(dict,list)) or not ev: errs.append('EVIDENCE_LINEAGE_REQUIRED')
    hs=[x for x in state.get('hypotheses',[]) if isinstance(x,dict)]
    sigs=_hyp_sigs(state); rh=_render_hashes(state)
    strategies=[x.get('communication_strategy') for x in hs]; families=[x.get('strategy_family') for x in hs]
    if len(sigs)<5 or len(set(sigs[:5]))<5 or any(not x for x in sigs[:5]): errs.append('FIVE_DISTINCT_HYPOTHESES_REQUIRED')
    if len(strategies)<5 or len(set(strategies[:5]))<5 or any(not x for x in strategies[:5]): errs.append('FIVE_DISTINCT_COMMUNICATION_STRATEGIES_REQUIRED')
    if len({x for x in families[:5] if x})<3: errs.append('THREE_COMMUNICATION_FAMILIES_REQUIRED')
    if not any(x in MINIMAL_STRATEGIES for x in strategies[:5]): errs.append('MINIMAL_NON_DIAGRAM_HYPOTHESIS_REQUIRED')
    if len(rh)<5 or len(set(rh[:5]))<5 or any(not x for x in rh[:5]): errs.append('FIVE_DISTINCT_CONCEPT_RENDER_HASHES_REQUIRED')
    return {'status':'PASS' if not errs else 'BLOCKED','errors':errs}

def validate_user_visible_artifact(state):
    errs=[]
    cs=validate_concept_search(state)
    if cs['status']!='PASS': errs.extend(cs['errors'])
    for k in ('selected_master','brand_preflight','qa_state','art_direction_execution','production_council_execution'):
        if not _okobj(state.get(k)): errs.append('MISSING_'+k.upper())
    if validate_artifact_execution_ledger(state.get('art_direction_execution') or {},'ART_DIRECTION').get('status')!='PASS': errs.append('ART_DIRECTION_EXECUTION_REQUIRED')
    if validate_artifact_execution_ledger(state.get('production_council_execution') or {},'PRODUCTION_READINESS').get('status')!='PASS': errs.append('PRODUCTION_COUNCIL_EXECUTION_REQUIRED')
    sm=state.get('selected_master',{}) or {}
    if sm.get('selection_authority') in {'POSITIONAL_DEFAULT','PROVISIONAL_PARTNER_HEURISTIC_NOT_INDEPENDENT'}: errs.append('USER_VISIBLE_MASTER_CANNOT_USE_PROVISIONAL_OR_POSITIONAL_AUTHORITY')
    if sm.get('render_kind')!='PRODUCTION_PAGE_RENDER': errs.append('USER_VISIBLE_MASTER_MUST_BE_PRODUCTION_PAGE_RENDER')
    if not sm.get('production_render_id') or not sm.get('actual_render_hash'): errs.append('PRODUCTION_RENDER_PROOF_REQUIRED')
    if str(sm.get('render_kind','')).startswith(CONCEPT_RENDER_PREFIX): errs.append('CONCEPT_RENDER_CANNOT_BE_USER_VISIBLE_MASTER')
    bp=state.get('brand_preflight',{}) or {}
    if bp.get('status')!='PASS' or bp.get('rubix_asset_status')!='VERIFIED': errs.append('BRAND_PREFLIGHT_NOT_PROVEN')
    qa=state.get('qa_state',{}) or {}
    if qa.get('status') not in ('USER_VISIBLE_QA_PASS','QA_CANDIDATE_PASS'): errs.append('USER_VISIBLE_ACTUAL_OUTPUT_QA_NOT_PASSED')
    if qa.get('qa_scope')!='ACTUAL_RENDERED_OUTPUT': errs.append('QA_MUST_TARGET_ACTUAL_RENDERED_OUTPUT')
    if qa.get('actual_output_qa_status')!='PASS': errs.append('ACTUAL_OUTPUT_QA_MUST_PASS_NOT_PARTIAL')
    if qa.get('actual_pixel_visual_quality_status')!='PASS': errs.append('ACTUAL_PIXEL_QA_REQUIRED_FOR_USER_VISIBLE')
    if qa.get('repair_loop_status') not in ('PASS','NOT_REQUIRED_FIRST_PASS_PASS'): errs.append('QA_REPAIR_LOOP_NOT_CLOSED')
    b=claim_visual_binding_check(state)
    if b['status']!='PASS': errs.append('CLAIM_TO_VISUAL_EVIDENCE_BINDING_INCOMPLETE')
    return {'status':'PASS' if not errs else 'BLOCKED','errors':errs}

# Backward compatibility: old name now means user-visible, not internal concept draft.
def validate_artifact_draft(state):
    return validate_user_visible_artifact(state)

def derive_output_classification(state):
    content=state.get('content_status')=='PASS' and state.get('evidence_status')=='PASS'
    if not content: return 'BLOCKED'
    concept=validate_concept_search(state)
    if concept['status']!='PASS': return 'CONTENT_DRAFT'
    user=validate_user_visible_artifact(state)
    if user['status']!='PASS': return 'INTERNAL_CONCEPT_DRAFT'
    ind=state.get('independent_judgment',{}); qa=state.get('qa_state',{}); rel=state.get('release',{})
    release_candidate=ind.get('status')=='PASS' and ind.get('independent') is True and qa.get('status')=='QA_CANDIDATE_PASS' and state.get('parity_status')=='PASS' and state.get('proof_index_status')=='PASS'
    if not release_candidate: return 'USER_VISIBLE_ARTIFACT_DRAFT'
    if rel.get('release_chair_status')=='RELEASED' and rel.get('release_authority')=='RASHAD_BRAIN_RELEASE_CHAIR': return 'RELEASED'
    return 'RELEASE_CANDIDATE'

def guard_composer(state, requested='USER_VISIBLE_ARTIFACT_DRAFT'):
    requested=ALIASES.get(requested,requested)
    if requested not in OUTPUT_LEVELS: return {'status':'BLOCK_RENDER','reason':'UNKNOWN_OUTPUT_CLASSIFICATION'}
    derived=derive_output_classification(state)
    if derived=='BLOCKED': return {'status':'BLOCK_RENDER','reason':'CONTENT_OR_EVIDENCE_NOT_READY','derived_classification':derived}
    if OUTPUT_LEVELS[derived] < OUTPUT_LEVELS[requested]:
        detail=validate_user_visible_artifact(state) if OUTPUT_LEVELS[requested]>=OUTPUT_LEVELS['USER_VISIBLE_ARTIFACT_DRAFT'] else validate_concept_search(state)
        return {'status':'BLOCK_RENDER','reason':'ARTIFACT_PIPELINE_OR_USER_VISIBLE_QA_INCOMPLETE','derived_classification':derived,'requested_classification':requested,'artifact_gate':detail}
    return {'status':'PASS','composer_admission':'ALLOWED','derived_classification':derived,'requested_classification':requested,'release_claim_allowed':derived=='RELEASED'}
