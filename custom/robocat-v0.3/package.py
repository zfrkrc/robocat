from pathlib import Path
import shutil,csv,json,zipfile,hashlib
R=Path(__file__).resolve().parents[2];P=R.parent/'RoboCat_PrintPack_v0.3';P.mkdir(exist_ok=True)
rows=[]
for f in sorted((R/'Nova-SM3/STL Files/SM3 Files').glob('*.stl')):
 n=f.name
 stage='01_Original_Frame' if 'Frame_' in n or n=='SM3_Foot.stl' else '02_Original_Covers' if 'Cover_' in n else '03_Original_Accessories'
 dst=P/stage;dst.mkdir(exist_ok=True);shutil.copy2(f,dst/n)
 q=2 if any(k in n for k in ['LeftCoax','RightCoax','LeftFemur','RightFemur','LeftTibia','RightTibia']) else 4 if n=='SM3_Foot.stl' else 1
 rows.append([stage,n,q,'ORIGINAL quantities provisional; dry fit required',hashlib.sha256(f.read_bytes()).hexdigest()])
for f in (R/'custom/robocat-v0.3/stl').glob('*'):
 dst=P/'04_RoboCat_Head_v0.3';dst.mkdir(exist_ok=True);shutil.copy2(f,dst/f.name)
 if f.suffix=='.stl':rows.append(['04_RoboCat_Head_v0.3',f.name,int(f.stem.rsplit('_x',1)[1]),'CAD prototype',hashlib.sha256(f.read_bytes()).hexdigest()])
for f in (R/'custom/zk-v0.1/stl').glob('*.stl'):
 if f.name.startswith(('03_','04_','06_')):
  dst=P/'05_Older_FitTest_Accessories';dst.mkdir(exist_ok=True);shutil.copy2(f,dst/f.name)
for f in (R/'Nova-SM3/Remote Control/STL Files').glob('*.stl'):
 dst=P/'06_Optional_Remote';dst.mkdir(exist_ok=True);shutil.copy2(f,dst/f.name)
for n in ['README.md','generate.py','package.py','validation.json','assembly_check.json','cad_head_v0.3.png','head_assembly.step']:
 shutil.copy2(R/'custom/robocat-v0.3'/n,P/n)
shutil.copy2(R/'LICENSE',P/'LICENSE_original_MIT.txt')
shutil.copy2(R/'Nova-SM3/README.md',P/'Nova_SM3_original_README.md')
shutil.copy2(R/'docs/images/robocat-concept-v0.3.png',P/'CONCEPT_NOT_CAD.png')
with (P/'PRINT_LIST.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['folder','file','quantity','status','sha256']);w.writerows(rows)
(P/'START_HERE.txt').write_text('ROBOCAT v0.3\nRead README.md before printing. First print TEST01 and one carrier/ear to verify actual hardware. Original servo fit and quantities remain unverified. Do not print all accessory alternatives. No completed robotic arm or live battery electrical assembly is included. CONCEPT_NOT_CAD.png is an illustration; cad_head_v0.3.png shows actual new geometry. Older v0.1/v0.2 head parts are superseded; do not mix their hole patterns with v0.3.\n')
z=R.parent/'RoboCat_PrintPack_v0.3.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for f in P.rglob('*'):
  if f.is_file():a.write(f,'RoboCat_PrintPack_v0.3/'+str(f.relative_to(P)))
print(json.dumps({'zip':str(z),'bytes':z.stat().st_size,'stl_count':len(list(P.rglob('*.stl')))}))
