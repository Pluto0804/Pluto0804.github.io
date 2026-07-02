import requests
import pandas as pd
import datetime
# 删除 sqlalchemy 相关导入
# from sqlalchemy import create_engine
# from sqlalchemy.types import INT,DateTime,VARCHAR

url = "http://tianqi.2345.com/Pc/GetHistory"
headers = {
   'User-Agent':
       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
     'Referer':
        'https://tianqi.2345.com/air-54172.htm'
}

import pyhttpx
session = pyhttpx.HttpSession()

import time

if __name__ == '__main__':
    ids = [50953, 53463, 54161, 54342, 53698, 54527, 53772, 57036, 52889, 53614, 52866, 51463,
           55591, 56294, 57516, 54823, 57083, 58238, 58321, 57494, 58457, 58847, 58606,
           57687, 57816, 59431, 59758, 58362, 59287, 56778, 54511]#, 45011, 45007, 71294]
    city_data = [
        ("黑龙江", "哈尔滨", 50953),
        ("内蒙古", "呼和浩特", 53463),
        ("吉林", "长春", 54161),
        ("辽宁", "沈阳", 54342),
        ("河北", "石家庄", 53698),
        ("天津", "天津", 54527),
        ("山西", "太原", 53772),
        ("陕西", "西安", 57036),
        ("甘肃", "兰州", 52889),
        ("宁夏", "银川", 53614),
        ("青海", "西宁", 52866),
        ("新疆", "乌鲁木齐", 51463),
        ("西藏", "拉萨", 55591),
        ("四川", "成都", 56294),
        ("重庆", "重庆", 57516),
        ("山东", "济南", 54823),
        ("河南", "郑州", 57083),
        ("江苏", "南京", 58238),
        ("安徽", "合肥", 58321),
        ("湖北", "武汉", 57494),
        ("浙江", "杭州", 58457),
        ("福建", "福州", 58847),
        ("江西", "南昌", 58606),
        ("湖南", "长沙", 57687),
        ("贵州", "贵阳", 57816),
        ("广西", "南宁", 59431),
        ("海南", "海口", 59758),
        ("上海", "上海", 58362),
        ("广东", "广州", 59287),
        ("云南", "昆明", 56778),
        ("北京", "北京", 54511),
        #("澳门", "澳门", 45011),
        #("香港", "香港", 45007),
        #("台湾", "台北", 71294),
    ]

    all_dfs = []   # 用于收集所有城市的 DataFrame

    for i in ids:
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        params = {
            "areaInfo[areaId]": i,
            "areaInfo[areaType]": 2,
            "date[year]": 2026,      # 你可以根据需要修改年份
            "date[month]": 5         # 你可以根据需要修改月份
        }
        resq = requests.get(url, headers=headers, params=params)
        time.sleep(1)
        print(resq)
        data = resq.json()["data"]
        print("原始数据:", data)
        # data frame
        df = pd.read_html(data)[0]
        print(df)

        # 查找城市名字
        city_info = next((city for city in city_data if city[2] == i), None)
        if city_info:
            city_name = city_info[1]
            df['城市名称'] = city_name

        df['日期'] = df['日期'].apply(lambda x: x.split()[0])
        df['空气质量指数'], df['空气质量状况'] = zip(*df['空气质量指数'].str.split().apply(lambda x: (int(x[0]), ' '.join(x[1:]))))
        df['城市代码'] = i
        df['最高温'] = df['最高温'].str.replace('°', '')
        df['最低温'] = df['最低温'].str.replace('°', '')

        # 重命名列（与原来一致）
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

        all_dfs.append(df)

    # 合并所有城市的数据
    final_df = pd.concat(all_dfs, ignore_index=True)

    # 保存为 CSV（推荐）
    final_df.to_csv('weather_data2605.csv', index=False, encoding='utf-8-sig')
    print("数据已保存为 weather_data2605.csv，共 {} 条记录".format(len(final_df)))

    # 如果你想要 JSON 格式，取消下面一行的注释，并注释上面的 to_csv
    # final_df.to_json('weather_data.json', orient='records', force_ascii=False, indent=2)