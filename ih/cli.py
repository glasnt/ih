import click

from ih import chart, palette


@click.command()
@click.argument("image")
@click.option(
    "--palette",
    "-p",
    default=chart.DEFAULT["palette"],
    show_default=True,
    type=click.Choice(palette.PALETTES),
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
    "--guidelines",
    "-g",
    is_flag=True,
    default=chart.DEFAULT["guidelines"],
    show_default=True,
    help="Show guidelines",
)
@click.option(
    "--print-ready",
    is_flag=True,
    default=chart.DEFAULT["print_ready"],
    help="Print black and white version",
)
@click.option(
    "--fileformat",
    "-o",
    type=click.Choice(chart.OUTPUT_FORMAT),
    default=chart.DEFAULT["fileformat"],
    show_default=True,
    help="Output file format",
)
@click.version_option()
def main(image, palette, scale, colors, render, guidelines, print_ready, fileformat):
    result = chart.chart(
        image_name=image,
        palette_name=palette,
        scale=scale,
        colors=colors,
        render=render,
        guidelines=guidelines,
        print_ready=print_ready,
        fileformat=fileformat,
    )

    if fileformat == "html":
        print("Result: %s" % result)
    else:
        return result
