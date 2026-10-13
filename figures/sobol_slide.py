"""Readable 4:3 layouts of the existing Sobol maps.

No sensitivity values are recalculated. Embedded result images are retained,
with an explicit geometric transpose: impacts become rows, parameters columns.
Each map retains its own colorbar and numeric scale.
"""
from copy import deepcopy
from pathlib import Path
import math
import re
import textwrap
import xml.etree.ElementTree as ET

from incomparability_slide import NS, XLINK, element, root, text

HERE = Path(__file__).resolve().parent
PARAMETERS = [
    'Rendement de la caténaire',
    'Consommation de diesel',
    'Durée de vie des batteries',
    'Rendement des batteries',
    'Rendement de l’électrolyse',
    'Scénario du mix électrique',
    'Durée de vie du système de référence',
    'Durée de vie de la caténaire',
    'Longueur de la ligne',
    'Pente',
    'Trains partageant la caténaire',
]
CODES = {name: chr(65 + i) for i, name in enumerate(PARAMETERS)}
TECHNOLOGIES = [('diesel', 'Diesel'), ('hydrogen', 'Hydrogène'),
                ('battery', 'Batteries'), ('electrification', 'Électrification')]
WIDTH, HEIGHT = 1373, 996
LEFT, GAP = 360, 18
CW = (WIDTH - LEFT - 3 * GAP) / 4
TOP, PH = 80, 570

def group_text(group):
    node = next(group.iter(f'{{{NS}}}text'), None)
    return ''.join(node.itertext()) if node is not None else ''

def axis(root_node, name):
    return next(g for g in root_node.iter(f'{{{NS}}}g') if g.get('id') == name)

def tick_groups(axis_node, prefix):
    return [g for g in axis_node.iter(f'{{{NS}}}g') if g.get('id', '').startswith(prefix)]

def mark(group):
    return next(u for u in group.iter(f'{{{NS}}}use')
                if u.get('x') is not None and u.get('y') is not None)

def scientific(value):
    return str(value).translate(str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))

