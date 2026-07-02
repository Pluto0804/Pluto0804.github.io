import re
import csv

def parse_city_ids_simple(file_path):
    """解析 interCitySelectData2.js 文件，提取所有城市中文名和数字ID"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    result = {}
    # 匹配每个 city['区域']=[ ... ] 块
    pattern = r"city\['([^']+)'\]=\[(.*?)\];"
    blocks = re.findall(pattern, content, re.DOTALL)

    for region, array_str in blocks:
        # 提取数组中每个双引号包裹的字符串（每个字符串可能包含多个用 | 分隔的城市）
        items = re.findall(r'"([^"]*)"', array_str)
        for item in items:
            # 每个 item 可能包含多个城市，用 | 分隔
            city_entries = item.split('|')
            for entry in city_entries:
                parts = entry.split(';')
                if len(parts) >= 4:
                    raw_name = parts[1].strip()
                    # 去除开头的字母和空格，例如 "H 红花山" -> "红花山"
                    if ' ' in raw_name:
                        chinese_name = raw_name.split(' ', 1)[-1]
                    else:
                        chinese_name = raw_name
                    code = parts[3].strip()
                    if code.isdigit():   # 只保留数字ID
                        result[chinese_name] = code
    return result

def save_to_csv(city_dict, csv_file='cities.csv'):
    """将城市字典保存为CSV文件"""
    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['城市中文名', '城市代码'])
        for name, code in city_dict.items():
            writer.writerow([name, code])
    print(f"已保存 {len(city_dict)} 条城市数据到 {csv_file}")

if __name__ == '__main__':
    js_file = 'interCitySelectData2.js'   # 请确保此文件在当前目录
    print(f"正在解析 {js_file} ...")
    cities = parse_city_ids_simple(js_file)
    print(f"成功解析到 {len(cities)} 个城市（含数字ID）")
    save_to_csv(cities)