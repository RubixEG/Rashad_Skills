from __future__ import annotations

GRAMMARS=[
 {'id':'CRG-01','families':['ANALYTICAL','DECISION'],'strategies':['STATEMENT_LED','DECISION_LED'],'principles':['answer first','one dominant decision artifact','implication rail','avoid equal-card democracy']},
 {'id':'CRG-04','families':['ARCHITECTURE','ANALYTICAL'],'strategies':['SYSTEM_LED','ARCHITECTURE_LED'],'principles':['workstream operating system','dependencies visible','acceptance outputs','few semantic layers']},
 {'id':'CRG-05','families':['SEQUENCE'],'strategies':['SEQUENCE_LED','JOURNEY_LED','PROCESS_LED'],'principles':['phase gates','governance','feedback closure','measured transitions']},
 {'id':'CRG-08','families':['ARCHITECTURE'],'strategies':['ARCHITECTURE_LED','SYSTEM_LED'],'principles':['technical/data/integration layers','directional islands','interfaces explicit']},
 {'id':'CRG-15','families':['ANALYTICAL','DECISION'],'strategies':['MATRIX_LED','SCORECARD_LED'],'principles':['risk prioritisation','response ownership','residual exposure']},
 {'id':'CRG-20','families':['DECISION'],'strategies':['DECISION_LED','CONTROL_TOWER_LED'],'principles':['conditions','exposures','actions','management decision visible first']},
 {'id':'MWAN-HERO','families':['COVER','SECTION_OPENER'],'strategies':['IMAGE_LED'],'principles':['full-page high-key institutional visual','physical left visual scene','physical right clean title space','co-brand single baseline','native authoritative overlays','restrained magenta accent']},
 {'id':'MWAN-ART-DIRECTED-GRID','families':['ANALYTICAL'],'strategies':['TABLE_LED','EVIDENCE_LED','COMPARISON_LED','NUMBER_LED'],'principles':['one dominant mass','asymmetric hierarchy','intentional negative space','cards are supporting surfaces not page grammar','meaningful density']},
]

def retrieve(page_family,strategy,limit=4):
    scored=[]
    for g in GRAMMARS:
        sc=(3 if page_family in g['families'] else 0)+(3 if strategy in g['strategies'] else 0)
        if page_family in ('COVER','SECTION_OPENER') and g['id']=='MWAN-HERO': sc+=5
        if page_family=='ANALYTICAL' and g['id']=='MWAN-ART-DIRECTED-GRID': sc+=2
        scored.append((sc,g))
    return [g for sc,g in sorted(scored,key=lambda x:(-x[0],x[1]['id'])) if sc>0][:limit] or [GRAMMARS[0]]
