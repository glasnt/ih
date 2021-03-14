import click

from ih import chart, palette


@click.command()
@click.argument("image", type=click.File('rb'))
@click.option(
    "--palette",
    "-p",
    default=chart.DEFAULT["palette"],
    show_default=True,
    type=click.Choice(palette.PALETTES + list(palette.PALETTE_OVERRIDE.keys())),
    help="Palette to use. See README.md for provenance",
)
@click.option(
    "--scale",
    "-s",
    default=chart.DEFAULT["scale"],
    show_default=True,
    help="Rescale factor",
)
@click.option(
    "--colors",
    "-c",
    default=chart.DEFAULT["colors"],
    show_default=True,
    help="Limit palette to at most N colors.",
)
@click.option(
    "--render",
    "-r",
    is_flag=True,
    default=chart.DEFAULT["render"],
    show_default=True,
    help="Render preview of resulting artwork",
)
@click.option(
    "--guidelines", "--print-ready",
    "-g",
    is_flag=True,
    default=chart.DEFAULT["guidelines"],
    show_default=True,
    help="Show guidelines, and print without colour",
)
@click.option(
    "--fileformat",
    "-o",
    type=click.Choice(chart.OUTPUT_FORMAT),
    default=chart.DEFAULT["fileformat"],
    show_default=True,
    help="Output file format",
)
@click.option('--outputfolder', '-f',
    default=chart.DEFAULT["outputfolder"],
    help="Output folder"
)
@click.version_option()
def main(image, palette, scale, colors, render, guidelines, fileformat, outputfolder):
    result = chart.chart(
        image=image,
        palette_name=palette,
        scale=scale,
        colors=colors,
        render=render,
        guidelines=guidelines,
        fileformat=fileformat,
        outputfolder=outputfolder
    )

    if fileformat == "html":
        print("Result: %s" % result)
    else:
        print(result)
