import re

__all__ = ["Tools"]


class Tools:
    @staticmethod
    def uni_to_chr(uni: str) -> str:
        """将 Unicode 码位表示的字符串转换正常的字符，用于获取字体映射时使用"""
        _uni = re.sub(r"^(0x|U\+|uni)", "", uni)
        unicode_value = int(_uni, 16)
        # 使用 chr() 函数将整数值转换为字符
        return chr(unicode_value)

    @staticmethod
    def match_text(text, mapping):
        result = ""
        for char in text:
            if char in mapping:
                result += mapping[char]
            else:
                result += char
        return result

    @staticmethod
    def merge_cnocr_result(ocr_result: list) -> str:
        res = [x["text"] for x in ocr_result]
        return "".join(res)

    @staticmethod
    def merge_rapidocr_result(ocr_result: list) -> str:
        res = [x[-2] for x in ocr_result]
        return "".join(res)
