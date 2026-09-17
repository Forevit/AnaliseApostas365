import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_python_files_have_valid_syntax():
    for path in (ROOT / "scraper").glob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"))


def test_config_contains_expected_leagues():
    text = (ROOT / "scraper" / "config.py").read_text(encoding="utf-8")
    assert '"Serie B": 72,' in text
    assert '"Premier League": 39' in text
