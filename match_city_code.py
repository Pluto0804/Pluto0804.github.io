#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys

def load_city_code_map(csv_path='cities.csv'):
    """从CSV文件加载城市中文名到代码的映射"""
    city_map = {}
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            header = next(reader)  # 跳过标题行：城市中文名,城市代码
            for row in reader:
                if len(row) >= 2:
                    city_name = row[0].strip()
                    city_code = row[1].strip()
                    if city_name and city_code:
                        city_map[city_name] = city_code
    except FileNotFoundError:
        print(f"错误：找不到文件 {csv_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"读取CSV文件时出错：{e}", file=sys.stderr)
        sys.exit(1)
    return city_map

def main():
    city_map = load_city_code_map()
    # 从标准输入读取每行城市名
    for line in sys.stdin:
        city = line.strip()
        if not city:
            continue
        if city in city_map:
            code = city_map[city]
            # 输出格式：("城市名", 代码)
            print(f'("{city}", {code})')
        else:
            # 未匹配到的输出到标准错误，不影响正常匹配结果
            print(f'未找到城市：{city}', file=sys.stderr)

if __name__ == '__main__':
    main()