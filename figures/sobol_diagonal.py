"""Retain the original Sobol orientation with readable diagonal impact labels."""
from copy import deepcopy
import math
import re
import xml.etree.ElementTree as ET
from sobol_slide import HERE, TECHNOLOGIES, PARAMETERS, axis, tick_groups, group_text, mark, scientific
from incomparability_slide import NS, element, root, text

SHORT = dict(zip(PARAMETERS, [
    'Rend. caténaire', 'Conso. diesel', 'Vie batteries', 'Rend. batteries',
    'Rend. électrolyse', 'Mix électrique', 'Vie de référence', 'Vie caténaire',
    'Longueur ligne', 'Pente', 'Trains / caténaire']))

def generate(kind):
    for stem, title in TECHNOLOGIES:
        original = ET.parse(HERE / f'{stem}_ST_{kind}_fr.svg').getroot()
        svg = root(690, 525)
        text(svg, 405, 29, title, size=24)
        ax = axis(original, 'axes_1')
        image = next(ax.iter(f'{{{NS}}}image'))
        ox, oy = float(image.get('x')), -float(image.get('y'))
        ow, oh = float(image.get('width')), float(image.get('height'))
        frame = element(svg, 'svg', x=180, y=50, width=450, height=210,
                        viewBox=f'{ox} {oy} {ow} {oh}', preserveAspectRatio='none', overflow='hidden')
        frame.append(deepcopy(image))
        element(svg, 'rect', x=180, y=50, width=450, height=210,
                fill='none', stroke='#77736c', stroke_width=1)
        for g in tick_groups(ax, 'xtick_'):
            x = 180 + (float(mark(g).get('x')) - ox) / ow * 450
            node = text(svg, 0, 0, group_text(g), anchor='end', size=20.5)
            node.set('transform', f'translate({x} 277) rotate(-50)')
        for g in tick_groups(ax, 'ytick_'):
            y = 50 + (float(mark(g).get('y')) - oy) / oh * 210
            label = group_text(g)
            node = text(svg, 165, y + 7, SHORT[label], anchor='end', size=20.5)
            element(node, 'title').text = label
        cb = axis(original, 'axes_2')
        bar_image = next(cb.iter(f'{{{NS}}}image'))
        bx, by = float(bar_image.get('x')), -float(bar_image.get('y'))
        bw, bh = float(bar_image.get('width')), float(bar_image.get('height'))
        bar = element(svg, 'svg', x=637, y=50, width=10, height=210,
                      viewBox=f'{bx} {by} {bw} {bh}', preserveAspectRatio='none')
        bar.append(deepcopy(bar_image))
        numbers = [(float(group_text(g)), float(mark(g).get('y')))
                   for g in tick_groups(cb, 'ytick_')]
        exponent = 0
        for node in cb.iter(f'{{{NS}}}text'):
            label = ''.join(node.itertext()).replace('−', '-')
            if re.fullmatch(r'1e-?\d+', label):
                exponent = int(label.split('e')[1])
        maximum = max(v for v, _ in numbers) * 10 ** exponent
        display_exponent = math.floor(math.log10(maximum)) if maximum < .01 else 0
        heading = 'Sₜ' + (f' ×10{scientific(display_exponent)}' if display_exponent else '')
        text(svg, 635, 29, heading, size=20.5)
        for value, original_y in numbers:
            y = 50 + (original_y - by) / bh * 210
            label = f'{value * 10 ** (exponent - display_exponent):g}'.replace('.', ',')
            text(svg, 653, y + 7, label, anchor='start', size=20.5)
        target = HERE / f'sobol-{stem}-{kind}-diagonal.svg'
        ET.ElementTree(svg).write(target, encoding='utf-8', xml_declaration=True)
        assert next(frame.iter(f'{{{NS}}}image')).attrib == image.attrib
        print(target.name)

if __name__ == '__main__':
    generate('all')
    generate('technologies')
