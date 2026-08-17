from __future__ import annotations
from pathlib import Path
import hashlib
from PIL import Image,ImageDraw


def _hash(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def _txt(d,xy,text,fill='black'):
    d.text(xy,str(text)[:72],fill=fill)

def _box(d,b,w=3): d.rounded_rectangle(b,16,outline='black',width=w)

def render_low_fidelity_candidates(hypotheses,out_dir,size=(1280,720)):
    """Concept-fidelity search renders.

    These are not final consulting pages. They intentionally render materially
    different communication strategies so actual search evidence cannot collapse
    back into five reusable geometric skeletons.
    """
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True); results=[]
    for h in hypotheses:
        im=Image.new('RGB',size,'white'); d=ImageDraw.Draw(im); w,hh=size
        st=h.get('communication_strategy','STATEMENT_LED'); fp=h.get('page_fingerprint','PAGE')
        _txt(d,(35,25),f"{h.get('id')} | {st} | {fp}")
        _txt(d,(35,55),h.get('visual_thesis','') or h.get('communication_intent',''))
        top=105; left=70; right=w-70; bottom=hh-70
        if st=='STATEMENT_LED':
            d.line((left,top,right,top),fill='black',width=2); _box(d,(270,220,1010,470),4); _txt(d,(320,300),'ONE ANSWER / SO WHAT'); _txt(d,(320,370),'2–3 proof points only')
        elif st=='NUMBER_LED':
            _box(d,(120,180,610,550),4); _txt(d,(280,290),'87.5%'); _txt(d,(240,380),'DECISIVE METRIC'); _box(d,(700,220,1140,500),2); _txt(d,(760,300),'IMPLICATION'); _txt(d,(760,360),'WHAT CHANGES THE DECISION')
        elif st in {'TABLE_LED','EVIDENCE_LED'}:
            _box(d,(90,145,1190,590),3)
            for y in range(220,590,90): d.line((90,y,1190,y),fill='black',width=1)
            for x in (430,760,980): d.line((x,145,x,590),fill='black',width=1)
            _txt(d,(120,165),'ISSUE / CLAIM'); _txt(d,(470,165),'EVIDENCE'); _txt(d,(800,165),'IMPLICATION'); _txt(d,(1000,165),'ACTION')
        elif st in {'COMPARISON_LED','BEFORE_AFTER','TRADEOFF_LED'}:
            _box(d,(100,160,585,560),3); _box(d,(695,160,1180,560),3); d.line((640,150,640,575),fill='black',width=2)
            _txt(d,(250,205),'A'); _txt(d,(850,205),'B'); _txt(d,(190,300),'TRADE-OFF / CURRENT'); _txt(d,(790,300),'CONSEQUENCE / FUTURE')
        elif st=='MATRIX_LED':
            d.line((250,560,1100,560),fill='black',width=3); d.line((250,560,250,150),fill='black',width=3); d.line((675,150,675,560),fill='black',width=1); d.line((250,355,1100,355),fill='black',width=1)
            _txt(d,(760,210),'HIGH IMPACT'); _txt(d,(330,430),'LOWER PRIORITY')
        elif st in {'DECISION_LED','CONTROL_TOWER_LED'}:
            _box(d,(90,150,470,570),4); _txt(d,(200,245),'DECISION'); _txt(d,(205,325),'HOLD / GO');
            for i,y in enumerate((165,265,365,465)):
                _box(d,(560,y,1160,y+70),2); _txt(d,(600,y+22),f'GATE {i+1}  STATUS  →  ACTION')
        elif st in {'SEQUENCE_LED','PROCESS_LED','JOURNEY_LED'}:
            y=360; d.line((120,y,1160,y),fill='black',width=4)
            for i,x in enumerate((180,410,640,870,1100)):
                _box(d,(x-75,y-60,x+75,y+60),3); _txt(d,(x-45,y-10),f'STEP {i+1}')
        elif st in {'SYSTEM_LED','ARCHITECTURE_LED'}:
            for i,(y0,y1,label) in enumerate([(150,240,'OUTCOMES / EXPERIENCE'),(270,370,'PLATFORM / PROCESS'),(400,500,'DATA / AI / INTEGRATION'),(530,610,'SECURITY / INFRA / CONTROL')]):
                _box(d,(120,y0,1160,y1),3 if i==1 else 2); _txt(d,(170,y0+28),label)
            d.line((640,240,640,530),fill='black',width=3)
        elif st=='CHART_LED':
            d.line((150,560,1150,560),fill='black',width=3); d.line((150,560,150,160),fill='black',width=3)
            bars=[250,420,610,820,1010]
            heights=[120,260,180,330,230]
            for x,ht in zip(bars,heights): d.rectangle((x,560-ht,x+90,560),outline='black',width=3)
        elif st=='IMAGE_LED':
            _box(d,(90,145,700,590),2); _txt(d,(280,350),'HERO IMAGE / VISUAL METAPHOR'); _box(d,(760,210,1170,500),3); _txt(d,(820,275),'ONE THESIS'); _txt(d,(820,345),'MINIMAL SUPPORT')
        elif st in {'CAUSE_EFFECT'}:
            pts=[(170,330),(420,220),(660,360),(900,230),(1110,350)]
            for i,(x,y) in enumerate(pts): _box(d,(x-75,y-45,x+75,y+45),3); _txt(d,(x-40,y-8),f'C{i+1}')
            for a,b in zip(pts,pts[1:]): d.line((a[0]+75,a[1],b[0]-75,b[1]),fill='black',width=3)
        else:  # HYBRID / portfolio / question and future strategies
            _box(d,(90,155,470,565),4); _txt(d,(160,270),'PRIMARY ANSWER'); _txt(d,(160,340),'METRIC / PROOF')
            _box(d,(540,155,1180,340),2); _box(d,(540,380,1180,565),2); _txt(d,(620,220),'ANALYTICAL SUPPORT'); _txt(d,(620,445),'RELATIONSHIP / ACTION')
        p=out/f"{h.get('id','HX')}_{st}.png"; im.save(p)
        results.append({'candidate_id':h.get('id'),'communication_strategy':st,'strategy_family':h.get('strategy_family'),'page_fingerprint':fp,'render_path':str(p),'actual_render_hash':_hash(p),'width':w,'height':hh,'render_kind':'COMMUNICATION_STRATEGY_CONCEPT_RENDER_V3'})
    return results
