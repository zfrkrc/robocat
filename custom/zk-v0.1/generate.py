"""Parametric mechanical mock-up; millimetres. Requires cadquery, matplotlib.
No electrical contacts, wiring, latch qualification or OEM mating geometry implied.
"""
from pathlib import Path
import cadquery as cq
import json
P=Path(__file__).parent
OUT=P/'stl'; OUT.mkdir(exist_ok=True)
parts={}
def box(x,y,z,a=0,b=0,c=0):
 return cq.Workplane('XY').box(x,y,z,centered=(True,True,False)).translate((a,b,c))
def holes(s,pts,d,h=100):
 for x,y in pts:s=s.cut(cq.Workplane('XY').center(x,y).circle(d/2).extrude(h).translate((0,0,-10)))
 return s
# Fixed face plate: lens apertures are generous, boards independently held behind.
f=box(120,60,3)
for x in [-32,32]:
 f=f.cut(cq.Workplane('XY').center(x,6).circle(10).extrude(5))
 # pair of vertical adjustment slots for each board cradle
 for dx in [-13,13]:
  f=f.cut(cq.Workplane('XY').center(x+dx,0).slot2D(14,3.4,90).extrude(5))
f=holes(f,[(-54,-24),(54,-24),(-54,24),(54,24)],3.4)
# smile cutout
f=f.cut(cq.Workplane('XY').center(0,-17).slot2D(36,4).extrude(5))
parts['01_fixed_face_x1']=f
# 29 x 42 clear space; open top/back enables ribbon and antenna access
c=box(35,48,2)
c=c.union(box(3,48,9,-16,0,2)).union(box(3,48,9,16,0,2))
c=c.union(box(29,3,5,0,-22.5,2))
c=c.cut(box(22,32,5,0,2,-1))
c=holes(c,[(-13,-19),(13,-19)],3.4)
parts['02_camera_cradle_x3']=c
# HC-SR04 nominal board pocket, retention by removable bridge/zip ties
s=box(54,32,3)
for x in [-13,13]:s=s.cut(cq.Workplane('XY').center(x,0).circle(8.5).extrude(5))
for x in [-24,24]:s=s.cut(cq.Workplane('XY').center(x,0).slot2D(12,3.4,90).extrude(5))
# bracket foot; no unsupported moving servo mounting
s=s.union(box(54,3,21,0,-14.5,3)).union(box(54,22,3,0,-24,0))
s=holes(s,[(-18,-27),(18,-27)],3.4)
parts['03_shoulder_ultrasonic_x2']=s
# Battery cassette holds cells aligned along X, electronics compartment at X positive.
# EXTERNAL 112 x 70 x 27. cell chamber 70 x 64 x 24, electronics 33 x 64.
b=box(112,70,27)
b=b.cut(box(70,64,27,-18,0,3)).cut(box(33,64,27,35.5,0,3))
# low separators establish 3 lanes of 20.5 mm; not spring contact mounts
for y in [-10.5,10.5]: b=b.union(box(70,1.5,5,-18,y,3))
# lid screw bosses in electronics compartment, cable passage in divider
for x,y in [(23,-25),(47,-25),(23,25),(47,25)]:
 b=b.union(cq.Workplane('XY').center(x,y).circle(4).extrude(27))
b=b.cut(box(5,12,7,18,0,20))
b=holes(b,[(23,-25),(47,-25),(23,25),(47,25)],2.6)
# exterior connector pilot intentionally omitted until hardware known
parts['04_3s_cassette_body_x2']=b
l=box(112,70,3)
l=holes(l,[(23,-25),(47,-25),(23,25),(47,25)],3.4)
# finger texture, no cell access holes
for x in [-35,-25,-15]:l=l.union(box(2,35,0.8,x,0,3))
parts['05_3s_cassette_lid_x2']=l
# dock: clearance around cassette; strap locking, no fragile printed latch claim
d=box(118,76,3)
d=d.union(box(118,2.5,10,0,-36.75,3)).union(box(118,2.5,10,0,36.75,3))
d=d.union(box(2.5,71,10,-57.75,0,3))
for x in [-38,38]:
 for y in [-27,27]:d=d.cut(box(5,12,5,x,y,-1))
d=holes(d,[(-45,0),(0,0),(45,0)],3.4)
parts['06_strap_dock_x2']=d
# Generic right-angle adapter for face mounting; body drilling coordinates unverified
a=box(30,25,3).union(box(30,3,28,0,11,3))
a=holes(a,[(-9,-5),(9,-5)],3.4)
for x in [-9,9]:
 tool=cq.Workplane('XZ').center(x,19).slot2D(12,3.4,90).extrude(50,both=True)
 a=a.cut(tool)
parts['07_face_angle_adapter_x2']=a
report={}
for name,shape in parts.items():
 solid=shape.val()
 if not solid.isValid() or len(shape.solids().vals())!=1:raise RuntimeError(name+' invalid/disconnected')
 cq.exporters.export(shape,str(OUT/(name+'.stl')),tolerance=0.08,angularTolerance=0.15)
 cq.exporters.export(shape,str(OUT/(name+'.step')))
 bb=solid.BoundingBox()
 report[name]={'dimensions_mm':[round(bb.xlen,2),round(bb.ylen,2),round(bb.zlen,2)],'volume_mm3':round(solid.Volume(),1),'valid':solid.isValid(),'solids':1}
(P/'validation.json').write_text(json.dumps(report,indent=2))
# Geometric preview from actual solids, not generated illustration.
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(15,9),facecolor='#f4f6f8')
for i,(name,shape) in enumerate(parts.items()):
 ax=fig.add_subplot(2,4,i+1,projection='3d')
 verts,tri=shape.val().tessellate(0.3)
 xyz=[v.toTuple() for v in verts]
 faces=[[xyz[j] for j in t] for t in tri]
 ax.add_collection3d(Poly3DCollection(faces,facecolor='#298fa8',edgecolor='none',alpha=1))
 bb=shape.val().BoundingBox();cx=(bb.xmin+bb.xmax)/2;cy=(bb.ymin+bb.ymax)/2;cz=(bb.zmin+bb.zmax)/2;r=max(bb.xlen,bb.ylen,bb.zlen)/2*1.1
 ax.set(xlim=(cx-r,cx+r),ylim=(cy-r,cy+r),zlim=(cz-r,cz+r))
 ax.view_init(30,-60);ax.set_axis_off();ax.set_title(name.replace('_',' '),fontsize=10)
fig.suptitle('ROBOCAT v0.1 | FIT-TEST PARTS | mm | not an assembled robot',fontsize=18)
plt.tight_layout();fig.savefig(P/'preview.png',dpi=150)
print(json.dumps(report,indent=2))
