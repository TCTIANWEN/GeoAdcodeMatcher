#!/usr/bin/env python3
"""
命令行接口 - 极简用法: python cli.py input.csv [codebook.csv]
"""

import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from geoadcode_matcher import match_csv, get_bundled_codebook


def main():
    if len(sys.argv) < 2:
        print("用法: python cli.py input.csv [codebook.csv]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"错误：输入文件不存在: {input_path}")
        sys.exit(1)

    # 区划表：参数2 > 内置 > 当前目录
    if len(sys.argv) >= 3:
        codebook_path = Path(sys.argv[2])
    else:
        codebook_path = get_bundled_codebook()
        if not codebook_path.exists():
            codebook_path = Path("discode_ans-2023.csv")
            if not codebook_path.exists():
                print("错误：未找到区划对照表")
                sys.exit(1)

    if not codebook_path.exists():
        print(f"错误：区划对照表不存在: {codebook_path}")
        sys.exit(1)

    # 输出文件：input_matched.csv
    output_path = input_path.with_name(f"{input_path.stem}_matched.csv")

    print(f"输入: {input_path}")
    print(f"区划表: {codebook_path}")
    print(f"输出: {output_path}")

    result = match_csv(input_path, codebook_path)
    result.to_csv(output_path, index=False, encoding="utf-8-sig")

    matched = (result["adcode"].astype(str).str.strip() != "").sum()
    print(f"完成：{matched}/{len(result)} 行匹配成功")


if __name__ == "__main__":
    main()