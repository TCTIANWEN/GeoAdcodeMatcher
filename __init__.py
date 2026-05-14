"""
geoadcode_matcher - 行政区划代码匹配工具
通过省、市、县/区名称模糊匹配对应的行政区划代码

即插即用：数据已内置，无需额外下载或配置。

使用方式（任意目录）：
    import sys
    from pathlib import Path
    skill_dir = Path('~/.claude/skills/geoadcode-matcher').expanduser()
    sys.path.insert(0, str(skill_dir))
    from geoadcode_matcher import AdcodeMatcher, get_bundled_codebook
"""

import importlib.resources
from pathlib import Path

__version__ = "1.1.0"

try:
    from .matcher import AdcodeMatcher
    from .utils import match_csv, match_dataframe, read_csv_with_fallback, detect_column
    from .utils import get_bundled_codebook, get_default_codebook
except ImportError:
    # 非包模式运行（如直接python运行或sys.path插入）
    import matcher
    import utils
    AdcodeMatcher = matcher.AdcodeMatcher
    match_csv = utils.match_csv
    match_dataframe = utils.match_dataframe
    read_csv_with_fallback = utils.read_csv_with_fallback
    detect_column = utils.detect_column
    get_bundled_codebook = utils.get_bundled_codebook
    get_default_codebook = utils.get_default_codebook

__all__ = ['AdcodeMatcher', 'match_csv', 'match_dataframe', 'read_csv_with_fallback', 'get_bundled_codebook', 'detect_column']


def get_bundled_codebook() -> Path:
    """
    获取内置的行政区划对照表路径。

    Returns:
        Path: discode_ans-2023.csv 的路径
    """
    return Path(__file__).parent / "discode_ans-2023.csv"


def get_default_codebook() -> Path:
    """兼容性别名"""
    return get_bundled_codebook()