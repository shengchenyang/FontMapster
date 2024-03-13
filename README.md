# FontMapster 项目说明

![license](https://img.shields.io/github/license/shengchenyang/FontMapster)
![python support](https://img.shields.io/badge/python-3.8%2B-blue)
![codecov](https://codecov.io/gh/shengchenyang/FontMapster/graph/badge.svg?token=SdVS49h3hd)

## 简介

`fontmapster` 是一个获取动态字体映射的工具，包含通过非 `ocr` 及 `ocr` 通用的方式来获取动态字体加密的真实映射功能。

## 安装

> 简洁安装，不使用 ocr 的方法时推荐安装此便携版：

```
pip install fontmapster
```

> 单使用 rapidocr ocr 的方式时：

```
pip install fontmapster[rapidocr]
```

> 单使用 cnocr ocr 的方式时：

```
pip install fontmapster[cnocr]
```

> 安装所有依赖的方式：

```
pip install fontmapster[all]
```

## 简单示例

> 具体示例请在 tests 的测试文件中查看。

1. 普通场景：

   一般是比较标准的字体文件，可以通过通用的方法高效地得到映射。

2. `ocr` 场景：

   在非标准字体文件，或者在一些字体不常变动的站点想快速得到结果时使用。

> 补充说明：

在 `ocr` 场景中可以很方便地调整字体大小，行间距，列间距等参数来提高 `ocr` 工具识别准确率。

比如以下由两个不同设置得到的图示（可以通过 `show` 参数在调试时使用）。

<div>
    <img src=".\examples\result1.png" style="float: left; width: 45%">
    <img src=".\examples\result2.png" style="float: left; width: 45%">
</div>
