# GeoAdcodeMatcher

行政区划代码匹配工具 - 通过省、市、县/区名称模糊匹配对应的行政区划代码。

## 功能特点

- **模糊匹配**：即使输入的名称有细微差异也能正确匹配
- **多种编码支持**：自动识别 UTF-8、GBK、GB2312 等常见编码
- **自动识别列名**：能够识别常见的省、市、县列名格式
- **两种使用方式**：GUI 界面和命令行接口
- **灵活定制**：支持指定列名和对照表路径

## 安装

```bash
pip install geoadcode-matcher
```

或直接从源码安装：

```bash
git clone https://github.com/YOUR_USERNAME/GeoAdcodeMatcher.git
cd GeoAdcodeMatcher
pip install -e .
```

## 使用方法

### Python API

```python
from geoadcode_matcher import AdcodeMatcher, match_dataframe

# 使用 AdcodeMatcher 类
import pandas as pd
codebook = pd.read_csv('discode_ans-2023.csv')
matcher = AdcodeMatcher(codebook)
result = matcher.find_code('广东省', '深圳市', '南山区')
print(result)  # ('440305', '广东省', '深圳市', '南山区')

# 对 DataFrame 进行批量匹配
df = pd.DataFrame({
    'province': ['广东省', '北京市'],
    'city': ['深圳市', '北京市'],
    'county': ['南山区', '朝阳区']
})
result_df = match_dataframe(df, matcher, 'province', 'city', 'county')
print(result_df)
```

### 命令行

```bash
python -m geoadcode_matcher.cli input.csv -c discode_ans-2023.csv
```

### GUI 界面

```bash
python -m geoadcode_matcher
```

## 输入文件格式

### 用户 CSV 文件

需要包含省、市、县/区列，支持以下列名：

- 省: `province`、`省`、`省份`、`所在省`、`所属省份` 等
- 市: `city`、`市`、`城市`、`所在市`、`所属城市` 等
- 县/区: `county`、`区县`、`县区`、`区`、`县`、`所在区县`、`所属区县` 等

### 区划对照表格式

必须包含列: `province`, `city`, `county`, `code`

## 许可证

MIT License