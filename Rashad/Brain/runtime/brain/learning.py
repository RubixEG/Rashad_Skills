from __future__ import annotations
from .utils import new_id

def propose_regression(defect):
    # Failures can create regression proposals, never silently mutate protected Skill authorities.
    required=['description','evidence','severity']
    missing=[x for x in required if not defect.get(x)]
    if missing: return {'status':'BLOCKED','reason':'INCOMPLETE_DEFECT','missing':missing}
    return {'status':'PENDING_OWNER_REVIEW','proposal_id':new_id('REG'),'defect':defect,'actions':['ADD_FIXTURE','ADD_DETECTOR_OR_DECLARE_RUNTIME_REQUIRED','ADD_REPAIR_POLICY','RUN_NON_REGRESSION'],'protected_authority_mutation':'FORBIDDEN_WITHOUT_EXPLICIT_APPROVAL'}
