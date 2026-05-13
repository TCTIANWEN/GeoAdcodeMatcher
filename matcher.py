"""
行政区划代码匹配核心模块
"""

import difflib
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

DEL_WORDS = ['生产建设兵团', '地区', '自治区', '州', '县', '区', '市', '省', '镇', '乡', '洲']


class AdcodeMatcher:
    """行政区划代码匹配器"""

    def __init__(self, codebook_df: pd.DataFrame):
        self.wzdata = self._build_index(codebook_df)

    @staticmethod
    def _safe_str(value: Any) -> str:
        if pd.isna(value):
            return ''
        text = str(value).strip()
        if text.lower() == 'nan':
            return ''
        return text

    @staticmethod
    def _normalize_for_match(text: str) -> str:
        text = AdcodeMatcher._safe_str(text)
        for word in DEL_WORDS:
            text = text.replace(word, '')
        return text.strip()

    @staticmethod
    def _find_closest_string(target: Any, candidates) -> Optional[str]:
        target = AdcodeMatcher._safe_str(target)
        candidate_list = [AdcodeMatcher._safe_str(x) for x in list(candidates) if AdcodeMatcher._safe_str(x)]
        if not target or not candidate_list:
            return None

        matches = difflib.get_close_matches(target, candidate_list, n=1)
        if matches:
            return matches[0]

        if len(target) >= 2:
            for item in candidate_list:
                if target in item:
                    return item

        stripped_target = AdcodeMatcher._normalize_for_match(target)
        if len(stripped_target) >= 2:
            for item in candidate_list:
                if stripped_target in item or stripped_target in AdcodeMatcher._normalize_for_match(item):
                    return item

        return None

    @staticmethod
    def _build_index(codebook_df: pd.DataFrame) -> Dict[str, Any]:
        required_cols = {'province', 'city', 'county', 'code'}
        if not required_cols.issubset(codebook_df.columns):
            raise ValueError(
                f'区划对照表必须包含列: {sorted(required_cols)}，当前列为: {list(codebook_df.columns)}'
            )

        df = codebook_df.copy()
        for col in ['province', 'city', 'county']:
            df[col] = df[col].map(AdcodeMatcher._safe_str)
        df['code'] = df['code'].map(lambda x: AdcodeMatcher._safe_str(x).split('.')[0].zfill(6))
        df = df[(df['province'] != '') & (df['city'] != '') & (df['county'] != '') & (df['code'] != '')]

        wzdata: Dict[str, Any] = {}
        for _, row in df.iterrows():
            tpro = row['province']
            tcity = row['city']
            tcounty = row['county']
            tid = row['code']

            if tpro not in wzdata:
                wzdata[tpro] = [{}, [tcity], tid[0:2]]
                wzdata[tpro][0][tcity] = [{}, [tcounty], tid[0:4]]
                wzdata[tpro][0][tcity][0][tcounty] = tid
            else:
                if tcity not in wzdata[tpro][0]:
                    wzdata[tpro][1].append(tcity)
                    wzdata[tpro][0][tcity] = [{}, [tcounty], tid[0:4]]
                    wzdata[tpro][0][tcity][0][tcounty] = tid
                else:
                    if tcounty not in wzdata[tpro][0][tcity][1]:
                        wzdata[tpro][0][tcity][1].append(tcounty)
                    wzdata[tpro][0][tcity][0][tcounty] = tid
        return wzdata

    def find_code(self, province: Any, city: Any, county: Any) -> Optional[Tuple[str, str, str, str]]:
        """
        根据省、市、县名称查找行政区划代码

        Returns:
            Tuple of (code, matched_province, matched_city, matched_county) or None
        """
        newpro = self._find_closest_string(province, self.wzdata.keys())
        if not newpro:
            return None

        newcity = self._find_closest_string(city, self.wzdata[newpro][0].keys())
        if newcity:
            newcounty = self._find_closest_string(county, self.wzdata[newpro][0][newcity][0].keys())
            if newcounty:
                return (
                    self.wzdata[newpro][0][newcity][0][newcounty],
                    newpro,
                    newcity,
                    newcounty,
                )
            return (
                self.wzdata[newpro][0][newcity][2] + '00',
                newpro,
                newcity,
                '',
            )

        city_list = self.wzdata[newpro][1]
        for tc in city_list:
            newcounty = self._find_closest_string(city, self.wzdata[newpro][0][tc][1])
            if newcounty:
                return (
                    self.wzdata[newpro][0][tc][0][newcounty],
                    newpro,
                    tc,
                    newcounty,
                )

        for tc in city_list:
            newcounty = self._find_closest_string(county, self.wzdata[newpro][0][tc][1])
            if newcounty:
                return (
                    self.wzdata[newpro][0][tc][0][newcounty],
                    newpro,
                    tc,
                    newcounty,
                )

        return None
