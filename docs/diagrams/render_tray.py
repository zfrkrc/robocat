from pathlib import Path
import cadquery as cq,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
r=Path(__file__).resolve().parents[2]
s=cq.importers.importStep(str(r/'custom/print-fit-v0.4/BAT_TEST_3S_2200_TRAY_x1.step'))
v,t=s.val().tessellate(.35);v=np.array([x.toTuple() for x in v]);faces=v[np.array(t)];n=np.cross(faces[:,1]-faces[:,0],faces[:,2]-faces[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-9)
shade=.5+.5*np.abs(n@np.array([.3,.5,.8]));colors=shade[:,None]*np.array([.15,.65,.68])
fig=plt.figure(figsize=(10,5),facecolor='#edf2f6');ax=fig.add_subplot(projection='3d');ax.add_collection3d(Poly3DCollection(faces,facecolors=colors,edgecolor='none'));ax.set(xlim=(-65,65),ylim=(-40,40),zlim=(-20,60));ax.set_box_aspect((130,80,80));ax.view_init(40,-65);ax.set_axis_off();fig.suptitle('RoboCat / LiPo tray — actual CAD, empty fit-test only',fontsize=16);fig.text(.5,.06,'118 x 45 x 26 mm outside | No chassis mount or electrical contacts',ha='center',fontsize=11);fig.savefig(r/'docs/images/lipo-tray-fit-v0.4.png',dpi=140,bbox_inches='tight')
