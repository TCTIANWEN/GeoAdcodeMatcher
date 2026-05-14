# GeoAdcodeMatcher

行政区划代码匹配工具 - 通过省、市、县/区名称模糊匹配对应的 6 位行政区划代码。

## 即插即用（无需 pip 安装）

数据已内置，克隆仓库后直接使用：

```python
import sys
from pathlib import Path

# 将模块目录加入 Python 路径
skill_dir = Path('/path/to/GeoAdcodeMatcher').absolute()
sys.path.insert(0, str(skill_dir))

from geoadcode_matcher import AdcodeMatcher, get_bundled_codebook
import pandas as pd

# 读取内置区划表
codebook = pd.read_csv(get_bundled_codebook())

# 创建匹配器
matcher = AdcodeMatcher(codebook)

# 单条查询
result = matcher.find_code('广东省', '深圳市', '南山区')
print(result)  # ('440305', '广东省', '深圳市', '南山区')

# 批量 DataFrame 匹配
df = pd.DataFrame({
    'province': ['广东省', '北京市', '浙江省'],
    'city': ['深圳市', '北京市', '杭州市'],
    'county': ['南山区', '朝阳区', '西湖区']
})
result_df = match_dataframe(df, matcher, 'province', 'city', 'county')
print(result_df)
```

输出示例：

```
  province city county  adcode matched_province matched_city matched_county
0      广东省  深圳市    南山区  440305              广东省          深圳市            南山区
1      北京市  北京市    朝阳区  110105              北京市          北京市            朝阳区
2      浙江省  杭州市    西湖区  330106              浙江省          杭州市            西湖区
```

## 命令行使用

```bash
# 1个参数: input.csv -> input_matched.csv (内置区划表)
python cli.py input.csv

# 2个参数: input.csv output.csv (内置区划表)
python cli.py input.csv output.csv

# 3个参数: input.csv output.csv codebook.csv
python cli.py input.csv output.csv codebook.csv
```

## GUI 图形界面

```bash
python match_adcode_gui.py
```

启动后，程序会弹出文件选择对话框，请选择要处理的 CSV 文件。

## discode_ans-2023.csv 是什么？

本仓库附带的 `discode_ans-2023.csv` 是 2023 年中国行政区划对照表，包含以下字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| `code` | 6 位行政区划代码 | 440305 |
| `name` | 县/区名称 | 南山区 |
| `province` | 省份 | 广东省 |
| `city` | 城市 | 深圳市 |
| `county` | 县/区 | 南山区 |

该数据用于匹配查询，原始数据来源于国家统计局公布的行政区划代码，仅供个人研究学习使用。

## 功能特点

- **即插即用**：数据内置，无需额外下载或 pip 安装
- **模糊匹配**：即使输入的名称有细微差异（如"深圳市" vs "深圳"）也能正确匹配
- **智能纠错**：支持相似名称的模糊匹配，处理输入中的小误差
- **多种编码支持**：自动识别 UTF-8、GBK、GB2312 等常见 CSV 编码
- **自动识别列名**：能够识别常见的省、市、县列名格式，无需手动指定

## 输入文件格式

### 用户 CSV 文件要求

需要包含省、市、县/区至少前两列（县/区可选），支持以下列名自动识别：

| 层级 | 支持的列名 |
|------|-----------|
| 省 | `province`、`省`、`省份`、`所在省`、`所属省份`、`C1` |
| 市 | `city`、`市`、`城市`、`所在市`、`所属城市`、`C2` |
| 县/区 | `county`、`区县`、`县区`、`区`、`县`、`所在区县`、`C3` |

### 区划对照表格式

`discode_ans-2023.csv` 必须包含以下四列：

```csv
code,name,province,city,county
440305,南山区,广东省,深圳市,南山区
110105,朝阳区,北京市,北京市,朝阳区
330106,西湖区,浙江省,杭州市,西湖区
```

## 返回值说明

### find_code() 返回值

| 结果 | 返回值 |
|------|--------|
| 成功匹配 | `('行政代码', '匹配后的省', '匹配后的市', '匹配后的县/区')` |
| 匹配失败 | `None` |

### match_dataframe() 添加的列

| 列名 | 说明 |
|------|------|
| `adcode` | 行政区划代码（6位数字） |
| `matched_province` | 匹配后的省名（规范化） |
| `matched_city` | 匹配后的市名（规范化） |
| `matched_county` | 匹配后的县/区名（规范化） |

## 匹配规则

1. **精确匹配**：首先尝试精确匹配输入的省、市、县名称
2. **模糊匹配**：如果精确匹配失败，使用字符串相似度算法（difflib）进行模糊匹配
3. **包含匹配**：如果相似度匹配失败，尝试子字符串包含匹配
4. **去后缀匹配**：最后会去除常见行政后缀（省、市、县、区、州等）后重试匹配

## 免责声明

**重要**：本工具及附带的行政区划数据仅供参考和学习研究使用。

1. **准确性**：匹配结果可能存在误差，请勿将本工具用于需要高精度行政区划数据的正式场合（如法律文书、官方统计等）
2. **数据时效性**：附带的 `discode_ans-2023.csv` 数据截至 2023 年，可能与当前行政区划不完全一致
3. **非商用**：本项目和附带数据仅限个人研究学习使用，未经授权不得用于商业目的
4. **无担保**：作者不对使用本工具造成的任何直接或间接损失负责

如需最新和权威的行政区划信息，请查询：
- 国家统计局：http://www.stats.gov.cn
- 民政部：http://www.mca.gov.cn

## 许可证

MIT License