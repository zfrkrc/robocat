"""RoboCat concept-aligned printable prototypes, mm. CadQuery source.
Not a CAD reconstruction of the generated illustration. Original chassis unmodified.
"""
from pathlib import Path
import cadquery as cq,json
P=Path(__file__).parent;O=P/'stl';O.mkdir(exist_ok=True)
def box(x,y,z,a=0,b=0,c=0):return cq.Workplane('XY').box(x,y,z,centered=(True,True,False)).translate((a,b,c))
def rounded(x,y,z,r):return box(x,y,z).edges('|Z').fillet(r)
def drill(s,pts,d):
 for x,y in pts:s=s.cut(cq.Workplane('XY').center(x,y).circle(d/2).extrude(100).translate((0,0,-20)))
 return s
corners=[(-52,-33),(52,-33),(-52,33),(52,33)]
earscrews=[(x+dx,40) for x in [-39,39] for dx in [-7,7]]
f=rounded(118,90,3,10)
f=drill(f,corners+earscrews+[(-17,-16),(17,-16)],3.4)
f=drill(f,[(-30,12),(30,12)],20);f=drill(f,[(0,-16)],12)
for x in [-40,40]:
 for y in [-9,-17,-25]:f=f.cut(cq.Workplane('XY').center(x,y).slot2D(17,2.5).extrude(4))
# black shell, no front plate: white face closes front at z=0; back at z=40
s=rounded(118,90,37,10).cut(rounded(112,84,39,7).translate((0,0,-1)))
for x,y in corners:
 s=s.union(cq.Workplane('XY').center(x,y).circle(4).extrude(37))
 s=s.union(box(10,8,37,54 if x>0 else -54,y))
s=drill(s,corners,2.6)
# face-to-shell bolts and rear lid use same posts, screws must stop before opposite fastener
for x in [-34,34]:s=s.cut(box(14,8,4,x,-43,17))
lid=drill(rounded(118,90,3,10),corners,3.4)
for x in [-28,-14,0,14,28]:lid=lid.cut(cq.Workplane('XY').center(x,0).slot2D(26,3,90).extrude(4))
e=cq.Workplane('XY').polyline([(-17,0),(17,0),(3,43)]).close().extrude(4)
e=drill(e,[(-7,4),(7,4)],3.4)
inner=cq.Workplane('XY').polyline([(-10,12),(10,12),(2,33)]).close().extrude(1.2)
# 0.25 mm perimeter clearance pocket for decorative teal insert, glue after dry fit
pocket=cq.Workplane('XY').polyline([(-10.4,11.7),(10.4,11.7),(2,33.7)]).close().extrude(1.4)
e=e.cut(pocket)
ring=cq.Workplane('XY').circle(14).circle(10).extrude(3).edges('>Z').fillet(.6)
n=cq.Workplane('XY').polyline([(-16,10),(16,10),(0,-13)]).close().extrude(12)
n=n.cut(cq.Workplane('XY').polyline([(-11,7),(11,7),(0,-8)]).close().extrude(9))
n=n.union(box(42,7,3));n=n.cut(cq.Workplane('XY').circle(5).extrude(9));n=drill(n,[(-17,0),(17,0)],3.4)
for x,y in [(-6,5),(0,5),(6,5),(-3,0),(3,0),(0,-5)]:n=drill(n,[(x,y)],2.6)
# Camera back plate, board not included. Lens point is local (0,0).
c=box(34,44,2)
c=c.cut(box(23,29,4,0,0,-1))
for x in [-15,15]:
 for y in [-14,14]:c=c.cut(box(2.4,7,4,x,y,-1))
# shell bosses only at edges; board holder fastens to face via small corner posts and slots
# deliberate screw holes on camera carrier correspond to face pilot holes
campts=[(x+dx,12+dy) for x in [-30,30] for dx in [-13,13] for dy in [-18,18]]
f=drill(f,campts,2.6)
c=drill(c,[(dx,dy) for dx in [-13,13] for dy in [-18,18]],3.4)
# 4 mm printed standoffs, camera back plate at z=7.5 with 0.5 mm separation to standoffs
spacer=cq.Workplane('XY').circle(3).circle(1.7).extrude(4)
# bottom saddle for straps; no unverified stock hole pattern
saddle=box(100,40,4)
for x in [-34,34]:saddle=saddle.cut(box(14,4,6,x,0,-1))
saddle=saddle.union(box(100,3,10,0,-18.5,4)).union(box(100,3,10,0,18.5,4))
# decorative battery lid: same interface as previous cartridge, recessed accents never open cell chamber
bl=box(112,70,3)
bl=drill(bl,[(23,-25),(47,-25),(23,25),(47,25)],3.4)
for x in [-38,-24,-10,4]:
 for y in [-19,19]:bl=bl.cut(box(9,2,1,x,y,2))
