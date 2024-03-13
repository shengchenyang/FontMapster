import base64

from fontmapster import Mapster
from tests import tests_dir


def decode_unicode(html_txt, mapping):
    for key, value in mapping.items():
        html_txt = html_txt.replace("&#x{};".format(key[3:].lower()), value)
    return html_txt


def decode_hex(html_txt, mapping):
    for key, value in mapping.items():
        html_txt = html_txt.replace("&#x{};".format(key[2:].lower()), value)
    return html_txt


def test_ocr_maoyan():
    fm = Mapster(
        font_path=f"{tests_dir}/fonts/maoyan.woff",
        img_size=20,
        skip=1,
        ocr="cnocr",
    )
    font_mapster_res = fm.get_ocr_map()
    assert all(
        [
            font_mapster_res.glyph_map is not None,
            font_mapster_res.cmap_map is not None,
            font_mapster_res.cmap_hex_map is not None,
            font_mapster_res.cmap_uni_map is not None,
        ]
    )

    html_text = "&#xe3ec;&#xef28;&#xed30;.&#xe3df;&#xe3df;"
    res = decode_unicode(html_text, font_mapster_res.glyph_map)
    assert res == "281.77"


def test_ocr_58():
    font_base64 = """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"""

    font_data_after_decode = base64.b64decode(font_base64)
    new_font_name = f"{tests_dir}/fonts/58.woff"
    with open(new_font_name, "wb") as f:
        f.write(font_data_after_decode)

    fm = Mapster(
        font_path=f"{tests_dir}/fonts/58.woff",
        img_size=20,
        ocr="cnocr",
    )
    font_mapster_res = fm.get_ocr_map()
    html_txt = "&#x9f92;.&#x9476;"
    res = decode_hex(html_txt, font_mapster_res.cmap_hex_map)
    assert res == "3.5"


def test_ocr_xuanzhi():
    fm = Mapster(
        font_path=f"{tests_dir}/fonts/xz.woff",
        img_size=100,
        row_space=5,
        font_size_decrease=15,
        ocr="rapidocr",
    )
    font_mapster_res = fm.get_ocr_map()
    html_txt = "升镇.管"
    match_lst = [font_mapster_res.cmap_uni_map.get(x, x) for x in html_txt]
    res = "".join(match_lst)
    assert res == "25.4"


def test_ocr_other():
    no_use_fm = Mapster(
        font_path=f"{tests_dir}/fonts/maoyan.woff",
        img_size=20,
        col_space=4,
        row_space=5,
        border_size=5,
        skip=[1],
        font_size_decrease=1,
        ocr="cnocr",
        show=True,
    )
    _ = no_use_fm.get_ocr_map()

    fail_fm = Mapster(
        font_path=f"{tests_dir}/fonts/xz.woff",
        img_size=5,
        skip=[1, 3, 5],
        ocr="cnocr",
    )
    res = fail_fm.get_ocr_map()
    assert all(
        [
            res.glyph_map is None,
            res.cmap_map is None,
            res.cmap_hex_map is None,
            res.cmap_uni_map is None,
        ]
    )
