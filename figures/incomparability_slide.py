"""Reframe existing result maps without changing pixels or directed axes.

The original embedded maps and their SVG transforms are preserved exactly.
Only the axes, labels, and shared legend are rebuilt for the 4:3 deck.
"""
from pathlib import Path
from copy import deepcopy
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
NS = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', NS)
ET.register_namespace('xlink', XLINK)

def element(parent, tag, **attributes):
    return ET.SubElement(parent, f'{{{NS}}}{tag}', {k.replace('_', '-'): str(v) for k, v in attributes.items()})

def text(parent, x, y, value, anchor='middle', size=22):
    node = element(parent, 'text', x=x, y=y, text_anchor=anchor, font_size=size,
                   font_family='Arial, Helvetica, sans-serif', fill='#171717')
    node.text = value
    return node

def root(width, height):
    return ET.Element(f'{{{NS}}}svg', width=str(width), height=str(height),
                      viewBox=f'0 0 {width} {height}')

def decoded(group):
    chars = []
    for node in group.iter(f'{{{NS}}}use'):
        ref = node.get(f'{{{XLINK}}}href', '')
        if ref.startswith('#DejaVuSans-'):
            chars.append(chr(int(ref.rsplit('-', 1)[-1], 16)))
    return ''.join(chars)

def generate(source, destination, xlabel, ylabel):
    original = ET.parse(HERE / source).getroot()
    image = next(original.iter(f'{{{NS}}}image'))
    ox = float(image.get('x'))
    oy = -float(image.get('y'))
    ow, oh = float(image.get('width')), float(image.get('height'))
    plot = (60, 65, 580, 490)
    svg = root(660, 680)
    text(svg, 350, 29, ylabel, size=24)
    frame = element(svg, 'svg', x=plot[0], y=plot[1], width=plot[2], height=plot[3],
                    viewBox=f'{ox} {oy} {ow} {oh}', preserveAspectRatio='none', overflow='hidden')
    frame.append(deepcopy(image))
    element(svg, 'rect', x=plot[0], y=plot[1], width=plot[2], height=plot[3],
            fill='none', stroke='#77736c', stroke_width=1)
    ticks = []
    for group in original.iter(f'{{{NS}}}g'):
        ident = group.get('id', '')
        if not ident.startswith(('xtick_', 'ytick_')):
            continue
        value = decoded(group)
        if not re.fullmatch(r'\d+(?:\.\d+)?', value):
            continue  # Colorbar labels are handled by the shared legend.
        mark = next(node for node in group.iter(f'{{{NS}}}use')
                    if node.get('x') is not None and node.get('y') is not None)
        if ident.startswith('xtick_'):
            x = plot[0] + (float(mark.get('x')) - ox) / ow * plot[2]
            element(svg, 'line', x1=x, x2=x, y1=555, y2=563, stroke='#77736c')
            text(svg, x, 590, value.replace('.', ','))
        else:
            y = plot[1] + (float(mark.get('y')) - oy) / oh * plot[3]
            element(svg, 'line', x1=52, x2=60, y1=y, y2=y, stroke='#77736c')
            text(svg, 45, y + 7, value, anchor='end')
        ticks.append((ident, value))
    text(svg, 350, 630, xlabel, size=24)
    ET.ElementTree(svg).write(HERE / destination, encoding='utf-8', xml_declaration=True)
    # Check that the original map payload and transformation remain identical.
    result = ET.parse(HERE / destination).getroot()
    assert next(result.iter(f'{{{NS}}}image')).attrib == image.attrib
    assert all(float(n.get('font-size')) >= 22 for n in result.iter(f'{{{NS}}}text'))
    print(destination, ticks)

def legend():
    original = ET.parse(HERE / 'battery_electrification_Ptrain_r_elec__Plongueur_km.svg').getroot()
    image = list(original.iter(f'{{{NS}}}image'))[1]
    svg = root(1320, 145)
    text(svg, 660, 26, 'Prédominance d’un scénario (%)', size=24)
    bar = element(svg, 'svg', x=80, y=43, width=1160, height=28,
                  viewBox='0 0 490 24', preserveAspectRatio='none')
    node = element(bar, 'image', x=0, y=0, width=24, height=490,
                   transform='translate(0 24) rotate(-90)', preserveAspectRatio='none')
    node.set(f'{{{XLINK}}}href', image.get(f'{{{XLINK}}}href'))
    text(svg, 80, 106, 'Batteries', anchor='start')
    text(svg, 660, 106, 'Incomparabilité')
    text(svg, 660, 135, 'et autres scénarios')
    text(svg, 1240, 106, 'Électrification', anchor='end')
    ET.ElementTree(svg).write(HERE / 'incomparability-legend-slide.svg', encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    generate('battery_electrification_d_stop__Pfrequentation_par_jour_sans_legende.svg',
             'incomparability-stops-slide.svg', 'Distance entre les arrêts (km)', 'Fréquentation par jour')
    generate('battery_electrification_Ptrain_r_elec__Plongueur_km.svg',
             'incomparability-trains-slide.svg', 'Trains partageant la caténaire', 'Longueur de la ligne (km)')
    legend()