# alignment coupon avoids printing full head before lens and M3 verification
coupon=box(88,29,2)
coupon=drill(coupon,[(-28,0)],18);coupon=drill(coupon,[(0,0)],20);coupon=drill(coupon,[(28,0)],22)
parts={
'CAT01_white_face_x1':(f,1,'white'),
'CAT02_dark_head_shell_x1':(s,1,'dark'),
'CAT03_dark_rear_lid_x1':(lid,1,'dark'),
'CAT04_white_ear_x2':(e,2,'white'),
'CAT05_teal_ear_insert_x2':(inner,2,'teal'),
'CAT06_dark_eye_bezel_x2':(ring,2,'dark'),
'CAT07_white_vented_nose_x1':(n,1,'white'),
'CAT08_camera_carrier_x2':(c,2,'dark'),
'CAT09_camera_spacer_x8':(spacer,8,'dark'),
'CAT10_strap_saddle_x1':(saddle,1,'dark'),
'BAT01_teal_cartridge_lid_x2':(bl,2,'teal'),
'TEST01_lens_coupon_x1':(coupon,1,'teal')}
report={};total=0
for name,(obj,q,col) in parts.items():
 assert obj.val().isValid() and len(obj.solids().vals())==1,name
 cq.exporters.export(obj,str(O/(name+'.stl')),tolerance=.12,angularTolerance=.2)
 cq.exporters.export(obj,str(O/(name+'.step')))
 b=obj.val().BoundingBox();vol=obj.val().Volume()/1000
 report[name]={'valid':True,'solids':1,'quantity':q,'color':col,'size_mm':[round(b.xlen,2),round(b.ylen,2),round(b.zlen,2)],'solid_volume_cm3':round(vol,2)}
 if name.startswith('CAT'):total+=vol*q
report['_head_material']={'solid_volume_cm3':round(total,1),'fully_solid_PETG_estimate_g':round(total*1.27,1),'note':'Not a slicer weight. Excludes screws, boards, lenses, straps and wiring.'}
(P/'validation.json').write_text(json.dumps(report,indent=2))
# assembled head only. Dummy lenses shown for context, not exported or physical boards.
assy=[('face',f,'white'),('shell',s.translate((0,0,3)),'dark'),('rear',lid.translate((0,0,40)),'dark')]
for x in [-39,39]:
 assy.append(('ear',e.translate((x,36,-4)),'white'))
 assy.append(('insert',inner.translate((x,36,-4)),'teal'))
for x in [-30,30]:
 assy.append(('ring',ring.translate((x,12,-3)),'dark'))
 assy.append(('lens',cq.Workplane('XY').circle(9).extrude(1).translate((x,12,-1)),'lens'))
 assy.append(('carrier',c.translate((x,12,7)),'dark'))
assy.append(('nose',n.rotate((0,0,0),(0,1,0),180).translate((0,-16,0)),'white'))
# collision report for intentional design geometry, no electronics/generic chassis simulated.
collisions=[]
for i,(a,sa,_) in enumerate(assy):
 for b,sb,_ in assy[i+1:]:
  # ears/decoration designed at interface; detect volumetric overlap for disclosure
  v=sa.intersect(sb).val()
  volume=0 if v is None else v.Volume()
  if volume>.1:collisions.append({'a':a,'b':b,'overlap_mm3':round(volume,2)})
(P/'assembly_check.json').write_text(json.dumps({'overlaps':collisions,'scope':'head printed parts + dummy lenses only; excludes fasteners, PCBs and chassis'},indent=2))
assembly=cq.Assembly()
colors={'white':(.86,.88,.86),'dark':(.12,.14,.15),'teal':(.1,.55,.6),'lens':(.01,.02,.03)}
for i,(name,shape,col) in enumerate(assy):assembly.add(shape,name=name+str(i),color=cq.Color(*colors[col]))
assembly.save(str(P/'head_assembly.step'))
import numpy as np,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(14,7))
for k,(elev,az,title) in enumerate([(-68,-90,'Front view — actual CAD'),(-35,-55,'Three-quarter view — actual CAD')]):
 ax=fig.add_subplot(1,2,k+1,projection='3d'); allfaces=[]; allcolors=[]
 for _,shape,col in assy:
  verts,tr=shape.val().tessellate(.4);v=np.array([z.toTuple() for z in verts]);p=v[np.array(tr)];norm=np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-9);light=.6+.4*np.abs(norm@np.array([.2,.4,.9]));fc=np.clip(light[:,None]*np.array(colors[col]),0,1)
  allfaces.extend(p); allcolors.extend(fc)
 ax.add_collection3d(Poly3DCollection(allfaces,facecolors=allcolors,edgecolor='none'))
 ax.set(xlim=(-80,80),ylim=(-60,100),zlim=(-65,95));ax.invert_yaxis();ax.view_init(elev,az);ax.set_axis_off();ax.set_title(title)
fig.suptitle('RoboCat v0.3 | ACTUAL CAD | FIT-TEST PROTOTYPE',fontsize=14)
plt.tight_layout(rect=[0,0,1,.93]);fig.savefig(P/'cad_head_v0.3.png',dpi=150)
print(json.dumps({'parts':len(parts),'head_solid_volume_cm3':round(total,1),'collisions':collisions}))
