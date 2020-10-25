from click.testing import CliRunner
from ih.cli import main


TEST_IMAGE = "test_image.png"
TEST_HTML = TEST_IMAGE.split(".")[0] + ".html"


def runner(args):
    runner = CliRunner()
    result = runner.invoke(main, [TEST_IMAGE] + args)
    assert result.exit_code == 0
    assert result.output == f"Result: {TEST_HTML}\n"


def test_image():
    runner([])


def test_render():
    runner(["-r"])


def test_guidelines():
    runner(["-g"])
