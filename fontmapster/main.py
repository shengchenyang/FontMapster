import io
from math import ceil, sqrt
from typing import TYPE_CHECKING, List, Union

import numpy
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont, ImageOps

from fontmapster.common.typevars import FontCfgArgs, FontMapsterResult
from fontmapster.common.utils import Tools

__all__ = ["Mapster"]


if TYPE_CHECKING:
    from cnocr.cn_ocr import CnOcr
    from rapidocr_onnxruntime import RapidOCR

    from fontmapster.common.typevars import ocr_choicesT


class Mapster:
    ocr_cur: Union["RapidOCR", "CnOcr"]

    def __init__(
        self,
        font_path: str,
        img_size: int = 50,
        col_space: int = 0,
        row_space: int = 0,
        border_size: int = 0,
        skip: Union[int, List[int]] = 0,
        font_size_decrease: int = 0,
        ocr: "ocr_choicesT" = "rapidocr",
        show: bool = False,
    ) -> None:
        self._cfg = FontCfgArgs(
            img_size=img_size,
            col_space=col_space,
            row_space=row_space,
            border_size=border_size,
            skip=skip,
            font_size_decrease=font_size_decrease,
            ocr=ocr,
            show=show
        )

        self.font = TTFont(font_path)
        self.font_img = ImageFont.truetype(
            font_path, self._cfg.img_size - self._cfg.font_size_decrease
        )
        if self._cfg.ocr == "cnocr":
            import cnocr

            self.ocr_cur = cnocr.CnOcr(det_model_name="ch_PP-OCRv4")
        else:
            from rapidocr_onnxruntime import RapidOCR

            self.ocr_cur = RapidOCR()

    def get_map(self) -> FontMapsterResult:
        cmap_map = {}
        cmap_uni_map = {}
        cmap_hex_map = {}
        glyph_map = {}
        for cmap_code, glyph_name in self.font.getBestCmap().items():
            character_key = chr(cmap_code)
            # 如果值中以 uni 开头，那么把他直接转为汉字
            if glyph_name.startswith("uni"):
                character_value = chr(int(glyph_name[3:], 16))
            else:
                character_value = glyph_name
            cmap_map[cmap_code] = character_value
            cmap_uni_map[character_key] = character_value
            cmap_hex_map[hex(cmap_code)] = character_value
            glyph_map[glyph_name] = character_value

        result = FontMapsterResult(
            glyph_map=glyph_map,
            cmap_map=cmap_map,
            cmap_uni_map=cmap_uni_map,
            cmap_hex_map=cmap_hex_map,
        )
        return result

    def get_ocr_map(self) -> FontMapsterResult:
        cmap_code_lst = []
        cmap_code_uni_lst = []
        cmap_code_hex_lst = []
        glyph_name_lst = []
        _skip_list = (
            [x - 1 for x in self._cfg.skip] if isinstance(self._cfg.skip, list) else []
        )
        count_num = -1
        img_datas = []
        for cmap_code, glyph_name in self.font.getBestCmap().items():
            count_num += 1
            if isinstance(self._cfg.skip, int):
                if count_num < self._cfg.skip:
                    continue
            elif isinstance(self._cfg.skip, list):
                if count_num in _skip_list:
                    continue

            txt = chr(cmap_code)
            cmap_code_lst.append(cmap_code)
            cmap_code_uni_lst.append(txt)
            cmap_code_hex_lst.append(hex(cmap_code))
            glyph_name_lst.append(glyph_name)

            img = Image.new("1", (self._cfg.img_size, self._cfg.img_size), 255)
            draw = ImageDraw.Draw(img)

            left, top, right, bottom = draw.textbbox(
                xy=(0, 0), text=txt, font=self.font_img
            )
            width, height = right - left, bottom - top

            # 计算文本的绘制位置，使其位于图像中心
            # 每种字体设计的不同，文本外部与基线可能有一定的距离，进一步调整位置
            x = (self._cfg.img_size - width) // 2 - left
            y = (self._cfg.img_size - height) // 2 - top

            draw.text(
                xy=(x, y),
                text=txt,
                font=self.font_img,
                fill=0,
            )
            img_byte = io.BytesIO()
            img.save(img_byte, format="PNG")
            img_datas.append(img_byte.getvalue())

        # Calculate the dimensions of the result image
        num_imgs = len(img_datas)
        side_length = ceil(sqrt(num_imgs))
        cols = side_length
        rows = ceil(num_imgs / cols)
        image_width = cols * self._cfg.img_size + (cols - 1) * self._cfg.col_space
        image_height = rows * self._cfg.img_size + (rows - 1) * self._cfg.row_space

        # Create a new blank image
        result_img = Image.new("RGB", (image_width, image_height), (255, 255, 255))

        # Paste each image into the result image
        for i, img_data in enumerate(img_datas):
            img = Image.open(io.BytesIO(img_data))
            col = i % cols
            row = i // cols
            x_offset = col * (self._cfg.img_size + self._cfg.col_space)
            y_offset = row * (self._cfg.img_size + self._cfg.row_space)

            result_img.paste(img, (x_offset, y_offset))

        if self._cfg.border_size:
            result_img = ImageOps.expand(
                result_img, self._cfg.border_size, (255, 255, 255)
            )

        # result_img.save("result_image.png")
        if self._cfg.show:
            result_img.show()

        # ocr
        if self._cfg.ocr == "cnocr":
            ocr_result = self.ocr_cur.ocr(img_fp=numpy.asarray(result_img))
            ocr_data = Tools.merge_cnocr_result(ocr_result)
            ocr_data_lst = list(ocr_data)
        else:
            ocr_result, elapse = self.ocr_cur(numpy.asarray(result_img))
            ocr_data = Tools.merge_rapidocr_result(ocr_result)
            ocr_data_lst = list(ocr_data)

        if len(glyph_name_lst) == len(ocr_data_lst):
            glyph_map = dict(zip(glyph_name_lst, ocr_data_lst))
            cmap_map = dict(zip(cmap_code_lst, ocr_data_lst))
            cmap_hex_map = dict(zip(cmap_code_hex_lst, ocr_data_lst))
            cmap_uni_map = dict(zip(cmap_code_uni_lst, ocr_data_lst))
            return FontMapsterResult(
                glyph_map=glyph_map,
                cmap_map=cmap_map,
                cmap_uni_map=cmap_uni_map,
                cmap_hex_map=cmap_hex_map,
            )
        return FontMapsterResult()
