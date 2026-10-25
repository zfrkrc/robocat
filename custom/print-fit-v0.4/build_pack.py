from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[2];P=Path(__file__).parent
specs=[('T01','TEST01_lens_coupon_x1',False),('T02','CAT08_camera_carrier_x2',False),('T03','CAT04_white_ear_x2',False),('T04','CAT05_teal_ear_insert_x2',False),('P1_FACE','CAT01_white_face_x1',True),('P1_CASE','CAT02_dark_head_shell_x1',True),('P2_LID','CAT03_dark_rear_lid_x1',False)]
jobs=[]
for id,name,already in specs:
 f=R/'custom/robocat-v0.3/stl'/(name+'.stl')
 jobs.append({'id':id,'file':str(f.relative_to(R)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'quantity':1,'status':'FIT_TEST_ONLY','already_reported_printing':already,'skip_if_already_printed':True,'orientation':'Source XY plane on bed; min Z=0','support':'LOCAL_REVIEW_AT_TWO_14MM_WINDOWS' if id=='P1_CASE' else 'NO_GENERAL_SUPPORT_EXPECTED_IN_SPECIFIED_ORIENTATION','requires_preview':True,'auto_start':False})
f=P/'BAT_TEST_3S_2200_TRAY_x1.stl'
jobs.append({'id':'T05_BATTERY','file':str(f.relative_to(R)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'quantity':1,'status':'EMPTY_DUMMY_FIT_TEST_ONLY','orientation':'Closed base down; open chamber up','support':'NO_GENERAL_SUPPORT_EXPECTED_IN_SPECIFIED_ORIENTATION','requires_preview':True,'auto_start':False})
manifest={'schema':'robocat.proposed.print_jobs.v1','revision':'0.4','auto_start':False,'machine_profile_verified':False,'filament_verified':False,'sliced_gcode_included':False,'warning':'This is a proposed manifest, not a verified integration with the printer automation. File discovery must not override blocked parts.','blocked_parts':[{'file':'CAT10_strap_saddle_x1','reason':'34mm channel and unverified chassis/head interface'},{'file':'04_3s_cassette_body_x2','reason':'Obsolete 18650 geometry, not chosen LiPo'},{'file':'05_3s_cassette_lid_x2','reason':'Obsolete 18650 geometry'},{'file':'06_strap_dock_x2','reason':'Obsolete 18650 geometry'},{'file':'BAT01_teal_cartridge_lid_x2','reason':'Obsolete 18650 geometry'},{'file':'03_shoulder_ultrasonic_x2','reason':'Chassis mounting not verified'}],'jobs':jobs}
(P/'print_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
z=R.parent/'RoboCat_FitTest_v0.4.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for j in jobs:
  f=R/j['file'];a.write(f,'RoboCat_FitTest_v0.4/'+j['file'])
 for f in P.iterdir():
  if f.is_file() and str(f.relative_to(R)) not in {j['file'] for j in jobs}:a.write(f,'RoboCat_FitTest_v0.4/custom/print-fit-v0.4/'+f.name)
 a.write(R/'LICENSE','RoboCat_FitTest_v0.4/LICENSE')
assert len({j['id'] for j in jobs})==len(jobs)
assert all(j['quantity']==1 and j['auto_start'] is False for j in jobs)
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None
 for j in jobs:
  b=a.read('RoboCat_FitTest_v0.4/'+j['file'])
  assert hashlib.sha256(b).hexdigest()==j['sha256']
print(json.dumps({'pack':str(z),'jobs':len(jobs),'verified_hashes':True,'blocked_part_count':len(manifest['blocked_parts'])}))
