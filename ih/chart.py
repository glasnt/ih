import json
import click
from textwrap import dedent

from PIL import Image

from math import ceil

from ih.palette import *
from ih.helpers import *

def chart(image_name, palette_name, scale, colours, render, fileformat="html", save=True):
    im = Image.open(image_name)

    chartimage = preprocess_image(im, palette_name=palette_name, colorlimit=colours, scale=scale)

    chart = generate_chart(chartimage, palette_name, render)

    if save:
        saved = save_chart(chart, image_name, fileformat)
        return saved
    else:
        return chart

def preprocess_image(image, palette_name="wool", colorlimit=256, scale=1):

    palette = get_palette_image(palette_name)

    # magic, 'cept grey
    im = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
    im = im.resize((int(im.width/scale), int(im.height/scale)))
    im = im.convert("RGB").convert('P', palette=Image.ADAPTIVE, colors=colorlimit).convert("RGB")

    _im = im.im.convert('P', 0, palette.im) # HACK, quantize fixes

    return im._new(_im).convert("RGB")


def generate_chart(chartimage, palette_name, render):
    histogram = sorted(chartimage.getcolors())

    html = ['<html><meta charset="utf-8">']

    with open(base_path('styling').joinpath("styling.css")) as s:
        html.append("<style>" + "".join(s.readlines()) + "</style>")

    if render:
        html.append(dedent("""
            <style>.cross_cell { 
                background-image: url('%s'); 
                background-size: cover; 
                border: none; 
            }</style>
            """ % get_thread_path(palette_name)))

    legend = {}
    for idx, x in enumerate(histogram):
        legend[rgb2hex(x[1])] = STARS[idx % len(STARS)]
    
    html.append('<table><tr><td class="zztop"><table class="legend">')
    html.append(('<tr><td>X</td><td># sts</td><td>skeins</td>'
                '<td>{} code</td><td>{} name</td></tr>').format(palette_name, palette_name))

    for idx, h in enumerate(reversed(histogram)):
        count, rgb = h
        color = rgb2hex(rgb)
        thread = thread_name(rgb, palette_name)
        name, code = (thread["Name"], thread["Code"])
        skeins = ceil(count / 1000)

        html.append('<tr><td style="padding:0">' + color_cell(rgb, legend[color], thread=False) + '</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><tr>'.format(count, skeins, code, name))
      

    html.append('</table><br>Image width: {}<br>Image height: {}<br><br>Generated by Experiment 626 ✨'
        .format(chartimage.width, chartimage.height))
    html.append('</td><td class="zztop space"><table class="chart">') 

    CENTER = True
    for x in range(0, chartimage.width):
        row = []
        for y in range(0, chartimage.height):
            rgb = chartimage.getpixel((x,y))
            p = rgb2hex(rgb)

            center_flag = False
            if CENTER:
                if chartimage.height / 2 <= y and chartimage.width / 2 <= x:
                    center_flag = True
                    CENTER = False

            row.append(color_cell(rgb, legend[p], thread=thread, center=center_flag))

        html.append("<div>" + "".join(row) + "</div>")
    html.append("</table></td></table></html>")
    return "\n".join(html) 

def save_chart(html, image, fileformat):
    if fileformat == "html":
        outfile = '{}.html'.format("_".join(image.split("/")[-1].split(".")[:-1]))

        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(html)

    return outfile

