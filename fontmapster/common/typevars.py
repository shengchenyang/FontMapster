from dataclasses import dataclass, field
from typing import List, Literal, NamedTuple, Optional, Union

ocr_choicesT = Literal["cnocr", "rapidocr"]


@dataclass
class FontCfgArgs:
    img_size: Optional[int] = field(default=50)
    col_space: Optional[int] = field(default=0)
    row_space: Optional[int] = field(default=0)
    border_size: Optional[int] = field(default=0)
    skip: Union[int, List[int]] = field(default=0)
    font_size_decrease: Optional[int] = field(default=0)
    ocr: Optional[ocr_choicesT] = field(default=None)
    show: bool = field(default=False)


class FontMapsterResult(NamedTuple):
    glyph_map: Optional[dict] = None
    cmap_map: Optional[dict] = None
    cmap_uni_map: Optional[dict] = None
    cmap_hex_map: Optional[dict] = None
