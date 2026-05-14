#!/usr/bin/env python3
"""
命令行接口 - 极简用法: python cli.py input.csv [output.csv] [codebook.csv]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from geoadcode_matcher import match_csv, get_bundled_codebook


def main():
    argc = len(sys.argv)
    if argc < 2 or argc > 4:
        print("用法: python cli.py input.csv [output.csv] [codebook.csv]")
        print("       1个参数: input.csv (输出为 input_matched.csv)")
        print("       2个参数: input.csv output.csv")
        print("       3个参数: input.csv output.csv codebook.csv")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"错误：输入文件不存在: {input_path}")
        sys.exit(1)

    # 解析参数
    if argc == 2:
        # input.csv -> input_matched.csv
        output_path = input_path.with_name(f"{input_path.stem}_matched.csv")
        codebook_path = get_bundled_codebook()
    elif argc == 3:
        # input.csv output.csv
        output_path = Path(sys.argv[2])
        codebook_path = get_bundled_codebook()
    else:  # argc == 4
        # input.csv output.csv codebook.csv
        output_path = Path(sys.argv[2])
        codebook_path = Path(sys.argv[3])

    # 检查区划表
    if not codebook_path.exists():
        # 尝试当前目录
        codebook_path = Path("discode_ans-2023.csv")
        if not codebook_path.exists():
            print(f"错误：未找到区划对照表: {codebook_path}")
            sys.exit(1)

    print(f"输入: {input_path}")
    print(f"区划表: {codebook_path}")
    print(f"输出: {output_path}")

    result = match_csv(input_path, codebook_path)
    result.to_csv(output_path, index=False, encoding="utf-8-sig")

    matched = (result["adcode"].astype(str).str.strip() != "").sum()
    print(f"完成：{matched}/{len(result)} 行匹配成功")


if __name__ == "__main__":
    main()