from pathlib import Path
import json,hashlib,zipfile
P=Path(__file__).parent;R=P.parents[1]
# User-supplied template is input only; never modify original bundle.
u=R.parent/'upload/Creality Creality Ender-3 V2 0.4 nozzle.orca_printer'
if u.exists():
 with zipfile.ZipFile(u) as z:
  name=next(n for n in z.namelist() if n.startswith('process/') and n.endswith('.json'));cfg=json.loads(z.read(name))
 cfg.update({'name':'RoboCat PETG Fit Candidate 0.20','print_settings_id':'RoboCat PETG Fit Candidate 0.20','layer_height':'0.2','initial_layer_print_height':'0.2','wall_loops':'4','sparse_infill_density':'25%','sparse_infill_pattern':'gyroid','top_shell_layers':'5','bottom_shell_layers':'5','initial_layer_speed':'20','initial_layer_infill_speed':'20','outer_wall_speed':'30','inner_wall_speed':'45','sparse_infill_speed':'50','internal_solid_infill_speed':'40','top_surface_speed':'30','gap_infill_speed':'35','bridge_speed':'20','support_speed':'40','support_interface_speed':'30','travel_speed':'100','default_acceleration':'500','outer_wall_acceleration':'300','inner_wall_acceleration':'500','initial_layer_acceleration':'300','travel_acceleration':'500','top_surface_acceleration':'300','enable_prime_tower':'0','enable_support':'0','enable_arc_fitting':'0','initial_layer_line_width':'0.42','line_width':'0.42','outer_wall_line_width':'0.42','inner_wall_line_width':'0.42','default_jerk':'0','initial_layer_jerk':'0','outer_wall_jerk':'0','inner_wall_jerk':'0','infill_jerk':'0','top_surface_jerk':'0','travel_jerk':'0','notes':'CANDIDATE ONLY. No temperatures set. Verify physical machine and filament. Preview and explicit user print command required.'})
 (P/'Orca_RoboCat_PETG_Fit_Candidate.json').write_text(json.dumps(cfg,indent=2))
spec=[('M01','custom/robocat-v0.3/stl/TEST01_lens_coupon_x1.stl'),('M02','custom/petg-stage-v0.5/stl/CAT06B_eye_bezel_7x7_boss_x2.stl'),('M03','custom/robocat-v0.3/stl/CAT08_camera_carrier_x2.stl'),('M04','custom/robocat-v0.3/stl/CAT09_camera_spacer_x8.stl'),('M05','custom/robocat-v0.3/stl/CAT05_teal_ear_insert_x2.stl'),('M06','custom/robocat-v0.3/stl/CAT03_dark_rear_lid_x1.stl')]
jobs=[]
for id,f in spec:
 jobs.append({'id':id,'file':f,'quantity':1,'sha256':hashlib.sha256((R/f).read_bytes()).hexdigest(),'material':'PETG','color':'metallic','status':'PREPARED_NOT_SLICED','orientation':'source XY on bed; minZ=0; M02 front face down and boss up','auto_start':False,'skip_if_already_printed':True,'requires_preview':True,'requires_previous_fit_pass':id!='M01'})
m={'schema':'robocat.proposed.print_jobs.v1','revision':'0.5-metallic','auto_start':False,'state':'WAITING_FOR_FILAMENT_AND_EXPLICIT_USER_PRINT_COMMAND','printer_integration_verified':False,'machine_profile_verified':False,'process_profile_verified_in_slicer':False,'filament_temperature_verified':False,'nozzle_temperature_c':None,'bed_temperature_c':None,'gcode_included':False,'notes':'Proposed contract only; does not enforce behavior in external automation. No automatic printing. One part per job, stop if prior fit fails.','jobs':jobs}
(P/'metallic_queue.json').write_text(json.dumps(m,indent=2))
# Verify exported STL is one closed connected mesh, not three overlapping shells.
import struct,numpy as np
b=(R/spec[1][1]).read_bytes();tri=np.frombuffer(b[84:],dtype=np.dtype([('n','<f4',3),('v','<f4',(3,3)),('att','<u2')]))['v'];v=tri.reshape(-1,3);vs,inv=np.unique(np.round(v,5),axis=0,return_inverse=True);t=inv.reshape(-1,3);edges=np.concatenate([t[:,[0,1]],t[:,[1,2]],t[:,[2,0]]]);edges.sort(axis=1);_,counts=np.unique(edges,axis=0,return_counts=True);assert np.all(counts==2)
p=list(range(len(vs)))
def root(x):
 while p[x]!=x:p[x]=p[p[x]];x=p[x]
 return x
for tr in t:
 for x in tr[1:]:p[root(int(x))]=root(int(tr[0]))
assert len({root(i) for i in range(len(vs))})==1
assert abs(float(v[:,2].min()))<1e-5
print('6 metallic jobs prepared; STL connected=1 and closed; auto_start=false; no G-code.')
