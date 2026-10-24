from pathlib import Path
import cadquery as cq,json
P=Path(__file__).parent;O=P/'stl';O.mkdir(exist_ok=True)
def box(x,y,z,a=0,b=0,c=0):return cq.Workplane('XY').box(x,y,z,centered=(True,True,False)).translate((a,b,c))
def drill(s,pts,d,h=80):
 for x,y in pts:s=s.cut(cq.Workplane('XY').center(x,y).circle(d/2).extrude(h).translate((0,0,-5)))
 return s
corners=[(-50,-35),(50,-35),(-50,35),(50,35)]
# front lies on build plate, rear open; ears remain within face plane
h=box(118,90,42).edges('|Z').fillet(8).cut(box(112,84,45,0,0,3).edges('|Z').fillet(5))
for x in [-39,39]:
 ear=cq.Workplane('XY').polyline([(x-19,37),(x+19,37),(x+(-7 if x<0 else 7),76)]).close().extrude(5)
 h=h.union(ear)
 # inner ear recessed decoration on front exterior, leaves 2 mm skin
 inner=cq.Workplane('XY').polyline([(x-10,44),(x+10,44),(x+(-5 if x<0 else 5),64)]).close().extrude(1)
 h=h.cut(inner)
# camera pupils
h=drill(h,[(-30,12),(30,12)],20)
# nose airflow opening and nose attachment
h=drill(h,[(0,-13)],12);h=drill(h,[(-17,-13),(17,-13)],3.4)
# camera ties; modules held behind face, clearance to be measured
for x in [-30,30]:
 for dx in [-13,13]:h=h.cut(cq.Workplane('XY').center(x+dx,10).slot2D(18,3.4,90).extrude(4))
# whisker vents
for side in [-1,1]:
 for y in [-9,-17,-25]:h=h.cut(cq.Workplane('XY').center(side*39,y).slot2D(17,2.5).extrude(4))
# bottom strap slots for a non-destructive strap to original shell
for x in [-36,36]:h=h.cut(box(14,8,4,x,-42,19))
for x,y in corners:h=h.union(cq.Workplane('XY').center(x,y).circle(4).extrude(42))
h=drill(h,corners,2.6)
lid=box(118,90,3).edges('|Z').fillet(8);lid=drill(lid,corners,3.4)
# rear ventilation
for x in [-28,-14,0,14,28]:lid=lid.cut(cq.Workplane('XY').center(x,0).slot2D(28,3,90).extrude(4))
# independent hollow muzzle, front grating; no selected gas sensor yet
n=cq.Workplane('XY').polyline([(-16,10),(16,10),(0,-13)]).close().extrude(12)
n=n.cut(cq.Workplane('XY').polyline([(-11,7),(11,7),(0,-8)]).close().extrude(10))
for x,y in [(-5,4),(0,4),(5,4),(-2.5,-1),(2.5,-1),(0,-5)]:n=drill(n,[(x,y)],2.5)
# ears of nose mount extend behind
n=n.union(box(42,8,3,0,0,0));n=n.cut(cq.Workplane('XY').circle(5).extrude(10))
n=drill(n,[(-17,0),(17,0)],3.4)
parts={'CAT01_fixed_head_shell_x1':h,'CAT02_rear_lid_x1':lid,'CAT03_vented_nose_x1':n}
report={}
for name,s in parts.items():
 assert s.val().isValid() and len(s.solids().vals())==1,name
 cq.exporters.export(s,str(O/(name+'.stl')),tolerance=.1,angularTolerance=.15)
 cq.exporters.export(s,str(O/(name+'.step')))
 b=s.val().BoundingBox();report[name]={'valid':True,'solids':1,'size_mm':[round(b.xlen,1),round(b.ylen,1),round(b.zlen,1)],'solid_volume_cm3':round(s.val().Volume()/1000,1)}
(P/'validation.json').write_text(json.dumps(report,indent=2));print(report)
# shaded mesh preview
import numpy as np,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(15,5))
for i,(name,s) in enumerate(parts.items()):
 ax=fig.add_subplot(1,3,i+1,projection='3d');v,t=s.val().tessellate(.25);v=np.array([q.toTuple() for q in v]);t=np.array(t);p=v[t];norm=np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-9);shade=.45+.55*np.abs(norm@np.array([.3,.5,.8]));base=np.array([.2,.65,.72]);colors=np.clip(shade[:,None]*base,0,1)
 ax.add_collection3d(Poly3DCollection(p,facecolors=colors,edgecolor='none'))
 lo=v.min(0);hi=v.max(0);mid=(lo+hi)/2;r=max(hi-lo)/2*1.1
 ax.set(xlim=(mid[0]-r,mid[0]+r),ylim=(mid[1]-r,mid[1]+r),zlim=(mid[2]-r,mid[2]+r));ax.view_init(65,-90);ax.set_axis_off();ax.set_title(name)
fig.suptitle('RoboCat v0.2 — fixed cat head / camera eyes / ventilated nose — FIT TEST')
plt.tight_layout();fig.savefig(P/'head_preview.png',dpi=160)
