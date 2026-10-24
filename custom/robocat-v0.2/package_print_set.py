from pathlib import Path
import shutil,csv,zipfile,hashlib,json
R=Path(__file__).resolve().parents[2];P=R.parent/'RoboCat_PrintPack_v0.2';P.mkdir(exist_ok=True)
src=R/'Nova-SM3/STL Files/SM3 Files'
rows=[]
for f in sorted(src.glob('*.stl')):
 n=f.name
 if 'Calibration' in n or 'Stand_' in n:stage='01_Kalibrasyon_ve_stand'
 elif 'Frame_' in n or n=='SM3_Foot.stl':stage='02_Govde_ve_bacaklar'
 elif 'Cover_' in n:stage='03_Orijinal_kapaklar'
 else:stage='04_Orijinal_sensor_aksesuar'
 q=2 if any(t in n for t in ['LeftCoax','RightCoax','LeftFemur','RightFemur','LeftTibia','RightTibia']) else 4 if n=='SM3_Foot.stl' else 1
 certainty='tahmini; montajla dogrula' if q>1 else 'ilk adet; montajla dogrula'
 dst=P/stage;dst.mkdir(exist_ok=True);shutil.copy2(f,dst/f.name)
 rows.append([stage,n,q,certainty,hashlib.sha256(f.read_bytes()).hexdigest()])
for f in (R/'custom/robocat-v0.2/stl').glob('*'):
 dst=P/'05_Kedi_kafasi_PROTOTIP';dst.mkdir(exist_ok=True);shutil.copy2(f,dst/f.name)
for f in (R/'custom/zk-v0.1/stl').glob('*'):
 if f.name.startswith(('02_','03_','04_','05_','06_')):
  dst=P/'06_Pil_ve_sensor_PROTOTIP';dst.mkdir(exist_ok=True);shutil.copy2(f,dst/f.name)
for f in (R/'Nova-SM3/Remote Control/STL Files').glob('*.stl'):
 dst=P/'07_Kumanda_ISTEGE_BAGLI';dst.mkdir(exist_ok=True);shutil.copy2(f,dst/f.name)
for name in ['README.md','generate_head.py','package_print_set.py','validation.json','head_preview.png']:shutil.copy2(R/'custom/robocat-v0.2'/name,P/name)
shutil.copy2(R/'LICENSE',P/'LICENSE_original_MIT.txt');shutil.copy2(R/'Nova-SM3/README.md',P/'Nova_SM3_original_README.md')
shutil.copy2(R/'custom/zk-v0.1/README.md',P/'Pil_sensor_prototip_notlari.md')
with (P/'BASKI_LISTESI.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['klasor','dosya','baslangic_adet','adet_durumu','kaynak_sha256']);w.writerows(rows)
(P/'ONCE_OKU_BASKI_SIRASI.txt').write_text('''ROBOCAT v0.2 — BASKI SIRASI\n\n0. README.md: servo/govde uyum uyarilarini oku. Parcalar mm; otomatik tumunu basma.\n1. Kalibrasyon aleti; sonra tek servo ve tek bacak uyum testi. Stand secenekleri alternatif; hepsini basma.\n2. Govde ve bacaklar: BASKI_LISTESI.csv adetleri baslangic tahmini, orijinal onayli BOM degil.\n3. Orijinal kapaklar: once kuru montaj. Kafa paneli referans olarak tutuldu. Slug kullanilmayan acikligi kapatan opsiyonel parca.\n4. Orijinal sensor yuvalari sadece kullanilan modul varsa basilacak. MP3/speaker tutuculari alternatif olabilir; hepsini basma.\n5. Kedi kafasi: burun ve kapak x1, ardindan kafa x1. Kafa baglantisi prototip; rijit govde adaptoru tamamlanmadi.\n6. Pil kartusu govde+kapak+kizak: once bir takim ENERJISIZ dene; uyarsa ikinci takimi bas. Sensor yuvasi x2, kamera besigi x3, modul olculeri dogrulanacak.\n7. El kumandasi istege bagli; ilk yuruyus icin gerekli degil.\n\nKol bu pakette yok. Eski v0.1 duz yuz paneli yeni kedi kafasinin alternatifi oldugu icin pakete konulmadi.\nTam montaj ve adetler fiziksel dogrulanmadi; siparis/uretim listesi olarak kullanma.\n''')
z=R.parent/'RoboCat_PrintPack_v0.2.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for f in P.rglob('*'):
  if f.is_file():a.write(f,'RoboCat_PrintPack_v0.2/'+str(f.relative_to(P)))
print(json.dumps({'zip':str(z),'bytes':z.stat().st_size,'original_stl':len(rows),'all_stl':len(list(P.rglob('*.stl')))}))
