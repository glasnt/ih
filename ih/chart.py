import json
import click
from textwrap import dedent
from pathlib import Path

import os
from tabulate import tabulate
from PIL import Image, ImageOps

from math import ceil, floor

from ih import palette, helpers

DEFAULT = {
    "palette": palette.PALETTE_DEFAULT,
    "scale": 1,
    "colors": 256,
    "render": False,
    "guidelines": False,
    "fileformat": "html",
    "outputfolder": '.',
}

OUTPUT_FORMAT = ["html", "term"]

# Guideline padding
GUIDE = 10

# Assuming no colour will be this in our palette.
GUIDECOL = (0, 0, 0, 0)


def nicename(image_name): 
    if hasattr(image_name, "name"):
        image_name = image_name.name
    return Path(image_name).name



def debug_data(image_name, scale, colors, palette_name, chartimage, colorsused, fileformat="html"):
    import pkg_resources

    ih_version = pkg_resources.require("ih")[0].version
    data = [
        f"Image: {nicename(image_name)}",
        f"Scale: {scale}x",
        f"Image size: {chartimage.height} x {chartimage.width}",
        f"Palette: {palette_name}",
        f"Colors used: {colorsused} (of possible {colors})",
        f"ih version: {ih_version}",
    ]
    if fileformat == "html":
        return f'<div class="debug">' + "<br />".join(data) + "</div>"
    else:
        return "\n".join(data)


def preprocess_image(
    im,
    pal,
    colors=DEFAULT["colors"],
    scale=DEFAULT["scale"],
    guidelines=DEFAULT["guidelines"],
):
    # Reduce palette to max 256 colors
    reduced_palette = palette.reduce_palette(palette=pal, image=im)
    palette_image = palette.get_palette_image(reduced_palette)
    im = im.resize((int(im.width / scale), int(im.height / scale)))

    # Remove black transparency issues with this one weird trick.
    alpha = im.convert("RGBA").split()[-1]
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.paste(im, mask=alpha)
    im = bg

    im = (
        im.convert("RGB")
        .convert("P", palette=Image.ADAPTIVE, colors=colors)
        .convert("RGB")
    )

    _im = im.im.convert("P", 0, palette_image.im)

    return im._new(_im).convert("RGB")


def get_legend(chartimage):
    legend = {}
    styles = {}
    histogram = sorted(chartimage.getcolors())
    STARS = helpers.STARS
    for idx, x in enumerate(histogram):
        rgb = x[1]
        h = helpers.rgb2hex(rgb)
        star = STARS[idx % len(STARS)]
        sclass = helpers.col_class(h)

        # Choose the best text colour
        if (rgb[0] * 0.299 + rgb[1] * 0.587 + rgb[2] * 0.114) > 186:
            color = "black"
        else:
            color = "lightgray"

        styles[sclass] = {"bg": h, "rgb": rgb, "c": color, "star": star}

        legend[helpers.rgb2hex(x[1])] = STARS[idx % len(STARS)]
    return legend, styles, histogram


def generate_html_chart(
    image_name,
    chartimage,
    palette_name,
    pal,
    render=False,
    guidelines=False,
    data="",
):

    html = [f'<html><meta charset="UTF-8" /><title>ih - {nicename(image_name)}</title>']
    html.append('<link rel="icon" href="data:image/svg+xml,%3csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3e%3ctext y=%22.9em%22 font-size=%2290%22%3e%f0%9f%a7%b6%3c/text%3e%3c/svg%3e" />')

    with open(helpers.base_path("styling").joinpath("styling.css")) as s:
        html.append("<style>")
        if guidelines:
            html.append(":root { --border: lightgrey; }")
        else:
            html.append(":root { --border: black; }")
        html.append("".join(s.readlines()) + "</style>")

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
                % palette.get_thread_image(palette_name)
            )
        )

    legend, styles, histogram = get_legend(chartimage)
    after = {}

    html.append("<style>")
    for _, x in enumerate(styles):
        y = styles[x]

        html.append(".%s { background-color: %s; color: %s }" % (x, y["bg"], y["c"]))
        if not render:
            html.append('.%s::after { content: "%s\ufe0e" }' % (x, y["star"]))

    if not render:
        html.append(
            '.%s::after { content: "%s" }'
            % (helpers.col_class(helpers.WHITECOL), helpers.WHITESTAR)
        )

    html.append("</style>")

    html.append('<div class="container">')
    html.append('<div class="left-content">')
    html.append('<div class="legend_div"><table class="legend">')
    html.append(
        (
            f"<tr><td>X</td><td class='label'>{palette.get_identity_name(palette_name)}</td>"
            f"<td class='label'>{palette_name} code</td></tr>"
        )
    )

    # Generate legend
    for idx, h in enumerate(reversed(histogram)):
        count, rgb = h
        color = helpers.rgb2hex(rgb)
        thread = palette.thread_name(rgb, pal)
        code = thread["code"]

        html.append(
            "<tr>"
            + helpers.color_cell(
                color=color, star=legend[color], thread=False, legend=True
            )
            + "<td>{}</td><td>{}</td></tr>".format(count, code)
        )

    html.append("</table></div>")

    html.append(f'<div class="debug">{data}</div>')

    # If using guidelines, enable printhacks
    if guidelines:
        with open(helpers.base_path("styling").joinpath("styling.html")) as s:
            html.append("".join(s.readlines()))

    html.append("</div>")  # end left-content
    html.append("<div class='page-break'></div>")  # force page break

    html.append('<div class="right-content"><div class="chart">')

    # If using guidelines, expand the image to a whole number of guidelines first.
    if guidelines:
        chartimage = chartimage.convert("RGBA")
        xpad = GUIDE - (chartimage.width % GUIDE)
        ypad = GUIDE - (chartimage.height % GUIDE)

        padding = (floor(ypad / 2), ceil(xpad / 2), ceil(ypad / 2), floor(xpad / 2))

        chartimage = ImageOps.expand(chartimage, padding, fill=GUIDECOL)

    # Generate Chart (TODO(glasnt): make this less terrible)
    CENTER = True
    for y in range(0, chartimage.height):

        row = []

        for x in range(0, chartimage.width):
            guide_x, guide_y = False, False
            if guidelines:
                if x % GUIDE == GUIDE - 1:
                    guide_x = True
                if y % GUIDE == GUIDE - 1:
                    guide_y = True

            rgb = chartimage.getpixel((x, y))

            if rgb == GUIDECOL:
                row.append(helpers.guide_cell([guide_x, guide_y]))
                continue
            p = helpers.rgb2hex(rgb)

            center_flag = False
            if not render:
                if CENTER:
                    if chartimage.height / 2 - 1 <= y and chartimage.width / 2 - 1 <= x:
                        center_flag = True
                        CENTER = False

            row.append(
                helpers.color_cell(
                    color=p,
                    star=legend[p],
                    center=center_flag,
                    guide=[guide_x, guide_y],
                )
            )

        html.append("<div class='r'>" + "".join(row) + "</div>")
    html.append("</div></div></div></html>")
    return "\n".join(html)


