from click.testing import CliRunner
from pathlib import Path
from PIL import Image, ImageDraw
from bs4 import BeautifulSoup as bs

from ih.cli import main
from ih.palette import get_palette
from ih import helpers


from test_cli import runner, TEST_OUTPUT

s = 1 #square
length = 8
stars_image = "stars_image.png"

def test_stars():
    # Build a unique image, with enough colours to use all stars and then some
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
            c = palette[ct] 
            ct += 1
            draw.polygon([(i,j),(i+s, j), (i, j+s), (i+s, j+s)], fill=c)

    path = Path(TEST_OUTPUT).parent.joinpath("images").joinpath(stars_image)
    img.save(path)

    # Generate Chart
    output = runner(["-p", "floss", "-c", 256], image=str(path))

    # Parse HTML into beautifulsoup
    html = Path(TEST_OUTPUT).joinpath(output)
    with open(html) as f:
        soup = bs(f, "html.parser")

    # Pull legend from HTML
    rows = soup.find("table", {"class": "legend"}).find_all("tr")

    # Can't compare Tags, so cast and sort
    def stringy(l):
        return sorted([str(x) for x in l])

    # Assert all rows in legend unique
    assert stringy(rows) == stringy(list(set(rows)))

    # Assert all elements in star column are unique
    stars = [ x.find('td') for x in rows ]
    assert stringy(stars) == stringy(list(set(stars)))

    # Assert colour count matches expectations
    starrows = len(rows) - 1 # remove header from counter
    assert starrows == ct 

    # Assert colour count matches shown
    assert str(starrows) in soup.find("div", {"class": "debug"}).text
