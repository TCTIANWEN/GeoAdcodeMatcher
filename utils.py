"""
行政区划匹配工具函数
"""

from pathlib import Path
from typing import List, Optional

import pandas as pd

from .matcher import AdcodeMatcher

COMMON_PROVINCE_COLS = ['province', '省', '省份', '所在省', '所属省份', 'Province', 'PROVINCE', 'C1']
COMMON_CITY_COLS = ['city', '市', '城市', '所在市', '所属城市', 'City', 'CITY', 'C2']
COMMON_COUNTY_COLS = ['county', '区县', '县区', '区', '县', '所在区县', '所属区县', 'district', 'area', 'County', 'COUNTY', 'District', 'DISTRICT', 'C3']


def detect_column(columns: List[str], candidates: List[str], required: bool = True) -> Optional[str]:
    """根据候选列名列表自动识别匹配的列名"""
    clean_to_original = {}
    for col in columns:
        clean = str(col).strip().replace('﻿', '')
        clean_to_original[clean] = col
        clean_to_original[clean.lower()] = col

    for name in candidates:
        if name in clean_to_original:
            return clean_to_original[name]
        lowered = str(name).strip().lower()
        if lowered in clean_to_original:
            return clean_to_original[lowered]

    if required:
        raise ValueError(f'无法自动识别列名。当前列为: {columns}')
    return None


def read_csv_with_fallback(path: Path) -> pd.DataFrame:
    """尝试多种编码读取 CSV 文件"""
    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'ansi']
    last_error = None
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception as e:
            last_error = e
    raise RuntimeError(f'读取 CSV 失败：{path}\n最后一次报错：{last_error}')


def match_dataframe(
    input_df: pd.DataFrame,
    matcher: AdcodeMatcher,
    province_col: str,
    city_col: str,
    county_col: Optional[str],
    code_col: str = 'adcode',
    matched_province_col: str = 'matched_province',
    matched_city_col: str = 'matched_city',
    matched_county_col: str = 'matched_county',
) -> pd.DataFrame:
    """对 DataFrame 中的每一行进行行政区划代码匹配"""
    df = input_df.copy()

    codes: List[str] = []
    provinces: List[str] = []
    cities: List[str] = []
    counties: List[str] = []

    for _, row in df.iterrows():
        county_value = row.get(county_col, '') if county_col else ''
        result = matcher.find_code(row.get(province_col, ''), row.get(city_col, ''), county_value)
        if result:
            code, m_pro, m_city, m_county = result
            codes.append(code)
            provinces.append(m_pro)
            cities.append(m_city)
            counties.append(m_county)
        else:
            codes.append('')
            provinces.append('')
            cities.append('')
            counties.append('')

    df[code_col] = codes
    df[matched_province_col] = provinces
    df[matched_city_col] = cities
    df[matched_county_col] = counties
    return df


def match_csv(
    input_path: Path,
    codebook_path: Path,
    province_col: Optional[str] = None,
    city_col: Optional[str] = None,
    county_col: Optional[str] = None,
) -> pd.DataFrame:
    """
    读取 CSV 文件并进行行政区划代码匹配

    Args:
        input_path: 输入 CSV 文件路径
        codebook_path: 行政区划对照表路径
        province_col: 省列名，如不指定则自动识别
        city_col: 市列名，如不指定则自动识别
        county_col: 县/区列名，如不指定则自动识别

    Returns:
        添加了匹配结果的 DataFrame
    """
    input_df = read_csv_with_fallback(input_path)
    codebook_df = read_csv_with_fallback(codebook_path)

    if province_col is None:
        province_col = detect_column(list(input_df.columns), COMMON_PROVINCE_COLS)
    if city_col is None:
        city_col = detect_column(list(input_df.columns), COMMON_CITY_COLS)
    if county_col is None:
        county_col = detect_column(list(input_df.columns), COMMON_COUNTY_COLS, required=False)

    matcher = AdcodeMatcher(codebook_df)
    return match_dataframe(
        input_df=input_df,
        matcher=matcher,
        province_col=province_col,
        city_col=city_col,
        county_col=county_col,
    )
