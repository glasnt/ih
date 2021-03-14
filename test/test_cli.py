from click.testing import CliRunner
from pathlib import Path

from ih.cli import main
from ih import palette



TEST_PNG = "test/images/smile.png"
TEST_JPG = "test/images/aurora.jpg"
TEST_OUTPUT = "test/output"

Path(TEST_OUTPUT).mkdir(exist_ok=True)

def get_test_html(image_src):
    return Path(image_src).stem + ".html"


def runner(args, print_output=False, image=TEST_PNG, output=None):
    if not output:
        output = get_test_html(image)
    args += ["-f", TEST_OUTPUT]
    runner = CliRunner()
    result = runner.invoke(main, [image] + args)
    if print_output:
        print(result.output)
    assert result.exit_code == 0
    assert output in result.output
    return output


def test_image():
    runner([])


def test_render():
    runner(["-r"])


def test_palettes():
    for p in palette.PALETTES:
        runner(["-p", p])
        runner(["-p", p, "-s", "25"], image=TEST_JPG)


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
           image=TEST_JPG)
