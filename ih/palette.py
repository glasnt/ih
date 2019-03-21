# Available palettes
import json
from PIL import Image
from ih.helpers import base_path

PALETTES = []
PALETTE_DIR = base_path('palettes')

for f in PALETTE_DIR.glob("*.json"):
    PALETTES.append(f.stem)

# Palette overrides (emoji)
PALETTE_OVERRIDE = {
    "🧵": "floss",
    "🧶": "wool",
    "🦙": "alpaca"
}

# Thread render overrides
THREAD_DEFAULT = "wool.png"
THREAD_OVERRIDE = {
    "floss": "floss.png"
}

def get_thread_path(palette_name):
    thread_image = THREAD_DEFAULT
    if palette_name in THREAD_OVERRIDE:
        thread_image = THREAD_OVERRIDE[palette_name]
    return str(base_path('styling').joinpath(thread_image))

def get_palette(palette_name):
    if palette_name in PALETTE_OVERRIDE.keys():
        palette = PALETTE_OVERRIDE[palette_name]

    if palette_name not in PALETTES:
        raise ValueError("Invalid palette: %s. Choices: %s" % (palette_name, ", ".join(PALETTES)))

    with open(PALETTE_DIR.joinpath("%s.json" % palette_name)) as f:
        palette = json.load(f)

    return palette

def get_palette_image(palette_name):
    palette = get_palette(palette_name)
    data = sum([x['RGB'] for x in palette], [])[:256]

    image = Image.new('P', (16,16))
    image.putpalette(data)
    return image

def display_palette(palette_name):
    palette = get_palette(palette_name)
    print(json.dumps(palette))
    # TODO visualise

PALETTE_DATA = {}

def thread_name(rgb, palette_name):
    #if not PALETTE_DATA:
    PALETTE_DATA = get_palette(palette_name)

    for t in PALETTE_DATA:
        if tuple(t['RGB']) == rgb:
            return t

    ## Return a basic thread type if thread not found in palette
    return {"Name": str(rgb), "Code": "???"}

