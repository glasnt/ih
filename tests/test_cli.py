from click.testing import CliRunner
from ih.cli import main


def test_image():
    runner = CliRunner()
    result = runner.invoke(main, ["test_image.png"])
    assert result.exit_code == 0
    assert result.output == "Result: test_image.html\n"


def test_render():
    runner = CliRunner()
    result = runner.invoke(main, ["test_image.png", "-r"])
    assert result.exit_code == 0
    assert result.output == "Result: test_image.html\n"


def test_guidelines():
    runner = CliRunner()
    result = runner.invoke(main, ["test_image.png", "-g"])
    assert result.exit_code == 0
    assert result.output == "Result: test_image.html\n"
