"""French vector labels on existing charts; original marks stay unchanged."""
from pathlib import Path
import base64
import xml.etree.ElementTree as E

BASE=Path(__file__).resolve().parent.parent
NS='http://www.w3.org/2000/svg'
def root(w,h):return E.Element('{'+NS+'}svg',{'width':str(w),'height':str(h),'viewBox':f'0 0 {w} {h}'})
def add(r,tag,**attrs):return E.SubElement(r,'{'+NS+'}'+tag,{k.replace('_','-'):str(v) for k,v in attrs.items()})
def label(r,x,y,value,size=20,**kw):
    t=add(r,'text',x=x,y=y,font_family='Arial, sans-serif',font_size=size,fill='#171717',**kw);t.text=value
def mask(r,x,y,w,h):add(r,'rect',x=x,y=y,width=w,height=h,fill='white')
def nested(source,w,h):
    r=root(w,h);original=E.parse(BASE/source).getroot();original.set('width',str(w));original.set('height',str(h));r.append(original);return r
def save(r,name):E.ElementTree(r).write(BASE/'figures'/name,encoding='utf-8',xml_declaration=True)

r=nested('figures/speed-model-no-title.svg',1250,850)
mask(r,205,124,320,119);mask(r,70,270,50,370);mask(r,470,782,500,48)
for y,t in zip([150,178,206,234],['Modélisation : i = 3 ‰','Modélisation : i = 0 ‰','Modélisation : i = −3 ‰','Courbe de limitation']):label(r,220,y,t,19)
label(r,0,0,'Vitesse maximale atteignable (m/s)',21,transform='translate(105 440) rotate(-90)',text_anchor='middle')
label(r,635,810,'Distance minimale entre arrêts (m)',21,text_anchor='middle')
save(r,'annexe-fr-speed.svg')

r=nested('assets/vector/s57_Espace_r_serv_du_contenu_6.svg',1200,350)
mask(r,0,0,650,70)
label(r,20,44,'Changement climatique',40)
mask(r,75,142,185,62)
label(r,80,165,'Concentration',20)
label(r,80,193,'de CO₂',20)
mask(r,295,142,905,35)
label(r,354,171,'Limite planétaire',19,text_anchor='middle')
label(r,516,171,'Seuil de risque élevé',19,text_anchor='middle')
label(r,1005,171,'CO₂ atmosphérique (ppm)',20,text_anchor='middle')
mask(r,400,267,160,24)
label(r,478,287,'Valeur en 2025',20,text_anchor='middle')
save(r,'annexe-fr-climate-boundary.svg')

r=nested('assets/vector/s58_Graphique_1.svg',1250,850)
mask(r,0,506,1250,344)
labels=['Particules fines','Ressources fossiles','Écotoxicité, eau douce','Eutrophisation, eau douce','Changement climatique','Toxicité humaine, cancer','Toxicité humaine, hors cancer','Rayonnements ionisants','Utilisation des sols','Écotoxicité marine','Eutrophisation marine','Ressources minérales','Formation d’ozone : santé humaine','Formation d’ozone : écosystèmes','Appauvrissement de l’ozone','Acidification terrestre','Écotoxicité terrestre','Consommation d’eau']
for i,t in enumerate(labels):label(r,0,0,t,22,transform=f'translate({160+i*61.75} 522) rotate(-45)',text_anchor='end')
save(r,'annexe-fr-midpoints.svg')

r=root(2048,710)
add(r,'image',x=0,y=0,width=2048,height=669,href='data:image/png;base64,'+base64.b64encode((BASE/'assets/media/image99.png').read_bytes()).decode())
for panel,(assessed,crossed) in enumerate([(7,3),(7,4),(9,6),(9,7)]):
    dx=panel*512
    mask(r,dx+20,565,475,85)
    label(r,dx+255,600,f'{assessed} limites évaluées,',28,text_anchor='middle')
    label(r,dx+255,638,f'{crossed} dépassées',28,text_anchor='middle')
# Translate the outer boundary labels without changing their colored sectors.
for panel in range(4):
    dx=panel*512
    for x,y,w,h,lines in [
        (160,148,95,32,['Changement','climatique']),
        (45,326,98,32,['Occupation','des sols']),
        (100,435,98,25,['Eau douce']),
        (228,482,88,33,['Flux','biogéochimiques']),
        (327,419,85,33,['Acidification','des océans']),
        (395,315,90,43,['Aérosols','atmosphériques']),
        (365,222,120,33,['Ozone','stratosphérique'])]:
        mask(r,dx+x,y,w,h)
        for j,line in enumerate(lines):label(r,dx+x+w/2,y+12+j*12,line,10,text_anchor='middle')
    bx=108 if panel==0 else 53
    mask(r,dx+bx,217,86,31)
    label(r,dx+bx+43,229,'Intégrité de',10,text_anchor='middle')
    label(r,dx+bx+43,242,'la biosphère',10,text_anchor='middle')
    # These labels occupy the original annotation area, not a sector boundary.
    color='white' if panel==0 else ('#d2d2d2' if panel==1 else '#ff743c')
    add(r,'rect',x=dx+292,y=158,width=90,height=33,fill=color)
    label(r,dx+337,172,'Entités nouvelles',10,text_anchor='middle')
label(r,1024,697,'Libellés : intégrité de la biosphère · entités nouvelles · espace de fonctionnement sûr · risque croissant',22,text_anchor='middle')
save(r,'annexe-fr-planetary.svg')

p=BASE/'presentation.qmd';s=p.read_text(encoding='utf-8')
for old,new in [('figures/speed-model-no-title.svg','figures/annexe-fr-speed.svg'),('assets/vector/s57_Espace_r_serv_du_contenu_6.svg','figures/annexe-fr-climate-boundary.svg'),('assets/vector/s58_Graphique_1.svg','figures/annexe-fr-midpoints.svg'),('assets/media/image99.png','figures/annexe-fr-planetary.svg')]:s=s.replace('src="'+old+'"','src="'+new+'"',1)
p.write_text(s,encoding='utf-8')
