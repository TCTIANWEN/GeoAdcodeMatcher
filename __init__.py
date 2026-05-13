"""
geoadcode_matcher - 行政区划代码匹配工具
通过省、市、县/区名称模糊匹配对应的行政区划代码
"""

__version__ = "1.0.0"

from .matcher import AdcodeMatcher
from .utils import match_csv, match_dataframe, read_csv_with_fallback

__all__ = ['AdcodeMatcher', 'match_csv', 'match_dataframe', 'read_csv_with_fallback']
