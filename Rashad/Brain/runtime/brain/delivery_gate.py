from __future__ import annotations
from pathlib import Path
import hashlib
from brain.actual_output_qa import evaluate_deck_output
from brain.product_inspector import inspect_pptx, sha256_file
from brain.execution_proof import validate_brain_execution_proof, validate_expert_execution_ledger, validate_artifact_execution_ledger
from brain.exact_handoff import verify_exact_artifact_handoff, issue_exact_handoff_certificate

USER_VISIBLE_LEVELS={'USER_VISIBLE_ARTIFACT_DRAFT','RELEASE_CANDIDATE','RELEASED'}


def validate_user_visible_delivery(dossier, pptx_path, requested='USER_VISIBLE_ARTIFACT_DRAFT'):
    blockers=[]
    if requested not in USER_VISIBLE_LEVELS: blockers.append('INVALID_USER_VISIBLE_CLASSIFICATION')
    p=Path(pptx_path)
    if not p.exists(): blockers.append('OUTPUT_PPTX_NOT_FOUND'); return {'status':'BLOCK_DELIVERY','blockers':blockers}
    deck_hash=sha256_file(p)
    if dossier.get('output_file_sha256')!=deck_hash: blockers.append('DOSSIER_OUTPUT_FILE_HASH_MISMATCH')
    if dossier.get('classification')!=requested: blockers.append('DOSSIER_CLASSIFICATION_MISMATCH')
    if dossier.get('artifact_brain_execution_status')!='PASS': blockers.append('ARTIFACT_BRAIN_EXECUTION_NOT_PROVEN')
    dce=dossier.get('deck_artifact_council_execution') or {}
    if dce.get('status')!='PASS': blockers.append('DECK_ARTIFACT_COUNCIL_EXECUTION_NOT_PROVEN')
    if dossier.get('production_render_status')!='PASS': blockers.append('PRODUCTION_RENDER_NOT_PROVEN')
    if dossier.get('actual_output_qa_closed_loop_status')!='PASS': blockers.append('ACTUAL_OUTPUT_QA_CLOSED_LOOP_NOT_PROVEN')
    if 'deck_continuity_qa' in dossier and (dossier.get('deck_continuity_qa') or {}).get('status')!='PASS': blockers.append('DECK_CONTINUITY_QA_NOT_PASSED')
    if dossier.get('framework_certification_substitute') is True: blockers.append('FRAMEWORK_CERTIFICATION_CANNOT_SUBSTITUTE_OUTPUT_QA')
    pages=dossier.get('pages') or []
    for pg in pages:
        prefix=str(pg.get('page_id','PAGE'))+'::'
        if validate_brain_execution_proof(pg.get('brain_session_execution_evidence') or {}).get('status')!='PASS': blockers.append(prefix+'BRAIN_EXECUTION_PROOF_INVALID')
        if validate_expert_execution_ledger(pg.get('expert_execution_ledger') or {}).get('status')!='PASS': blockers.append(prefix+'EXPERT_EXECUTION_LEDGER_INVALID')
        if validate_artifact_execution_ledger(pg.get('artifact_council_execution') or {},'PRE_CONCEPT').get('status')!='PASS': blockers.append(prefix+'ARTIFACT_COUNCIL_LEDGER_INVALID')
        if validate_artifact_execution_ledger(pg.get('art_direction_execution') or {},'ART_DIRECTION').get('status')!='PASS': blockers.append(prefix+'ART_DIRECTION_LEDGER_INVALID')
        if validate_artifact_execution_ledger(pg.get('production_council_execution') or {},'PRODUCTION_READINESS').get('status')!='PASS': blockers.append(prefix+'PRODUCTION_COUNCIL_LEDGER_INVALID')
        if pg.get('brain_cognitive_lock_status')!='PASS': blockers.append(prefix+'BRAIN_COGNITIVE_LOCK_NOT_PROVEN')
        if pg.get('expert_execution_status')!='PASS': blockers.append(str(pg.get('page_id','PAGE'))+'::EXECUTABLE_SME_COUNCIL_NOT_PROVEN')
        if pg.get('artifact_council_execution_status')!='PASS': blockers.append(str(pg.get('page_id','PAGE'))+'::ARTIFACT_COUNCIL_EXECUTION_NOT_PROVEN')
        if pg.get('art_direction_execution_status')!='PASS': blockers.append(str(pg.get('page_id','PAGE'))+'::ART_DIRECTION_EXECUTION_NOT_PROVEN')
        if pg.get('production_council_execution_status')!='PASS': blockers.append(str(pg.get('page_id','PAGE'))+'::PRODUCTION_COUNCIL_EXECUTION_NOT_PROVEN')
        try:
            at=float(pg.get('artifact_truth_score',(pg.get('actual_pixel_review') or {}).get('artifact_truth_score',0)) or 0)
            ce=float(pg.get('ceqs_score',(pg.get('actual_pixel_review') or {}).get('ceqs_score',(pg.get('actual_pixel_review') or {}).get('ceqs',0))) or 0)
        except Exception:
            at=ce=0
        if at < 90: blockers.append(prefix+'ARTIFACT_TRUTH_BELOW_90')
        if ce < 90: blockers.append(prefix+'CEQS_BELOW_90')
        sm=pg.get('semantic_master_qa') or {}
        if sm.get('status')!='PASS' or not pg.get('html_master_sha256') or not pg.get('composition_spec_sha256'):
            blockers.append(prefix+'SEMANTIC_MASTER_PROOF_NOT_PASS')
        material=pg.get('material_claim_ids') or []; bindings=pg.get('claim_visual_bindings') or []
        by={x.get('claim_id'):x for x in bindings if isinstance(x,dict)}
        missing=[cid for cid in material if not (by.get(cid,{}).get('evidence_refs') and by.get(cid,{}).get('visual_node_ids'))]
        if missing: blockers.append(str(pg.get('page_id','PAGE'))+'::CLAIM_EVIDENCE_VISUAL_BINDING_INCOMPLETE')
    product=inspect_pptx(p,pages)
    deckqa=evaluate_deck_output(
        pages, visibility=requested, deck_review=dossier.get('deck_pixel_review'),
        deck_sha256=deck_hash, montage_sha256=dossier.get('montage_sha256'), product_inspection=product
    )
    blockers.extend(deckqa.get('blockers',[]))
    if requested in {'RELEASE_CANDIDATE','RELEASED'}:
        if dossier.get('independent_judgment_status')!='PASS': blockers.append('INDEPENDENT_JUDGMENT_REQUIRED')
        if dossier.get('parity_status')!='PASS': blockers.append('PDF_PPTX_PARITY_REQUIRED')
        if dossier.get('proof_index_status')!='PASS': blockers.append('PROOF_INDEX_REQUIRED')
    if requested=='RELEASED':
        rel=dossier.get('release') or {}
        if rel.get('release_authority')!='RASHAD_BRAIN_RELEASE_CHAIR' or rel.get('release_chair_status')!='RELEASED': blockers.append('RELEASE_CHAIR_PROOF_REQUIRED')
    exact=verify_exact_artifact_handoff(p,dossier)
    if exact.get('status')!='HANDOFF_ALLOWED': blockers.extend('EXACT_HANDOFF::'+x for x in exact.get('blockers',[]))
    cert=issue_exact_handoff_certificate(p,dossier) if not blockers else {'status':'BLOCK_HANDOFF','blockers':sorted(set(blockers))}
    return {'status':'DELIVERY_ALLOWED' if not blockers else 'BLOCK_DELIVERY','blockers':sorted(set(blockers)),'deck_sha256':deck_hash,'product_inspection':product,'actual_output_qa':deckqa,'exact_handoff_verification':exact,'handoff_certificate':cert,'requested':requested}
