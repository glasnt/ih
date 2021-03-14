from click.testing import CliRunner
from pathlib import Path
from PIL import Image, ImageDraw

from ih.cli import main
from ih.palette import get_palette
from ih import helpers


from test_cli import runner, TEST_OUTPUT

s = 1 #square
length = 8
stars_image = "stars_image.png"

def test_stars():

    stars = len(helpers.STARS)
    w = length + 1
    h = int(stars/length) + 1

    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)

    # Draw palette from file
    palette = [tuple(x['rgb']) for x in get_palette("floss")][:(w*h)]

    ct = 0
    for i in range(0, w):
        for j in range(0, h):
            c = palette[ct] #(0, int(255/length * i), int(255/(stars/length) * j))
            ct += 1
            draw.polygon([(i,j),(i+s, j), (i, j+s), (i+s, j+s)], fill=c)

    path = Path(TEST_OUTPUT).parent.joinpath("images").joinpath(stars_image)
    img.save(path)
    runner(["-p", "floss", "-c", 256], image=str(path))


