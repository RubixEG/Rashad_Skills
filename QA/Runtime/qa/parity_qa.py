#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib,shutil,subprocess,tempfile,time
from pathlib import Path
from PIL import Image,ImageChops,ImageStat

def rasterize(p,work,dpi=180):
 p=Path(p);work.mkdir(parents=True,exist_ok=True)
 if p.is_dir():return sorted([x for x in p.iterdir() if x.suffix.lower() in ('.png','.jpg','.jpeg','.webp')])
 if p.suffix.lower() in ('.png','.jpg','.jpeg','.webp'):return [p]
 if p.suffix.lower()=='.pdf':subprocess.run(['pdftoppm','-png','-r',str(dpi),str(p),str(work/'page')],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);return sorted(work.glob('page-*.png'))
 if p.suffix.lower()=='.pptx':
  lo=shutil.which('libreoffice') or shutil.which('soffice');subprocess.run([lo,'--headless','--convert-to','pdf','--outdir',str(work),str(p)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);return rasterize(work/(p.stem+'.pdf'),work/'pptx_pdf',dpi)
 raise RuntimeError('unsupported '+p.suffix)

def cmp(a,b,meanmax,ratio,pdelta):
 ia=Image.open(a).convert('RGB');ib=Image.open(b).convert('RGB');orig=ib.size
 if ia.size!=ib.size:ib=ib.resize(ia.size,Image.Resampling.LANCZOS)
 d=ImageChops.difference(ia,ib);st=ImageStat.Stat(d);mean=sum(st.mean)/3;px=d.getdata();chg=sum(1 for r,g,b in px if max(r,g,b)>pdelta);rr=chg/max(1,ia.width*ia.height)
 return {'reference':str(a),'candidate':str(b),'reference_size':ia.size,'candidate_original_size':orig,'mean_abs_diff':round(mean,4),'pixel_diff_ratio':round(rr,6),'pass':mean<=meanmax and rr<=ratio}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--reference',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--format-name',default='OUTPUT');ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mean-max',type=float,default=5.0);ap.add_argument('--pixel-ratio-max',type=float,default=.025);ap.add_argument('--pixel-delta',type=int,default=20);ap.add_argument('--min-master-width',type=int,default=3840);ap.add_argument('--min-master-height',type=int,default=2160);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);ts=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());eid='PAR-'+hashlib.sha256((str(a.reference)+str(a.candidate)+ts).encode()).hexdigest()[:16].upper()
 try:
  with tempfile.TemporaryDirectory() as td:
   td=Path(td);refs=rasterize(a.reference,td/'r');cands=rasterize(a.candidate,td/'c')
   if len(refs)!=len(cands):raise RuntimeError(f'page count mismatch {len(refs)} != {len(cands)}')
   # reference directory is authoritative master; require high resolution
   low=[]
   if a.reference.is_dir():
    for r in refs:
     sz=Image.open(r).size
     if sz[0]<a.min_master_width or sz[1]<a.min_master_height:low.append({'file':str(r),'size':sz})
   pages=[cmp(r,c,a.mean_max,a.pixel_ratio_max,a.pixel_delta) for r,c in zip(refs,cands)];ok=not low and all(x['pass'] for x in pages)
  report={'evidence_id':eid,'status':'PASS' if ok else 'FAIL','verdict':a.format_name.upper()+'_PARITY_PASS' if ok else 'BLOCKED','low_resolution_masters':low,'pages':pages}
 except Exception as e:report={'evidence_id':eid,'status':'NOT_EXECUTED','verdict':'BLOCKED','runtime_error':str(e),'pages':[]}
 ev=a.out/eid;ev.mkdir();(ev/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));return 0 if report['verdict'].endswith('_PARITY_PASS') else 1
if __name__=='__main__':raise SystemExit(main())
