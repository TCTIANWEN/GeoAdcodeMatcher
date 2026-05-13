"""
命令行接口
"""

import argparse
import sys
from pathlib import Path

from .utils import match_csv


def main():
    parser = argparse.ArgumentParser(
        description='行政区划代码匹配工具 - 通过省、市、县名称匹配行政代码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python -m GeoAdcodeMatcher.cli input.csv
  python -m GeoAdcodeMatcher.cli input.csv -c codebook.csv
  python -m GeoAdcodeMatcher.cli input.csv -o output.csv -c codebook.csv
        '''
    )
    parser.add_argument('input', type=Path, help='输入 CSV 文件路径')
    parser.add_argument('-c', '--codebook', type=Path, help='区划对照表路径（默认为 discode_ans-2023.csv）')
    parser.add_argument('-o', '--output', type=Path, help='输出文件路径（默认为 input_stem_匹配行政代码.csv）')
    parser.add_argument('--province-col', dest='province_col', help='省列名（不指定则自动识别）')
    parser.add_argument('--city-col', dest='city_col', help='市列名（不指定则自动识别）')
    parser.add_argument('--county-col', dest='county_col', help='县/区列名（不指定则自动识别）')

    args = parser.parse_args()

    if not args.input.exists():
        print(f'错误：输入文件不存在: {args.input}', file=sys.stderr)
        sys.exit(1)

    codebook_path = args.codebook
    if codebook_path is None:
        codebook_path = Path('discode_ans-2023.csv')
        if not codebook_path.exists():
            codebook_path = Path('discode_ans.csv')
        if not codebook_path.exists():
            print(f'错误：未找到区划对照表，请使用 -c 参数指定', file=sys.stderr)
            sys.exit(1)

    if not codebook_path.exists():
        print(f'错误：区划对照表不存在: {codebook_path}', file=sys.stderr)
        sys.exit(1)

    output_path = args.output
    if output_path is None:
        output_path = args.input.with_name(f'{args.input.stem}_匹配行政代码.csv')

    print(f'输入文件: {args.input}')
    print(f'区划对照表: {codebook_path}')
    print(f'输出文件: {output_path}')

    try:
        result_df = match_csv(
            input_path=args.input,
            codebook_path=codebook_path,
            province_col=args.province_col,
            city_col=args.city_col,
            county_col=args.county_col,
        )
        result_df.to_csv(output_path, index=False, encoding='utf-8-sig')

        matched_count = (result_df['adcode'].astype(str).str.strip() != '').sum()
        total_count = len(result_df)
        print(f'成功匹配 {matched_count}/{total_count} 行')
        print(f'结果已保存到: {output_path}')
    except Exception as e:
        print(f'错误: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
