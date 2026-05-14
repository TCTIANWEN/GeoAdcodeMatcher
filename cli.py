#!/usr/bin/env python3
"""
命令行接口 - 极简用法: python cli.py input.csv [output.csv] [codebook.csv]
"""

import sys
from pathlib import Path

# 将父目录加入路径
script_dir = Path(__file__).parent
parent_dir = script_dir.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(script_dir))

# 直接加载模块
import importlib.util

def load_module(name, filepath):
    spec = importlib.util.spec_from_file_location(name, filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

geoadcode = load_module("geoadcode_matcher", script_dir / "__init__.py")
match_csv = geoadcode.match_csv
get_bundled_codebook = geoadcode.get_bundled_codebook


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