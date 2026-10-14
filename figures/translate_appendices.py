"""Translate appendix vector labels without changing plotted result geometry."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent.parent
NS = 'http://www.w3.org/2000/svg'
XL = 'http://www.w3.org/1999/xlink'
T = {
 'Climate change':'Changement climatique', 'Ecotoxicity, freshwater':'Écotoxicité, eau douce',
 'Eutrophication, freshwater':'Eutrophisation, eau douce', 'Eutrophication, marine':'Eutrophisation marine',
 'Eutrophication, terrestrial':'Eutrophisation terrestre', 'Human toxicity, cancer':'Toxicité humaine, cancer',
 'Ionising radiation':'Rayonnements ionisants', 'Land use':'Utilisation des sols',
 'Ozone depletion':'Appauvrissement de l’ozone', 'Particulate matter':'Particules fines',
 'Photochemical ozone formation':'Formation d’ozone photochimique',
 'Resource use, fossils':'Ressources fossiles', 'Resource use, minerals and metals':'Ressources minérales et métalliques',
 'Water use':'Utilisation de l’eau', 'Criterion-normalized impact':'Impact normalisé par critère',
 'catenary 1500V':'Caténaire 1 500 V', 'catenary 25kV':'Caténaire 25 kV',
 'ecosystem quality':'Qualité des écosystèmes', 'human health':'Santé humaine',
 'resources':'Ressources', 'battery technology':'Technologie de batterie', 'single score':'Score unique',
 'Production scale MWh':'Échelle de production (MWh)',
 'Weight':'Poids', 'Criteria':'Critères', 'Cost':'Coût', 'Ecosystem diversity':'Diversité des écosystèmes',
 'Resource scarcity':'Rareté des ressources', 'Human health':'Santé humaine', 'Social impact':'Impact social',
 'Alternatives':'Solutions', 'Biofuel':'Biocarburant', 'Hybrid':'Hybride', 'Hydrogen':'Hydrogène',
 'Electrification':'Électrification', 'Scenario':'Scénario', 'Rank':'Rang',
}

def decode(group):
    result = ''
    for use in group.iter(f'{{{NS}}}use'):
        m = re.search(r'-([0-9a-fA-F]+)$', use.get(f'{{{XL}}}href', ''))
        if m:
            try: result += chr(int(m[1],16))
            except ValueError: pass
    return result

def translate_svg(source):
    r = ET.parse(BASE/source).getroot()
    parents = {child:parent for parent in r.iter() for child in parent}
    changes = 0
    for g in list(r.iter(f'{{{NS}}}g')):
        if not re.fullmatch(r'text_\d+', g.get('id','')): continue
        label = decode(g)
        if label not in T: continue
        transformed = next((n for n in g if n.get('transform')),None)
        if transformed is None: continue
        matrix = re.fullmatch(r'matrix\(([^)]+)\)',transformed.get('transform',''))
        if matrix:
            a,b,c,d,x,y = map(float, matrix[1].replace(',',' ').split())
            parent = parents.get(g)
            is_x = parent is not None and parent.get('id','').startswith('xtick_')
            if is_x:
                tick = next((u for u in parent.iter(f'{{{NS}}}use') if u.get('x') and u.get('y')),None)
                path = next((p for p in parent.iter(f'{{{NS}}}path') if p.get('d','').startswith('M')),None)
                if tick is not None:
                    x,y = float(tick.get('x')),float(tick.get('y'))+22
                elif path is not None:
                    nums = re.findall(r'-?\d+(?:\.\d+)?',path.get('d'))
                    x,y = float(nums[0]),float(nums[1])+12
                if abs(b)<.001:
                    transform=f'translate({x} {y})';size,anchor=12,'middle'
                else:
                    transform = f'translate({x} {y}) rotate(-45)'
                    size,anchor = 9,'end'
            else:
                transform=f'matrix({a} {b} {-c} {-d} {x} {y})'
                size,anchor = 100,'start'
            # Glyph definitions may be reused by other labels: keep their defs.
            for node in list(transformed.iter(f'{{{NS}}}defs')):
                g.append(node)
            g.remove(transformed)
            text = ET.SubElement(g,f'{{{NS}}}text',{'transform':transform,'font-family':'Arial, sans-serif','font-size':str(size),'text-anchor':anchor,'fill':'#171717'})
            text.text=T[label]
            changes+=1
    for node in r.iter():
        if node.tag in [f'{{{NS}}}text',f'{{{NS}}}tspan'] and node.text in T:
            node.text=T[node.text];changes+=1
    target=BASE/'figures'/('annexe-fr-'+Path(source).stem+'.svg')
    ET.ElementTree(r).write(target,encoding='utf-8',xml_declaration=True)
    print(target.name,changes)
    return target.relative_to(BASE).as_posix()

def main():
    p=BASE/'presentation.qmd';s=p.read_text(encoding='utf-8')
    headings=list(re.finditer(r'^## .*$',s,re.M))
    for i in range(len(headings)-1,-1,-1):
        h=headings[i]
        if '.appendix-slide' not in h.group():continue
        a,b=h.start(),headings[i+1].start() if i+1<len(headings) else len(s)
        block=s[a:b]
        for source in re.findall(r'src="([^"]+\.svg)"',block):
            if source in ['assets/media/image100.svg','assets/media/image101.svg','assets/media/image47.svg','assets/media/image50.svg','assets/media/image51.svg','assets/vector/s28_Espace_r_serv_du_contenu_6.svg','assets/vector/s38_Groupe_8.svg']:
                block=block.replace('src="'+source+'"','src="'+translate_svg(source)+'"')
        block=block.replace('src="assets/media/image103.svg"','src="figures/lcia/impact_pathways_fr.svg"')
        for old,new in T.items():
            block=re.sub(r'(?<=>)'+re.escape(old)+r'(?=<)',lambda _:new,block)
        s=s[:a]+block+s[b:]
    p.write_text(s,encoding='utf-8')

if __name__=='__main__':main()
