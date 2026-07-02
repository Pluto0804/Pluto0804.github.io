import requests
import pandas as pd
import datetime
import time

# 城市列表：(国家, 城市名, 城市代码)
city_data = [
    ("日本", "东京", 226396),
    ("韩国", "首尔", 226081),
    ("泰国", "曼谷", 318849),
    ("新加坡", "新加坡", 300597),
    ("马来西亚", "吉隆坡", 233776),
    ("印度尼西亚", "雅加达", 208971),
    ("印度", "新德里", 187745),
    ("印度", "孟买", 204842),
    ("阿联酋", "迪拜", 323091),
    ("沙特阿拉伯", "利雅得", 297030),
    ("土耳其", "伊斯坦布尔", 318251),
    ("以色列", "耶路撒冷", 213225),
    ("约旦", "安曼", 221790),
    ("伊朗", "德黑兰", 210841),
    ("越南", "河内", 353412),
    ("菲律宾", "马尼拉", 264885),
    ("缅甸", "仰光", 246562),
    ("斯里兰卡", "科伦坡", 311399),
    ("孟加拉国", "达卡", 1007914),
    ("埃及", "开罗", 127164),
    ("尼日利亚", "拉各斯", 4607),
    ("肯尼亚", "内罗毕", 224758),
    ("埃塞俄比亚", "亚的斯亚贝巴", 126831),
    ("南非", "约翰内斯堡", 305448),
    ("摩洛哥", "卡萨布兰卡", 243353),
    ("阿尔及利亚", "阿尔及尔", 2093),
    ("突尼斯", "突尼斯", 321398),
    ("塞内加尔", "达喀尔", 297442),
    ("加纳", "阿克拉", 178551),
    ("乌干达", "坎帕拉", 318416),
    ("卢旺达", "基加利", 293211),
    ("英国", "伦敦", 328328),
    ("法国", "巴黎", 623),
    ("德国", "柏林", 178087),
    ("意大利", "罗马", 213490),
    ("西班牙", "马德里", 308526),
    ("奥地利", "维也纳", 31868),
    ("荷兰", "阿姆斯特丹", 249758),
    ("比利时", "布鲁塞尔", 27581),
    ("瑞典", "斯德哥尔摩", 314929),
    ("丹麦", "哥本哈根", 123094),
    ("挪威", "奥斯陆", 254946),
    ("芬兰", "赫尔辛基", 133328),
    ("俄罗斯", "莫斯科", 294021),
    ("波兰", "华沙", 274663),
    ("匈牙利", "布达佩斯", 187423),
    ("捷克", "布拉格", 125594),
    ("希腊", "雅典", 182536),
    ("葡萄牙", "里斯本", 274087),
    ("爱尔兰", "都柏林", 207931),
    ("瑞士", "苏黎世", 316622),
    ("美国", "纽约", 349727),
    ("美国", "洛杉矶", 347625),
    ("美国", "芝加哥", 348308),
    ("美国", "休斯顿", 351197),
    ("加拿大", "多伦多", 55488),
    ("加拿大", "温哥华", 53286),
    ("墨西哥", "墨西哥城", 242560),
    ("巴西", "圣保罗", 45881),
    ("巴西", "里约热内卢", 45449),
    ("阿根廷", "布宜诺斯艾利斯", 7894),
    ("智利", "圣地亚哥", 60449),
    ("秘鲁", "利马", 264120),
    ("哥伦比亚", "波哥大", 107487),
    ("澳大利亚", "悉尼", 22889),
    ("澳大利亚", "墨尔本", 26216),
    ("新西兰", "奥克兰", 252066),
]

# 提取城市代码列表
city_ids = [item[2] for item in city_data]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Referer': 'https://tianqi.2345.com/air-54172.htm'
}

url = "http://tianqi.2345.com/Pc/GetHistory"

def fetch_monthly_weather(city_id, year, month):
    """获取单个城市某月的天气数据，返回DataFrame"""
    params = {
        "areaInfo[areaId]": city_id,
        "areaInfo[areaType]": 1,
        "date[year]": year,
        "date[month]": month
    }
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if "data" not in data or not data["data"]:
            print(f"警告：{city_id} {year}-{month} 无数据")
            return None
        df = pd.read_html(data["data"])[0]
        return df
    except Exception as e:
        print(f"错误：{city_id} {year}-{month} 请求失败 - {e}")
        return None

def process_df(df, country, city_name, city_id, year, month):
    """清洗DataFrame，添加国家和城市信息"""
    if df is None or df.empty:
        return None
    df['国家'] = country
    df['城市名称'] = city_name
    df['城市代码'] = city_id
    # 清洗日期列：去掉星期几
    df['日期'] = df['日期'].apply(lambda x: x.split()[0])
    # 去掉温度中的°符号
    df['最高温'] = df['最高温'].str.replace('°', '')
    df['最低温'] = df['最低温'].str.replace('°', '')
    # 重命名列
    df.rename(columns={
        '日期': 'date',
        '国家': 'country',
        '城市名称': 'city',
        '最高温': 'max_temperature',
        '最低温': 'min_temperature',
        '天气': 'weather_condition',
        '风力风向': 'wind_info',
        '城市代码': 'city_id'
    }, inplace=True)
    # 调整列顺序
    df = df[['date', 'country', 'city', 'city_id', 'max_temperature', 'min_temperature', 'weather_condition', 'wind_info']]
    return df

if __name__ == '__main__':
    start_year, start_month = 2025, 5
    end_year, end_month = 2026, 5

    all_dfs = []

    # 生成要爬取的月份列表
    months_to_crawl = []
    current_year, current_month = start_year, start_month
    while (current_year < end_year) or (current_year == end_year and current_month <= end_month):
        months_to_crawl.append((current_year, current_month))
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1

    total_requests = len(city_ids) * len(months_to_crawl)
    print(f"总共需要请求 {total_requests} 次（{len(city_ids)} 个城市 × {len(months_to_crawl)} 个月）")

    for (country, city_name, city_id) in city_data:
        print(f"\n正在处理城市：{country} {city_name} (代码 {city_id})")
        for year, month in months_to_crawl:
            print(f"  获取 {year}-{month:02d} 数据...")
            df_raw = fetch_monthly_weather(city_id, year, month)
            if df_raw is not None:
                df_clean = process_df(df_raw, country, city_name, city_id, year, month)
                if df_clean is not None:
                    all_dfs.append(df_clean)
            time.sleep(1)  # 控制请求频率

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        # 按国家和日期排序
        final_df.sort_values(['country', 'city', 'date'], inplace=True)
        output_file = 'weather_202505_202605.csv'
        final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n数据保存成功！共 {len(final_df)} 条记录，文件名为 {output_file}")
    else:
        print("没有获取到任何数据，请检查网络或城市代码。")