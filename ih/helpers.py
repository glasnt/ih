"""
Helpers and values
"""
import os
import pkg_resources
from pathlib import Path

# A series of visually distinct characters, to populate the chart
STARS = [
    "✚",
    "✽",
    "※",
    "✷",
    "❐",
    "❄",
    "✔",
    "◀",
    "⊐",
    "♠",
    "★",
    "»",
    "✿",
    "⟘",
    "❦",
    "⟒",
    "❦",
    "⚉",
    "♣",
    "▷",
    "♦",
    "×",
    "«",
    "△",
    "⊔",
    "➤",
    "⚑",
    "◼",
    "⬇",
    "✭",
    "⧓",
    "❤",
    "✤",
    "⟙",
    "✾",
    "∀",
    "⊕",
    "♥",
    "⬆",
    "⚇",
    "◼",
    "✰",
]


def rgb2hex(pix):
    """Given a tuple of r, g, b, return the hex value """
    r, g, b = pix[:3]
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def hex2rgb(h):
    h = h.strip("#")
    return list(int(h[i : i + 2], 16) for i in (0, 2, 4))


def guide_cell(guide):
    classes = "s"
    if guide[0]:
        classes += " gx"
    if guide[1]:
        classes += " gy"
    return f'<div class="{classes}">&nbsp;</div>'


def color_cell(
    star="*", center=False, legend=False, thread=False, guide=[False, False]
):
    if legend:
        td = "td"
    else:
        td = "span"

    classes = f"s {star_class(star)}"
    if center:
        classes += " center"
    if guide[0]:
        classes += " gx"
    if guide[1]:
        classes += " gy"

    return f'<{td} class="{classes}"></{td}>'


def star_class(star):
    return f"u{hex(ord(star))[2:]}"


def color_cell2(rgb, icon, thread=False, center=False, legend=False):
    h = rgb2hex(rgb)
    if thread:
        return "<div class='color_cell cross_cell' style='background-color: {};'>&nbsp;</div>".format(
            h
        )

    # Render as chart
    if (rgb[0] * 0.299 + rgb[1] * 0.587 + rgb[2] * 0.114) > 186:
        text = "color: black"
    else:
        text = "color: lightgray"

    if center:
        border = "center"
    else:
        border = ""

    if legend:
        style = "td"
    else:
        style = "div"

    return "<{} class='color_cell {}' style='background-color: {}; {} '>{}</{}>".format(
        style, border, h, text, icon, style
    )


def base_path(path):
    return Path(pkg_resources.resource_filename("ih", path))
