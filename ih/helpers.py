"""
Helpers and values
"""
from pathlib import Path
from ih.palette import *

# A series of visually distinct characters, to populate the chart
STARS = ['✚', '✽', '※', '✷', '❐', '❄', '✔', '◀', '⊐', '♠', '★', '»', '✿', '⟘',
         '❦', '⟒', '❦', '⚉', '♣', '▷', '♦', '×', '«', '△', '⊔', '➤', '⚑', '◼', 
         '⬇', '✭', '⧓', '❤', '✤', '⟙', '✾', '∀', '⊕', '♥', '⬆', '⚇', '◼', '✰']


def rgb2hex(pix):
    """Given a tuple of r, g, b, return the hex value """
    r, g, b = pix
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

PALETTE_DATA = {}

def thread_name(rgb, palette_name):
    #if not PALETTE_DATA:
    PALETTE_DATA = get_palette(palette_name)

    for t in PALETTE_DATA:
        if tuple(t['RGB']) == rgb:
            return t

    ## Return a basic thread type if thread not found in palette
    return {"Name": str(rgb), "Code": "???"}


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