def generate(kind):
    svg = root(WIDTH, HEIGHT)
    maps, all_impacts, used = [], None, set()
    text(svg, LEFT - 15, 35, 'Catégorie d’impact', anchor='end', size=22)
    for index, (stem, title) in enumerate(TECHNOLOGIES):
        original = ET.parse(HERE / f'{stem}_ST_{kind}_fr.svg').getroot()
        ax = axis(original, 'axes_1')
        image = next(ax.iter(f'{{{NS}}}image'))
        impacts = [group_text(g) for g in tick_groups(ax, 'xtick_')]
        parameters = [group_text(g) for g in tick_groups(ax, 'ytick_')]
        assert len(impacts) == 15
        assert all(p in CODES for p in parameters)
        if all_impacts is None:
            all_impacts = impacts
        assert impacts == all_impacts
        used.update(parameters)
        x = LEFT + index * (CW + GAP)
        text(svg, x + CW / 2, 35, title, size=24)
        ox, oy = float(image.get('x')), -float(image.get('y'))
        ow, oh = float(image.get('width')), float(image.get('height'))
        transposed = element(svg, 'g', transform=f'translate({x} {TOP}) matrix(0 1 1 0 0 0)')
        frame = element(transposed, 'svg', x=0, y=0, width=PH, height=CW,
                        viewBox=f'{ox} {oy} {ow} {oh}', preserveAspectRatio='none', overflow='hidden')
        frame.append(deepcopy(image))
        maps.append(deepcopy(image))
        element(svg, 'rect', x=x, y=TOP, width=CW, height=PH,
                fill='none', stroke='#77736c', stroke_width=1)
        # Transfer the original row tick locations to the transposed x axis.
        for g, parameter in zip(tick_groups(ax, 'ytick_'), parameters):
            m = mark(g)
            px = x + (float(m.get('y')) - oy) / oh * CW
            text(svg, px, 68, CODES[parameter], size=22)
        cb = axis(original, 'axes_2')
        bar_image = next(cb.iter(f'{{{NS}}}image'))
        bw, bh = float(bar_image.get('width')), float(bar_image.get('height'))
        bar_y = -float(bar_image.get('y'))
        cb_ticks = tick_groups(cb, 'ytick_')
        numbers = [(float(group_text(g)), float(mark(g).get('y'))) for g in cb_ticks]
        exponent = 0
        for node in cb.iter(f'{{{NS}}}text'):
            label = ''.join(node.itertext()).replace('−', '-')
            if re.fullmatch(r'1e-?\d+', label):
                exponent = int(label.split('e')[1])
        absolute_max = max(v for v, _ in numbers) * 10 ** exponent
        display_exponent = math.floor(math.log10(absolute_max)) if absolute_max < .01 else 0
        heading = 'Sₜ' + (f' × 10{scientific(display_exponent)}' if display_exponent else '')
        text(svg, x + CW / 2, 693, heading, size=22)
        bar = element(svg, 'svg', x=x, y=711, width=CW, height=18,
                      viewBox=f'0 0 {bh} {bw}', preserveAspectRatio='none')
        colored = element(bar, 'image', x=0, y=0, width=bw, height=bh,
                          transform=f'translate(0 {bw}) rotate(-90)', preserveAspectRatio='none')
        colored.set(f'{{{XLINK}}}href', bar_image.get(f'{{{XLINK}}}href'))
        # Keep three original graduations; their positions and values stay exact.
        selected = sorted(set([0, (len(numbers) - 1) // 2, len(numbers) - 1]))
        for j in selected:
            value, original_y = numbers[j]
            px = x + (1 - (original_y - bar_y) / bh) * CW
            actual = value * 10 ** (exponent - display_exponent)
            label = f'{actual:g}'.replace('.', ',')
            element(svg, 'line', x1=px, x2=px, y1=729, y2=736, stroke='#77736c')
            anchor = 'start' if px - x < 15 else ('end' if x + CW - px < 15 else 'middle')
            text(svg, px, 759, label, anchor=anchor, size=20)
    # One shared, complete set of impact labels for all four maps.
    first = ET.parse(HERE / f'diesel_ST_{kind}_fr.svg').getroot()
    ax = axis(first, 'axes_1')
    image = next(ax.iter(f'{{{NS}}}image'))
    ox, ow = float(image.get('x')), float(image.get('width'))
    for g, label in zip(tick_groups(ax, 'xtick_'), all_impacts):
        y = TOP + (float(mark(g).get('x')) - ox) / ow * PH
        text(svg, LEFT - 15, y + 7, label, anchor='end', size=20)
    text(svg, WIDTH / 2, 797, 'Paramètres — clé commune aux quatre cartes', size=22)
    entries = [p for p in PARAMETERS if p in used]
    for index, parameter in enumerate(entries):
        row, col = divmod(index, 3)
        x = col * 460 + 8
        y = 832 + row * 43
        lines = textwrap.wrap(f'{CODES[parameter]} · {parameter}', width=40,
                              break_long_words=False, break_on_hyphens=False)
        for line_index, line in enumerate(lines):
            text(svg, x, y + line_index * 22, line, anchor='start', size=20)
    target = HERE / f'sobol-{kind}-slide.svg'
    ET.ElementTree(svg).write(target, encoding='utf-8', xml_declaration=True)
    result = ET.parse(target).getroot()
    result_maps = [im for im in result.iter(f'{{{NS}}}image') if im.get('id')]
    assert [im.attrib for im in result_maps] == [im.attrib for im in maps]
    assert all(float(t.get('font-size')) >= 20 for t in result.iter(f'{{{NS}}}text'))
    print(target.name, 'four original maps retained; parameters:', len(entries))

if __name__ == '__main__':
    generate('all')
    generate('technologies')