def save_chart(html, image, fileformat, outputfolder):
    if fileformat == "html":
        os.makedirs(outputfolder, exist_ok=True)
        if type(image) == str: 
            imna = image
        else:
            imna = image.name
        fn = "_".join(imna.split("/")[-1].split(".")[:-1])
        outfile = os.path.join(outputfolder, f"{fn}.{fileformat}")

        with open(outfile, "w", encoding="utf-8") as f:
            f.write(html)

    return outfile


def generate_term_chart(chartimage, pal, render, palette_name, data):
    def c(text, bg=None, fg=None):
        def color(rgb, code):
            if not rgb:
                return ""
            R, G, B = rgb
            return f"\033[{code};2;{R};{G};{B}m"

        def foreground(rgb=None):
            return color(rgb, "38")

        def background(rgb=None):
            return color(rgb, "48")

        def reset():
            return "\033[0;00m"

        result = foreground(fg) + background(bg) + text + reset()
        return result

    def star(rgb, render=False):
        p = helpers.rgb2hex(rgb)
        if render:
            return c("  ", bg=rgb)
        else:
            return c(legend[p], fg=rgb) + " "

    legend, styles, histogram = get_legend(chartimage)

    headers = ["*", palette.get_identity_name(palette_name), f"{palette_name} code"]
    table = []
    result = "\n"

    for idx, h in enumerate(reversed(histogram)):
        count, rgb = h
        color = helpers.rgb2hex(rgb)
        thread = palette.thread_name(rgb, pal)
        code = thread["code"]
        symbol = star(rgb, render=render)

        table.append([symbol, str(count), code])

    result += tabulate(table, headers=headers)
    result += "\n\n"

    for y in range(0, chartimage.height):
        row = []
        for x in range(0, chartimage.width):
            rgb = chartimage.getpixel((x, y))
            row.append(star(rgb, render=render))

        result += "".join(row) + "\n"
    result += "\n" + data
    return result


def chart(
    image=None,
    image_obj=None,
    palette_name=DEFAULT["palette"],  # PALETTE_DEFAULT,
    scale=DEFAULT["scale"],
    colors=DEFAULT["colors"],
    render=DEFAULT["render"],
    guidelines=DEFAULT["guidelines"],
    fileformat=DEFAULT["fileformat"],
    outputfolder=DEFAULT["outputfolder"],
):
    # can't have both guidelines and rendering
    if render:
        guidelines = False

    image_name = image

    if image_name:
        im = Image.open(image_name)
    elif image_obj:
        im = image_obj
    else:
        raise ValueError("Must provide an image filename or Image object")

    pal = palette.get_palette(palette_name)
    chartimage = preprocess_image(
        im, pal=pal, colors=colors, scale=scale, guidelines=guidelines
    )

    data = debug_data(
        image_name=image_name,
        scale=scale,
        colors=colors,
        palette_name=palette_name,
        chartimage=chartimage,
        fileformat=fileformat,
        colorsused=len(sorted(chartimage.getcolors())),
    )

    if fileformat == "html":
        chart = generate_html_chart(
            image_name=image_name,
            chartimage=chartimage,
            palette_name=palette_name,
            pal=pal,
            render=render,
            guidelines=guidelines,
            data=data,
        )
        saved = save_chart(chart, image_name, fileformat, outputfolder)
        return saved
    elif fileformat == "term":
        chart = generate_term_chart(
            chartimage, pal=pal, render=render, palette_name=palette_name, data=data
        )
        return chart
