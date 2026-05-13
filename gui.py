"""
行政区划代码匹配工具 - GUI 界面
"""

import sys
from pathlib import Path
from typing import Optional

import pandas as pd

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
except Exception as e:
    raise RuntimeError('当前 Python 环境缺少 tkinter，无法弹出窗口。') from e

from .matcher import AdcodeMatcher
from .utils import (
    COMMON_PROVINCE_COLS,
    COMMON_CITY_COLS,
    COMMON_COUNTY_COLS,
    detect_column,
    match_dataframe,
    read_csv_with_fallback,
)

DEFAULT_CODEBOOK_NAMES = ['discode_ans-2023.csv', 'discode_ans.csv']


def find_codebook(script_dir: Path) -> Optional[Path]:
    """在脚本目录下查找区划对照表"""
    for name in DEFAULT_CODEBOOK_NAMES:
        candidate = script_dir / name
        if candidate.exists():
            return candidate
    return None


def choose_input_file() -> Optional[Path]:
    """弹出文件选择对话框"""
    file_path = filedialog.askopenfilename(
        title='请选择要处理的 CSV 文件',
        filetypes=[('CSV 文件', '*.csv'), ('所有文件', '*.*')],
    )
    return Path(file_path) if file_path else None


def choose_codebook_file() -> Optional[Path]:
    """弹出文件选择对话框让用户选择区划对照表"""
    file_path = filedialog.askopenfilename(
        title='未找到区划对照表，请选择 discode_ans-2023.csv',
        filetypes=[('CSV 文件', '*.csv'), ('所有文件', '*.*')],
    )
    return Path(file_path) if file_path else None


def build_output_path(input_path: Path) -> Path:
    """生成输出文件路径"""
    return input_path.with_name(f'{input_path.stem}_匹配行政代码.csv')


def main() -> None:
    """主函数"""
    root = tk.Tk()
    root.withdraw()
    root.update()

    try:
        input_path = choose_input_file()
        if not input_path:
            messagebox.showinfo('提示', '你没有选择输入文件，程序已结束。')
            return

        script_dir = Path(sys.argv[0]).resolve().parent
        codebook_path = find_codebook(script_dir)
        if codebook_path is None:
            messagebox.showinfo('提示', '脚本同目录下未找到区划对照表，请手动选择。')
            codebook_path = choose_codebook_file()
            if not codebook_path:
                messagebox.showinfo('提示', '你没有选择区划对照表，程序已结束。')
                return

        output_path = build_output_path(input_path)

        input_df = read_csv_with_fallback(input_path)
        codebook_df = read_csv_with_fallback(codebook_path)

        province_col = detect_column(list(input_df.columns), COMMON_PROVINCE_COLS)
        city_col = detect_column(list(input_df.columns), COMMON_CITY_COLS)
        county_col = detect_column(list(input_df.columns), COMMON_COUNTY_COLS, required=False)

        matcher = AdcodeMatcher(codebook_df)
        result_df = match_dataframe(
            input_df=input_df,
            matcher=matcher,
            province_col=province_col,
            city_col=city_col,
            county_col=county_col,
            code_col='adcode',
            matched_province_col='matched_province',
            matched_city_col='matched_city',
            matched_county_col='matched_county',
        )

        result_df.to_csv(output_path, index=False, encoding='utf-8-sig')

        matched_count = (result_df['adcode'].astype(str).str.strip() != '').sum()
        total_count = len(result_df)
        messagebox.showinfo(
            '处理完成',
            f'成功匹配 {matched_count}/{total_count} 行。\n\n'
            f'识别到的列名：\n省 = {province_col}\n市 = {city_col}\n区县 = {county_col if county_col else "未识别到，已按城市层级匹配"}\n\n'
            f'区划对照表：\n{codebook_path}\n\n'
            f'输出文件：\n{output_path}'
        )
    except Exception as e:
        messagebox.showerror('运行出错', str(e))
        raise
    finally:
        try:
            root.destroy()
        except Exception:
            pass


if __name__ == '__main__':
    main()
