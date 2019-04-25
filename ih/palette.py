# Available palettes
import csv
import base64
from PIL import Image
from ih.helpers import base_path, hex2rgb

PALETTES = []
PALETTE_DIR = base_path("palettes")

for f in PALETTE_DIR.glob("*.txt"):
    PALETTES.append(f.stem)

# Palette overrides (emoji)
PALETTE_OVERRIDE = {"🧵": "floss", "🧶": "wool", "🦙": "alpaca"}


THREAD_DEFAULT = "wool.png"
THREAD_OVERRIDE = {}
for p in PALETTES:
    img = base_path("styling").joinpath(f"{p}.png")
    if img.exists():
        THREAD_OVERRIDE[p] = img


DEFAULT_IDENTITY = "stitches"
IDENTITY_OVERRIDE = {"lego": "bricks", "perler": "beads"}


# Return the name of the identity. E.g, floss is stitches, lego is bricks
def get_identity_name(palette_name):
    if palette_name in IDENTITY_OVERRIDE.keys():
        return IDENTITY_OVERRIDE[palette_name]
    else:
        return DEFAULT_IDENTITY


# Return the location of the image for the mock representation of the thread.
def get_thread_image_path(palette_name):
    thread_image = THREAD_DEFAULT
    if palette_name in THREAD_OVERRIDE:
        return THREAD_OVERRIDE[palette_name]
    return str(base_path("styling").joinpath(thread_image))


def get_thread_image(palette_name):
    path = get_thread_image_path(palette_name)
    with open(path, "rb") as f:
        image = str(base64.b64encode(f.read())).strip("b'").strip("'")
    return f"data:image/png;base64,{image}"


def get_palette(palette_name):
    if palette_name in PALETTE_OVERRIDE.keys():
        palette = PALETTE_OVERRIDE[palette_name]

    if palette_name not in PALETTES:
        raise ValueError(
            "Invalid palette: %s. Choices: %s" % (palette_name, ", ".join(PALETTES))
        )

    palette = []
    with open(PALETTE_DIR.joinpath(f"{palette_name}.txt")) as f:
        data = csv.reader(f, delimiter=",")
        for line in data:
            code, h = line
            rgb = hex2rgb(h)
            palette.append({"rgb": rgb, "hex": h, "code": code})

    return palette


# get a base image that had the palette we want
# Math involved:
# putpalette requires a flattened list of up to 256 triples for RGB
# so:
#  * get our RGB values
#  * flatten
#  * pad the list to 256 triples, if required
#  * then cut the list, if required.
# The result will always be length 256 * 3
# Math: https://stackoverflow.com/a/55755789/124019
def get_palette_image(palette):
    data = (
        sum([x["rgb"] for x in palette], [])
        + (palette[-1]["rgb"] * (256 - len(palette)))
    )[: 256 * 3]
    image = Image.new("P", (16, 16))
    image.putpalette(data)

    return image


def thread_name(rgb, palette):
    for t in palette:
        if tuple(t["rgb"]) == rgb:
            return t

    ## Return a basic thread type if thread not found in palette
    return {"code": str(rgb)}
