"""Mechanical fit-test tray only. No chassis interface or electrical contacts."""
from pathlib import Path
import cadquery as cq,json
P=Path(__file__).parent
b=cq.Workplane('XY').box(118,45,26,centered=(True,True,False)).edges('|Z').fillet(2)
v=cq.Workplane('XY').box(112,39,26,centered=(True,True,False)).edges('|Z').fillet(1).translate((0,0,3))
b=b.cut(v)
# Cable opening: open top at one short end. Not a selected connector footprint.
b=b.cut(cq.Workplane('XY').box(8,20,26,centered=(True,True,False)).translate((57,0,8)))
# Strap passages across width, one on each side of the battery at two positions.
for x in [-32,32]:
 for y in [-17.5,17.5]:
  b=b.cut(cq.Workplane('XY').box(14,3,5,centered=(True,True,False)).translate((x,y,-1)))
assert b.val().isValid() and len(b.solids().vals())==1
cq.exporters.export(b,str(P/'BAT_TEST_3S_2200_TRAY_x1.stl'),tolerance=.1,angularTolerance=.2)
cq.exporters.export(b,str(P/'BAT_TEST_3S_2200_TRAY_x1.step'))
bb=b.val().BoundingBox()
(P/'tray_validation.json').write_text(json.dumps({'valid_solid':True,'solid_count':1,'outside_mm':[bb.xlen,bb.ylen,bb.zlen],'nominal_clearance_mm':[112,39,23],'battery_catalog_mm':[108,35,21],'status':'EMPTY_FIT_TEST_ONLY','chassis_mount_verified':False,'electrical_design':False},indent=2))
print('Tray valid. Empty/dummy fit only, not a verified battery mount.')
