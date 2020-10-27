from click.testing import CliRunner
from ih.cli import main
from ih import palette


TEST_IMAGE = "test_image.png"
TEST_HTML = TEST_IMAGE.split(".")[0] + ".html"


def runner(args, output=TEST_HTML, print_output=False, image=TEST_IMAGE):
    runner = CliRunner()
    result = runner.invoke(main, [image] + args)
    if print_output:
        print(result.output)
    assert result.exit_code == 0
    assert output in result.output


def test_image():
    runner([])


def test_render():
    runner(["-r"])


def test_palettes():
    for p in palette.PALETTES:
        runner(["-p", p])
        runner(["-p", p, "-s", "25"], image="test_image.jpg")


def test_guidelines():
    runner(["-g"])


def test_thread():
    runner(["-p", "🧵"])


def test_alpaca():
    runner(["-p", "🦙"])


def test_wool():
    runner(["-p", "🧶"])


def test_term():
    runner(["-o", "term"], output="ih version")


def test_term_render():
    runner(["-o", "term", "-r"], output="ih version", print_output=True)
    runner(["-o", "term", "-r", "-s", "25"],
           output="ih version",
           print_output=True,
           image="test_image.jpg")
