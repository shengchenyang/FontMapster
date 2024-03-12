from pathlib import Path

from fontTools.ttLib import TTFont

tests_dir = Path(__file__).parent


def to_woff(font_path, save_path):
    f = TTFont(font_path)
    f.flavor = "woff"
    f.save(save_path)
