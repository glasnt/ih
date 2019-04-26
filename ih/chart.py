import json
import click
from textwrap import dedent


from PIL import Image, ImageOps

from math import ceil, floor

from ih.palette import *
from ih.helpers import *

# Guideline padding
GUIDE = 10

# Assuming no colour will be this in our palette.
GUIDECOL = (0, 0, 0, 0)


def chart(
    image_name=None,
    image_obj=None,
    palette_name="wool",
    scale=1,
    colours=256,
    render=False,
    guidelines=False,
    fileformat="html",
    save=True,
):
    # can't have both guidelines and rendering
    if render:
        guidelines = False

    if image_name:
        im = Image.open(image_name)
    elif image_obj:
        im = image_obj
    else:
        raise ValueError("Must provide an image filename or Image object")

    palette = get_palette(palette_name)
    chartimage = preprocess_image(
        im, palette=palette, colorlimit=colours, scale=scale, guidelines=guidelines
    )

    chart = generate_chart(chartimage, palette_name, palette, render, guidelines)

    if save:
        saved = save_chart(chart, image_name, fileformat)
        return saved
    else:
        return chart


def preprocess_image(image, palette=None, colorlimit=256, scale=1, guidelines=False):
    palette_image = get_palette_image(palette)
    im = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
    im = im.resize((int(im.width / scale), int(im.height / scale)))

    im = (
        im.convert("RGB")
        .convert("P", palette=Image.ADAPTIVE, colors=colorlimit)
        .convert("RGB")
    )

    _im = im.im.convert("P", 0, palette_image.im)

    return im._new(_im).convert("RGB")


def generate_chart(chartimage, palette_name, palette, render=False, guidelines=False):
    histogram = sorted(chartimage.getcolors())

    html = ['<html><meta charset="UTF-8">']

    with open(base_path("styling").joinpath("styling.css")) as s:
        html.append("<style>" + "".join(s.readlines()) + "</style>")

    if render:
        html.append(
            dedent(
                """
            <style>
            .s {  
                background-image: url('%s'); 
                background-size: cover; 
                border: none; 
            }
            .r { border: none }
            .chart { border: 1px solid black }
            </style>
            """
                % get_thread_image(palette_name)
            )
        )

    legend = {}
    styles = {}
    after = {}
    for idx, x in enumerate(histogram):
        rgb = x[1]
        h = rgb2hex(rgb)
        star = STARS[idx % len(STARS)]
        sclass = star_class(star)

        # Choose the best text colour
        if (rgb[0] * 0.299 + rgb[1] * 0.587 + rgb[2] * 0.114) > 186:
            color = "black"
        else:
            color = "lightgray"
        styles[sclass] = {"bg": h, "c": color, "star": star}

        legend[rgb2hex(x[1])] = STARS[idx % len(STARS)]

    html.append("<style>")
    for _, x in enumerate(styles):
        y = styles[x]

        html.append(".%s { background-color: %s; color: %s }" % (x, y["bg"], y["c"]))
        if not render:
            html.append('.%s::after { content: "%s" }' % (x, y["star"]))

    html.append("</style>")

    html.append('<div class="container">')
    html.append('<div class="left-content">')
    html.append('<div class="legend_div"><table class="legend">')
    html.append(
        (
            f"<tr><td>X</td><td class='label'>{get_identity_name(palette_name)}</td>"
            f"<td class='label'>{palette_name} code</td></tr>"
        )
    )

    # Generate legend
    for idx, h in enumerate(reversed(histogram)):
        count, rgb = h
        color = rgb2hex(rgb)
        thread = thread_name(rgb, palette)
        code = thread["code"]

        html.append(
            "<tr>"
            + color_cell(legend[color], thread=False, legend=True)
            + "<td>{}</td><td>{}</td></tr>".format(count, code)
        )

    html.append("</table></div>")

    # Debug
    import pkg_resources
    ih_version = pkg_resources.require("ih")[0].version
    html.append(
        f'<div class="debug">Image: {chartimage.width} x {chartimage.height}. ih version {ih_version}</div>'
    )
    html.append('</div>') # end left-content

    html.append('<div class="right-content"><div class="chart">')

    if guidelines:
        chartimage = chartimage.convert("RGBA")
        xpad = GUIDE - (chartimage.width % GUIDE)
        ypad = GUIDE - (chartimage.height % GUIDE)

        padding = (floor(ypad / 2), ceil(xpad / 2), ceil(ypad / 2), floor(xpad / 2))

        chartimage = ImageOps.expand(chartimage, padding, fill=GUIDECOL)

    CENTER = True

    for x in range(0, chartimage.width):
        row = []
        for y in range(0, chartimage.height):

            guide_x, guide_y = False, False
            if guidelines:
                if x % GUIDE == GUIDE - 1:
                    guide_x = True
                if y % GUIDE == GUIDE - 1:
                    guide_y = True

            rgb = chartimage.getpixel((x, y))

            if rgb == GUIDECOL:
                row.append(guide_cell([guide_x, guide_y]))
                continue
            p = rgb2hex(rgb)

            center_flag = False
            if not render:
                if CENTER:
                    if chartimage.height / 2 - 1 <= y and chartimage.width / 2 - 1 <= x:
                        center_flag = True
                        CENTER = False

            row.append(
                color_cell(star=legend[p], center=center_flag, guide=[guide_x, guide_y])
            )

        html.append("<div class='r'>" + "".join(row) + "</div>")
    html.append("</div></div></div></html>")
    return "\n".join(html)


def save_chart(html, image, fileformat):
    if fileformat == "html":
        outfile = "{}.html".format("_".join(image.split("/")[-1].split(".")[:-1]))

        with open(outfile, "w", encoding="utf-8") as f:
            f.write(html)

    return outfile
