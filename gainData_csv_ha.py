import requests
import pandas as pd
import datetime
import time

# 目标地区：id, 名称
target_areas = [
    (45007, "香港"),
    (45011, "澳门"),
    (71294, "台湾")
]

url = "http://tianqi.2345.com/Pc/GetHistory"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Referer': 'https://tianqi.2345.com/air-54172.htm'
}

def fetch_month_data(area_id, year, month, max_retries=3):
    """请求单个月份的数据，返回原始DataFrame，失败返回None"""
    params = {
        "areaInfo[areaId]": area_id,
        "areaInfo[areaType]": 2,
        "date[year]": year,
        "date[month]": month
    }
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            if resp.status_code != 200:
                print(f"请求失败 {area_id}-{year}-{month}，状态码：{resp.status_code}")
                time.sleep(2)
                continue
            data = resp.json()["data"]
            df = pd.read_html(data)[0]
            return df
        except Exception as e:
            print(f"处理 {area_id}-{year}-{month} 时出错：{e}，重试 {attempt+1}/{max_retries}")
            time.sleep(2)
    return None

def clean_df(df, area_name, area_id, year, month):
    """清洗单月原始DataFrame，添加地区、日期、城市代码等信息"""
    if df is None or df.empty:
        return None
    # 日期处理：去掉可能的时间部分
    df['日期'] = df['日期'].apply(lambda x: x.split()[0])
    # 拆分空气质量指数列（假设格式 "数字 状况"）
    df['空气质量指数'], df['空气质量状况'] = zip(*df['空气质量指数'].str.split().apply(lambda x: (int(x[0]), ' '.join(x[1:]))))
    # 温度去掉°符号
    df['最高温'] = df['最高温'].str.replace('°', '')
    df['最低温'] = df['最低温'].str.replace('°', '')
    # 添加自定义列
    df['城市名称'] = area_name
    df['城市代码'] = area_id
    # 统一列名
    df.rename(columns={
        '日期': 'date',
        '城市名称': 'city',
        '最高温': 'max_temperature',
        '最低温': 'min_temperature',
        '天气': 'weather_condition',
        '风力风向': 'wind_info',
        '空气质量指数': 'air_quality_index',
        '空气质量状况': 'air_quality_status',
        '城市代码': 'city_id'
    }, inplace=True)
    return df

if __name__ == '__main__':
    # 生成月份序列：2025-05 到 2026-05
    start_date = datetime.date(2025, 5, 1)
    end_date = datetime.date(2026, 5, 1)
    months = []
    current = start_date
    while current <= end_date:
        months.append((current.year, current.month))
        # 下个月
        if current.month == 12:
            current = current.replace(year=current.year+1, month=1)
        else:
            current = current.replace(month=current.month+1)

    for area_id, area_name in target_areas:
        print(f"开始抓取 {area_name} 的数据...")
        area_dfs = []   # 存放当前地区的所有月份数据

        for year, month in months:
            print(f"  请求 {year}-{month:02d}")
            raw_df = fetch_month_data(area_id, year, month)
            if raw_df is None:
                print(f"    跳过 {area_name} {year}-{month:02d} (无数据)")
                continue
            clean_df_month = clean_df(raw_df, area_name, area_id, year, month)
            if clean_df_month is not None:
                area_dfs.append(clean_df_month)
            time.sleep(1)   # 礼貌间隔

        if not area_dfs:
            print(f"{area_name} 未获取到任何数据，跳过。")
        else:
            area_df = pd.concat(area_dfs, ignore_index=True)
            filename = f"weather_{area_name}_{start_date.strftime('%Y%m')}-{end_date.strftime('%Y%m')}.csv"
            area_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"{area_name} 数据已保存至 {filename}，共 {len(area_df)} 条记录。")