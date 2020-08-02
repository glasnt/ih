"""
Helpers and values
"""
import os
import pkg_resources
from pathlib import Path

# A series of visually distinct characters, to populate the chart
STARS = [
    "✚", "❐", "◀", "♠", "✿", "⟘", "⟒", "⚉", "♣", "▷", "♦", "×", "⊔", 
    "⚑", "◼", "⬇", "⧓", "❤", "⟙", "✾", "∀", "⊕", "♥", "⇨", "⚇", "◼",
]

WHITESTAR = "·"


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
    color=None, star="*", center=False, legend=False, thread=False, guide=[False, False]
):
    if legend:
        td = "td"
    else:
        td = "span"

    if color == "#ffffff":
        star = WHITESTAR

    classes = f"s {star_class(star)}"
    if center:
        classes += " center"
    if guide[1]:
        classes += " gx"
    if guide[0]:
        classes += " gy"

    return f'<{td} class="{classes}"></{td}>'


def star_class(star):
    return f"u{hex(ord(star))[2:]}"


def base_path(path):
    return Path(pkg_resources.resource_filename("ih", path))
