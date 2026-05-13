# GeoAdcodeMatcher

行政区划代码匹配工具 - 通过省、市、县/区名称模糊匹配对应的行政区划代码。

## 功能特点

- 支持模糊匹配：即使输入的名称有细微差异也能正确匹配
- 多种编码支持：自动识别 UTF-8、GBK、GB2312 等常见编码
- 自动识别列名：能够识别常见的省、市、县列名格式
- 两种使用方式：GUI 界面和命令行接口
- 灵活定制：支持指定列名和对照表路径

## 安装

```bash
pip install GeoAdcodeMatcher
```

或直接从源码安装：

```bash
git clone https://github.com/yourusername/GeoAdcodeMatcher.git
cd GeoAdcodeMatcher
pip install -e .
```

## 使用方法

### GUI 界面

安装后直接运行：

```bash
python -m GeoAdcodeMatcher
```

或运行主脚本：

```bash
python GeoAdcodeMatcher/__main__.py
```

### 命令行

```bash
# 基本用法
python -m GeoAdcodeMatcher.cli input.csv

# 指定区划对照表
python -m GeoAdcodeMatcher.cli input.csv -c discode_ans-2023.csv

# 指定输出文件
python -m GeoAdcodeMatcher.cli input.csv -o output.csv

# 指定列名
python -m GeoAdcodeMatcher.cli input.csv --province-col 省 --city-col 市 --county-col 区县
```

### Python API

```python
from GeoAdcodeMatcher import AdcodeMatcher, match_csv

# 方式一：使用便捷函数
result_df = match_csv('input.csv', 'discode_ans-2023.csv')
result_df.to_csv('output.csv', index=False)

# 方式二：使用 AdcodeMatcher 类
import pandas as pd
codebook_df = pd.read_csv('discode_ans-2023.csv')
matcher = AdcodeMatcher(codebook_df)
result = matcher.find_code('广东省', '深圳市', '南山区')
print(result)  # ('440305', '广东省', '深圳市', '南山区')
```

## 输入文件格式

输入 CSV 文件应包含省、市、县/区列，支持以下列名：

- 省：`province`、`省`、`省份`、`所在省`、`所属省份` 等
- 市：`city`、`市`、`城市`、`所在市`、`所属城市` 等
- 县/区：`county`、`区县`、`县区`、`区`、`县`、`所在区县`、`所属区县` 等

## 区划对照表

区划对照表需要包含以下列：

- `province`：省份名称
- `city`：城市名称
- `county`：县/区名称
- `code`：行政区划代码（6位数字）

可以使用自带的 `discode_ans-2023.csv` 作为对照表。

## 许可证

MIT License
