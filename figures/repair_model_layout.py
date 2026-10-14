from pathlib import Path
import xml.etree.ElementTree as E
NS='http://www.w3.org/2000/svg'
r=E.Element('{'+NS+'}svg',{'width':'1800','height':'1000','viewBox':'0 0 1800 1000'})
def add(parent,tag,**a):return E.SubElement(parent,'{'+NS+'}'+tag,{k.replace('_','-'):str(v) for k,v in a.items()})
defs=add(r,'defs');m=add(defs,'marker',id='arrow',markerWidth=10,markerHeight=10,refX=10,refY=5,orient='auto',markerUnits='userSpaceOnUse');add(m,'path',d='M0 0 L10 5 L0 10 Z',fill='#666')
edges=add(r,'g',fill='none',stroke='#666',stroke_width=2,stroke_linejoin='round',marker_end='url(#arrow)')
for path in ['M170 200 V260 H360 V510 H340','M410 200 V240 H630 V470','M650 200 V250 H1080 V470','M190 400 V470','M1540 185 V215','M1365 300 H1170 V470','M1540 385 V420','M1390 550 H1300','M340 550 H480','M780 550 H960','M1130 630 V730','M190 630 V930 H470','M630 630 V850','M1130 880 V930 H820']:
 add(edges,'path',d=path)
boxes=add(r,'g',fill='#f6f4ef',stroke='#171717',stroke_width=2)
for x,y,w,h in [(40,40,750,160),(65,105,210,65),(305,105,210,65),(545,105,210,65),(1040,40,700,145),(40,300,300,100),(40,470,300,160),(480,470,300,160),(960,470,340,160),(960,730,340,150),(470,850,350,100),(1390,420,360,280)]:
 add(boxes,'rect',x=x,y=y,width=w,height=h,rx=8)
add(boxes,'path',d='M1540 215 L1715 300 L1540 385 L1365 300 Z')
labels=add(r,'g',font_family='Arial, sans-serif',fill='#171717',text_anchor='middle')
def label(x,y,lines,size=26,gap=36):
 t=add(labels,'text',x=x,y=y,font_size=size)
 for i,line in enumerate(lines):add(t,'tspan',x=x,dy=0 if i==0 else gap).text=line
label(415,80,['Données d’impact brutes du scénario n'])
label(170,145,['Système embarqué'],22);label(410,145,['Infrastructure'],22);label(650,145,['Énergie'],22)
label(1390,85,['Données de roulement','Pente, arrêts, vitesse, électrification'],24,45)
label(190,342,['Données du','matériel roulant'],26,32)
label(190,526,['Modélisation du','système embarqué'])
label(630,526,['Modélisation de','l’infrastructure'])
label(1130,510,['Puissance consommée','en roulement :','Pbus, a'])
label(1130,771,['Consommation et','récupération d’énergie :','E, Erecup'])
label(645,891,['Impacts du','scénario n'])
label(1540,290,['Données de roulement','disponibles ?'],20,30)
label(1570,462,['Modélisation du roulement'],24)
label(1570,510,['Accélération :','distance entre arrêts, a max, P max','Croisière :','P max, i, distance entre arrêts','Décélération :','V max, a min, P min (optionnel)'],21,33)
label(1260,285,['Oui'],22);label(1570,410,['Non'],22)
E.ElementTree(r).write(Path(__file__).parent/'appendix_model_fr.svg',encoding='utf-8',xml_declaration=True)
