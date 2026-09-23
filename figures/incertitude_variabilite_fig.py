# Adapté de LCA/examples/schema_bloc/incertitude_variabilite_fig.py.
# Version française et état de focus pour la soutenance.
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import html


OUT_PATH = Path(__file__).with_name("uncertainty_variability_diagram.svg")

HEADER_FILL = "#333333"
CONTEXT_FILL = "#eeeeee"
DECISION_FILL = "#eeeeee"
PROCESS_FILL = "#dddddd"
IMPACT_FILL = "#555555"
STROKE_COLOR = "#333333"
TEXT_COLOR = "#111111"
LIGHT_TEXT = "#ffffff"
FONT_SIZE = 22


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
    font_size: int = FONT_SIZE

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
    color: str = STROKE_COLOR
    width: int = 2


def create_boxes() -> dict[str, Box]:
    return {
        "uncertainty": Box(
            "Incertitude",
            40,
            75,
            250,
            62,
            fill=HEADER_FILL,
            text_color=LIGHT_TEXT,
        ),
        "contextual_1": Box(
            "Construction du modèle",
            340,
            45,
            300,
            72,
            fill=CONTEXT_FILL,
        ),
        "contextual_2": Box(
            "Incertitude des\nparamètres",
            340,
            135,
            300,
            72,
            fill=CONTEXT_FILL,
        ),
        "variability": Box(
            "Variabilité",
            40,
            285,
            250,
            62,
            fill=HEADER_FILL,
            text_color=LIGHT_TEXT,
        ),
        "decision": Box(
            "Variabilité des\nparamètres",
            340,
            255,
            300,
            72,
            fill=CONTEXT_FILL,
        ),
        "production": Box(
            "Modélisation du\nsystème",
            710,
            155,
            260,
            86,
            fill=PROCESS_FILL,
        ),
        "lca": Box(
            "ACV",
            1020,
            170,
            120,
            56,
            fill=HEADER_FILL,
            text_color=LIGHT_TEXT,
        ),
        "impact": Box(
            "Résultats d’impact\nou classement",
            1190,
            155,
            190,
            86,
            fill=IMPACT_FILL,
            text_color=LIGHT_TEXT,
        ),
    }


def create_arrows(boxes: dict[str, Box]) -> list[Arrow]:
    production = boxes["production"]

    return [
        Arrow(boxes["uncertainty"].right_mid, boxes["contextual_1"].left_mid),
        Arrow(boxes["uncertainty"].right_mid, boxes["contextual_2"].left_mid),
        Arrow(boxes["variability"].right_mid, boxes["decision"].left_mid),
        Arrow(boxes["contextual_1"].right_mid, (production.x, production.y + 18)),
        Arrow(boxes["contextual_2"].right_mid, (production.x, production.y + 34)),
        Arrow(boxes["decision"].right_mid, (production.x, production.y + production.h - 22)),
        Arrow(production.right_mid, boxes["lca"].left_mid),
        Arrow(boxes["lca"].right_mid, boxes["impact"].left_mid),
    ]


def svg_text_lines(text: str, x: int, y: int, w: int, h: int, font_size: int, color: str) -> str:
    lines = text.split("\n")
    line_height = int(font_size * 1.2)
    total_height = line_height * len(lines)
    start_y = y + (h - total_height) // 2 + font_size
    center_x = x + w // 2

    tspans = []
    for i, line in enumerate(lines):
        line_y = start_y + i * line_height
        tspans.append(f'<tspan x="{center_x}" y="{line_y}">{html.escape(line)}</tspan>')

    return (
        f'<text text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{font_size}" fill="{color}">' + "".join(tspans) + "</text>"
    )


def render_box(box: Box) -> str:
    return (
        f'<rect x="{box.x}" y="{box.y}" rx="6" ry="6" width="{box.w}" height="{box.h}" '
        f'fill="{box.fill}" stroke="{box.stroke}" stroke-width="1.5" />\n'
        + svg_text_lines(box.text, box.x, box.y, box.w, box.h, box.font_size, box.text_color)
    )


def render_arrow(arrow: Arrow) -> str:
    (x1, y1), (x2, y2) = arrow.start, arrow.end
    mid_x = (x1 + x2) // 2
    path = f"M {x1} {y1} C {mid_x} {y1}, {mid_x} {y2}, {x2} {y2}"
    return (
        f'<path d="{path}" fill="none" stroke="{arrow.color}" stroke-width="{arrow.width}" '
        f'marker-end="url(#arrowhead)" />'
    )


def render_svg(boxes: dict[str, Box], arrows: list[Arrow], focus: bool = False) -> str:
    width = 1420
    height = 410

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs>',
        '<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="8" refY="3.5" orient="auto">',
        f'<polygon points="0 0, 10 3.5, 0 7" fill="{STROKE_COLOR}" />',
        "</marker>",
        "</defs>",
        svg_text_lines(
            "",
            250,
            10,
            900,
            30,
            FONT_SIZE,
            STROKE_COLOR,
        ),
    ]

    for arrow in arrows:
        opacity = "0.2" if focus else "1"
        parts.append(f'<g opacity="{opacity}">{render_arrow(arrow)}</g>')

    for key, box in boxes.items():
        opacity = "0.2" if focus and key != "contextual_1" else "1"
        rendered = render_box(box)
        if focus and key == "contextual_1":
            rendered = rendered.replace('stroke-width="1.5"', 'stroke-width="4"')
        parts.append(f'<g id="{key}" opacity="{opacity}">{rendered}</g>')

    parts.append("</svg>")
    return "\n".join(parts)


def build_diagram(out_path: Path = OUT_PATH) -> Path:
    boxes = create_boxes()
    arrows = create_arrows(boxes)
    svg = render_svg(boxes, arrows)
    out_path.write_text(svg, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    print(build_diagram())
    focus_path = OUT_PATH.with_name("uncertainty_variability_focus.svg")
    boxes = create_boxes()
    focus_path.write_text(render_svg(boxes, create_arrows(boxes), focus=True), encoding="utf-8")
    print(focus_path)
