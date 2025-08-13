import sys
import json
import pandas as pd
import glob
import re
from datetime import datetime
from collections import Counter
import os
from opencc import OpenCC

def load_and_concat(files_pattern: str) -> pd.DataFrame:
    dfs = []
    for file in glob.glob(files_pattern):
        if file.endswith(('.xlsx', '.xls')):
            excel_file = pd.ExcelFile(file)
            for sheet_name in excel_file.sheet_names:
                df = excel_file.parse(sheet_name)
                df['tags'] = [[sheet_name]] * len(df)  # 每行都用 sheet_name 的列表作为 tags
                dfs.append(df)
        elif file.endswith('.csv'):
            df = pd.read_csv(file)
            df['tags'] = [['csv']] * len(df)  # 可以用 'csv' 或者文件名作标记
            dfs.append(df)
    # return pd.concat(dfs, ignore_index=True)

    df = pd.concat(dfs, ignore_index=True)

    # 剔除四个字段同时为空的记录（title/question, content/answer, source, link）
    fields = ['标题', '内容', '来源', '链接']
    mask = ~df[fields].fillna("").applymap(str.strip).eq("").all(axis=1)
    df = df[mask]

    return df.reset_index(drop=True)

_converter = OpenCC('t2s')

def clean_text(s: str) -> str:
    if pd.isna(s):
        return ""
    s = _converter.convert(str(s)) # 繁體轉簡體
    s = re.sub(r'<[^>]+>', '', s) # 去除 emoji 和 HTML 标签
    s = re.sub(r'[^\w\s\-\u4e00-\u9fa5\.,\?]', '', s) # 保留英文，数字，空格，下划线，中文字符，横杠，英文逗号/句号，和问号
    return s.strip()

def clean_row(row: pd.Series, idx: int) -> pd.Series:
    row['id'] = str(idx + 1).zfill(5)
    row['question'] = clean_text(row['question'])
    row['answer']   = clean_text(row['answer'])
    row['source']   = clean_text(row['source'])
    row['link']     = clean_text(row.get('link', ''))
    row['creator']  = str(row.get('creator', '')).lower()
    # 统一日期格式
    try:
        dt = pd.to_datetime(row.get('created_at'))
        row['created_at'] = dt.strftime('%Y-%m-%d')
    except Exception:
        row['created_at'] = ''
    return row

def row_to_json(row: pd.Series) -> dict:
    return {
        "id":         row['id'],
        "question":   row['question'],
        "answer":     row['answer'],
        "source":     row['source'],
        "link":       row['link'],
        "tags":       row['tags'],
        "creator":    row['creator'],
        "created_at": row['created_at'],
    }

def main(input_pattern: str, output_file: str):
    if os.path.exists(output_file):
        answer = input(f"文件 {output_file} 已存在。是否覆盖？(Y/N): ").strip().lower()
        if answer != 'y':
            print("已取消生成。")
            return
    
    df = load_and_concat(input_pattern)
    df = df.rename(columns={
        # 将原始列名映射到标准列名
        '标题':'question', '内容':'answer',
        '来源':'source', '链接':'link',
        '标签':'tags', '添加人员':'creator', '更新时间':'created_at'
    })
    df = df.apply(lambda row: clean_row(row, row.name), axis=1)
    df = df.dropna(subset=['question','answer'])
    records = df.apply(row_to_json, axis=1).tolist()
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"成功生成：{output_file}，共 {len(records)} 条记录。")

    # 展平所有 tags 到一个列表
    flat_tags = [tag for tags in df['tags'] for tag in tags]

    # 统计每个 tag 的出现次数
    tag_counts = Counter(flat_tags)

    print("\n📊 标签分布统计：")
    for tag, count in tag_counts.items():
        print(f"  - {tag}: {count} 条记录")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法: python qa_builder.py 'C:\Codes\CSSA\生活专区.xlsx' qa_clean_data.json")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
