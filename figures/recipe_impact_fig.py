# Adapté de ../LCA/examples/schema_bloc/recipe_impact_fig.py.
# Traduction française du schéma ReCiPe fourni.
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import html


OUT_PATH = Path(__file__).with_name("LCIA_diagram.svg")
HEADER_FILL = "#333333"  # Matplotlib magma(0.28)
MID_FILL = "#eeeeee"  # Matplotlib magma(0.97)
HUMAN_FILL = "#eeeeee"  # Matplotlib magma(0.92)
ECOSYSTEM_FILL = "#dddddd"  # Matplotlib magma(0.78)
RESOURCE_FILL = "#cccccc"  # Matplotlib magma(0.62)
STROKE_COLOR = "#333333"  # Matplotlib magma(0.12)
TEXT_COLOR = "#111111"


@dataclass(frozen=True)
class Box:
    text: str
    x: int
    y: int
    w: int
    h: int
    fill: str
    stroke: str = STROKE_COLOR
    text_color: str = TEXT_COLOR
    font_size: int = 16

    @property
    def left_mid(self) -> tuple[int, int]:
        return (self.x, self.y + self.h // 2)

    @property
    def right_mid(self) -> tuple[int, int]:
        return (self.x + self.w, self.y + self.h // 2)


@dataclass(frozen=True)
class Arrow:
    start: tuple[int, int]
    end: tuple[int, int]
    dashed: bool = False
    color: str = STROKE_COLOR
    width: int = 2


MIDPOINTS = [
    "Particules fines",
    "Formation d’ozone\n(santé humaine)",
    "Rayonnements ionisants",
    "Appauvrissement de l’ozone\nstratosphérique",
    "Toxicité humaine (cancer)",
    "Toxicité humaine (hors cancer)",
    "Changement climatique",
    "Utilisation de l’eau",
    "Écotoxicité en eau douce",
    "Eutrophisation des eaux douces",
    "Formation d’ozone\n(écosystèmes)",
    "Écotoxicité terrestre",
    "Acidification terrestre",
    "Utilisation / transformation des sols",
    "Écotoxicité marine",
    "Eutrophisation marine",
    "Ressources minérales",
    "Ressources fossiles",
]

PATHWAYS = [
    "Augmentation des\nmaladies respiratoires",
    "Augmentation des\ndifférents cancers",
    "Augmentation des autres\nmaladies / causes",
    "Augmentation de\nla malnutrition",
    "Dommages aux espèces\nd’eau douce",
    "Dommages aux\nespèces terrestres",
    "Dommages aux\nespèces marines",
    "Hausse des coûts\nd’extraction",
    "Coût énergétique\npétrole / gaz / charbon",
]

ENDPOINTS = [
    "Dommages à la\nsanté humaine",
    "Dommages aux\nécosystèmes",
    "Dommages à la\ndisponibilité\ndes ressources",
]


def create_boxes() -> tuple[list[Box], list[Box], list[Box]]:
    mid_boxes: list[Box] = []
    path_boxes: list[Box] = []
    end_boxes: list[Box] = []

    left_x = 30
    mid_x = 430
    right_x = 800

    mid_w, mid_h = 300, 42
    path_w, path_h = 220, 78
    end_w, end_h = 180, 84

    top_y = 70
    mid_gap = 10
    path_gap = 18
    end_gap = 80

    for i, label in enumerate(MIDPOINTS):
        y = top_y + i * (mid_h + mid_gap)
        mid_boxes.append(Box(label, left_x, y, mid_w, mid_h, fill=MID_FILL))

    path_colors = [HUMAN_FILL] * 4 + [ECOSYSTEM_FILL] * 3 + [RESOURCE_FILL] * 2
    for i, label in enumerate(PATHWAYS):
        y = top_y + 8 + i * (path_h + path_gap)
        path_boxes.append(Box(label, mid_x, y, path_w, path_h, fill=path_colors[i]))

    end_colors = [HUMAN_FILL, ECOSYSTEM_FILL, RESOURCE_FILL]
    for i, label in enumerate(ENDPOINTS):
        y = top_y + 40 + i * (end_h + end_gap)
        end_boxes.append(Box(label, right_x, y, end_w, end_h, fill=end_colors[i]))

    return mid_boxes, path_boxes, end_boxes


MIDPOINT_TO_PATHWAY: dict[int, list[int]] = {
    0: [0],  # Particulate matter
    1: [0],  # Trop. ozone formation (hum)
    2: [1, 2],  # Ionizing radiation
    3: [1, 2],  # Stratos. ozone depletion
    4: [1],  # Human toxicity (cancer)
    5: [2],  # Human toxicity (non-cancer)
    6: [2, 3, 4, 5],  # Global warming
    7: [3, 4, 5],  # Water use
    8: [4],  # Freshwater ecotoxicity
    9: [4],  # Freshwater eutrophication
    10: [5],  # Trop. ozone formation (eco)
    11: [5],  # Terrestrial ecotoxicity
    12: [5],  # Terrestrial acidification
    13: [5],  # Land use/transformation
    14: [6],  # Marine ecotoxicity
    15: [6],  # Marine eutrophication
    16: [7],  # Mineral resources
    17: [8],  # Fossil resources
}

PATHWAY_TO_ENDPOINT = {
    0: 0,  # Increase in respiratory disease
    1: 0,  # Increase in various types of cancer
    2: 0,  # Increase in other diseases/causes
    3: 0,  # Increase in malnutrition
    4: 1,  # Damage to freshwater species
    5: 1,  # Damage to terrestrial species
    6: 1,  # Damage to marine species
    7: 2,  # Increased extraction costs
    8: 2,  # Oil/gas/coal energy cost
}

DASHED_MIDPOINTS = {17}  
DASHED_PATHWAYS = {8}    


def create_arrows(mid_boxes: list[Box], path_boxes: list[Box], end_boxes: list[Box]) -> list[Arrow]:
    arrows: list[Arrow] = []

    for mid_idx, path_indices in MIDPOINT_TO_PATHWAY.items():
        for path_idx in path_indices:
            arrows.append(
                Arrow(
                    start=mid_boxes[mid_idx].right_mid,
                    end=path_boxes[path_idx].left_mid,
                    dashed=mid_idx in DASHED_MIDPOINTS,
                )
            )

    for path_idx, end_idx in PATHWAY_TO_ENDPOINT.items():
        arrows.append(
            Arrow(
                start=path_boxes[path_idx].right_mid,
                end=end_boxes[end_idx].left_mid,
                dashed=path_idx in DASHED_PATHWAYS,
            )
        )

    return arrows


def svg_text_lines(text: str, x: int, y: int, w: int, h: int, font_size: int, color: str) -> str:
    lines = text.split("\n")
    line_height = int(font_size * 1.2)
    total_height = line_height * len(lines)
    start_y = y + (h - total_height) // 2 + font_size
    center_x = x + w // 2

    tspans = []
    for i, line in enumerate(lines):
        line_y = start_y + i * line_height
        tspans.append(
            f'<tspan x="{center_x}" y="{line_y}">{html.escape(line)}</tspan>'
        )
    return (
        f'<text text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{font_size}" fill="{color}">' + "".join(tspans) + "</text>"
    )


def render_box(box: Box) -> str:
    return (
        f'<rect x="{box.x}" y="{box.y}" rx="4" ry="4" width="{box.w}" height="{box.h}" '
        f'fill="{box.fill}" stroke="{box.stroke}" stroke-width="1.5" />\n'
        + svg_text_lines(box.text, box.x, box.y, box.w, box.h, box.font_size, box.text_color)
    )


def render_arrow(arrow: Arrow) -> str:
    (x1, y1), (x2, y2) = arrow.start, arrow.end
    mid_x = (x1 + x2) // 2
    dash = ' stroke-dasharray="6,4"' if arrow.dashed else ""
    path = f"M {x1} {y1} C {mid_x} {y1}, {mid_x} {y2}, {x2} {y2}"
    return (
        f'<path d="{path}" fill="none" stroke="{arrow.color}" stroke-width="{arrow.width}"{dash} '
        f'marker-end="url(#arrowhead)" />'
    )


def render_svg(box_groups: Iterable[Iterable[Box]], arrows: Iterable[Arrow]) -> str:
    width = 1020
    height = 1030
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs>',
        '<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="8" refY="3.5" orient="auto">',
        f'<polygon points="0 0, 10 3.5, 0 7" fill="{STROKE_COLOR}" />',
        '</marker>',
        '</defs>',
        svg_text_lines("Catégories d’impact", 30, 12, 300, 40, 22, "#ffffff").replace('<text ', f'<g><path d="M 30 12 h 300 l 20 20 -20 20 h -300 z" fill="{HEADER_FILL}" /><text ').replace('</text>', '</text></g>'),
        svg_text_lines("Mécanismes de dommage", 430, 12, 220, 40, 16, "#ffffff").replace('<text ', f'<g><path d="M 430 12 h 220 l 20 20 -20 20 h -220 z" fill="{HEADER_FILL}" /><text ').replace('</text>', '</text></g>'),
        svg_text_lines("Domaines\nde protection", 780, 5, 220, 60, 22, "#ffffff").replace('<text ', f'<g><path d="M 780 12 h 220 l 20 24 -20 24 h -220 z" fill="{HEADER_FILL}" /><text ').replace('</text>', '</text></g>'),
    ]

    for arrow in arrows:
        parts.append(render_arrow(arrow))

    for group in box_groups:
        for box in group:
            parts.append(render_box(box))

    parts.append('</svg>')
    return "\n".join(parts)


def build_diagram(out_path: Path = OUT_PATH) -> Path:
    mid_boxes, path_boxes, end_boxes = create_boxes()
    arrows = create_arrows(mid_boxes, path_boxes, end_boxes)
    svg = render_svg((mid_boxes, path_boxes, end_boxes), arrows)
    out_path.write_text(svg, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    print(build_diagram())
