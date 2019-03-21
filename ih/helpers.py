"""
Helpers and values
"""
import os
import pkg_resources
from pathlib import Path

# A series of visually distinct characters, to populate the chart
STARS = ['✚', '✽', '※', '✷', '❐', '❄', '✔', '◀', '⊐', '♠', '★', '»', '✿', '⟘',
         '❦', '⟒', '❦', '⚉', '♣', '▷', '♦', '×', '«', '△', '⊔', '➤', '⚑', '◼', 
         '⬇', '✭', '⧓', '❤', '✤', '⟙', '✾', '∀', '⊕', '♥', '⬆', '⚇', '◼', '✰']


def rgb2hex(pix):
    """Given a tuple of r, g, b, return the hex value """
    r, g, b = pix
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def color_cell(rgb, icon, thread=False, center=False):
    h = rgb2hex(rgb)
    if thread:
        return "<div class='color_cell cross_cell' style='background-color: {};'>&nbsp;</div>".format(h)

    # Render as chart
    if (rgb[0]*0.299 + rgb[1]*0.587 + rgb[2]*0.114) > 186:
        text = "color: black"
    else:
        text = "color: lightgray"

    if center:
        border = "center"
    else:
        border = ""
    return "<div class='color_cell {}' style='background-color: {}; {} '>{}</div>".format(border, h, text, icon)

def base_path(path):
    return Path(pkg_resources.resource_filename('ih', path))
