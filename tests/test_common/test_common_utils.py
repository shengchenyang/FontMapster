from fontmapster.common.utils import Tools


def test_uni_to_chr():
    res = Tools.uni_to_chr(uni="uniE8CD")
    assert res == ""
