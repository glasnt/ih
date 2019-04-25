from ih.chart import *


@click.command()
@click.argument("image")
@click.option(
    "--palette",
    "-p",
    default="wool",
    help="Choices: %s. Default: wool" % ", ".join(PALETTES),
)
@click.option("--scale", "-s", default=1, help="Rescale factor. Default: 1")
@click.option(
    "--colours",
    "-c",
    default=256,
    help="Limit palette to at most N colors. Default: 256",
)
@click.option(
    "--render",
    "-r",
    is_flag=True,
    default=False,
    help="Render a preview (using thread images",
)
@click.option(
    "--guidelines", "-g", is_flag=True, default=False, help="Render guidelines"
)
def main(image, palette, scale, colours, render, guidelines):
    result = chart(
        image_name=image,
        palette_name=palette,
        scale=scale,
        colours=colours,
        render=render,
        guidelines=guidelines,
    )

    print("Result: %s" % result)
