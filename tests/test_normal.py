from fontmapster import Mapster
from fontmapster.common.utils import Tools
from tests import tests_dir, to_woff


def test_normal_qxb():
    to_woff(
        f"{tests_dir}/fonts/qxb.woff2",
        f"{tests_dir}/fonts/qxb_search.woff",
    )

    fm = Mapster(font_path=f"{tests_dir}/fonts/qxb_search.woff")
    font_map = fm.get_map()
    html_text = "理度在线网络绍远（榆喀）漯汕皇徐"
    word = Tools.match_text(html_text, font_map.cmap_uni_map)
    assert word == "百度在线网络技术（北京）有限公司"

    # qxb detail page
    to_woff(
        f"{tests_dir}/fonts/qxb_detail.woff2",
        f"{tests_dir}/fonts/qxb_detail.woff",
    )
    fm = Mapster(font_path=f"{tests_dir}/fonts/qxb_detail.woff")
    font_map = fm.get_map()
    html_text = "lbjP 万美元"
    word = Tools.match_text(html_text, font_map.cmap_uni_map)
    assert word == "4520 万美元"


def test_normal_chacewang():
    fm = Mapster(font_path=f"{tests_dir}/fonts/chacewang.woff")
    font_map = fm.get_map()
    html_text = "膣臣舱脑舧舙臹膗腟芹"
    word = Tools.match_text(html_text, font_map.cmap_uni_map)
    assert word == "浙江至鑫建设有限公司"
