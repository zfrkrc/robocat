"""CAT06B, one fused CAD solid; mm. Print front face on XY bed.
Geometry only: camera optical fit and glue retention are not validated.
"""
from pathlib import Path
import cadquery as cq,json,numpy as np
P=Path(__file__).parent;R=P.parents[1];O=P/'stl';O.mkdir(exist_ok=True)
# Original coordinate: body z0..3; rear boss z-1.5..0.
a=cq.Workplane('XY').circle(14).extrude(3)
a=a.union(cq.Workplane('XY').circle(9.8).extrude(1.5).translate((0,0,-1.5)))
a=a.cut(cq.Workplane('XY').rect(7,7).extrude(7).translate((0,0,-2)))
a=a.cut(cq.Workplane('XY').rect(9,9).extrude(2).translate((0,0,2))).clean()
assert a.val().isValid() and len(a.solids().vals())==1
# Export print orientation: large face down; boss up; minZ=0.
a=a.rotate((0,0,0),(1,0,0),180).translate((0,0,3)).clean()
name='CAT06B_eye_bezel_7x7_boss_x2'
cq.exporters.export(a,str(O/(name+'.stl')),tolerance=.08,angularTolerance=.15)
cq.exporters.export(a,str(O/(name+'.step')))
# Independent check against existing face only; not electronics/optical verification.
face=cq.importers.importStep(str(R/'custom/robocat-v0.3/stl/CAT01_white_face_x1.step'))
checks=[]
for x in [-30,30]:
 placed=a.translate((x,12,-3));i=face.intersect(placed);v=0 if not i.val() else i.val().Volume();checks.append({'x_mm':x,'face_overlap_mm3':round(v,6)});assert v<.01
import struct
bin_data=(O/(name+'.stl')).read_bytes()
tri=np.frombuffer(bin_data[84:],dtype=np.dtype([('n','<f4',3),('v','<f4',(3,3)),('att','<u2')]))['v'].reshape(-1,3)
assert abs(float(tri[:,2].min()))<1e-5
(P/'validation.json').write_text(json.dumps({'cad_valid':a.val().isValid(),'solid_count':len(a.solids().vals()),'nominal_dimensions_mm':[28,28,4.5],'stl_dimensions_mm':(tri.max(0)-tri.min(0)).tolist(),'min_z_mm':float(tri[:,2].min()),'boss_diameter_mm':19.6,'boss_height_mm':1.5,'throat_mm':[7,7],'front_recess_mm':[9,9,1],'face_checks':checks,'scope':'face and printed eye bezel only; no camera, glue, fastener, cable or thermal checks','print_orientation':'front large face down, boss up; minZ=0','physical_fit_verified':False},indent=2))
# Reproducible CAD preview.
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
v,t=a.val().tessellate(.2);v=np.array([q.toTuple() for q in v]);p=v[np.array(t)];n=np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-9);light=.4+.6*np.abs(n@np.array([.2,.4,.9]));col=light[:,None]*np.array([.4,.43,.45])
fig=plt.figure(figsize=(9,4));
for j,(elev,az,title) in enumerate([(35,-65,'Print orientation / boss up'),(-50,-90,'Front / 7 x 7 aperture')]):
 ax=fig.add_subplot(1,2,j+1,projection='3d');ax.add_collection3d(Poly3DCollection(p,facecolors=col,edgecolor='none'));ax.set(xlim=(-17,17),ylim=(-17,17),zlim=(-14,20));ax.set_axis_off();ax.view_init(elev,az);ax.set_title(title,fontsize=10)
fig.suptitle('RoboCat CAT06B / fused single solid / FIT TEST ONLY');fig.tight_layout(rect=[0,0,1,.92]);fig.savefig(P/'eye_fixed.png',dpi=140)
print('CAT06B fused: 1 solid; face overlaps <0.01mm3; minZ=0')
