# 天气数据可视化

这是一个面向天气数据分析与展示的可视化项目，包含国内城市天气概览、城市详情分析、空气质量展示，以及基于 Three.js 的全球天气视野页面。

## 项目特色

- 国内省会城市天气与空气质量数据总览
- 城市平均最高温、最低温、AQI 等指标对比
- 天气情况占比与城市列表联动展示
- 单城市天气趋势与空气指数分析
- 全球城市天气 3D 地球可视化

## 在线访问

项目部署到 GitHub Pages 后可通过以下地址访问：

https://Pluto0804.github.io/

## 主要文件

- `index.html`：GitHub Pages 入口页
- `index_final.html`：天气数据可视化主页面
- `global_vision.html`：全球天气 3D 可视化页面
- `city_average_data.json`：城市平均天气数据
- `weather_202505_202605.csv`：天气历史数据
- `interCitySelectData2.js`：城市选择与联动数据
- `中华人民共和国.geojson`：中国地图边界数据
- `js/`：ECharts、D3、Three.js 等前端依赖

## 本地预览

直接在浏览器中打开 `index.html` 即可预览。如果浏览器限制本地数据加载，可以在项目目录启动一个静态服务器：

```bash
python -m http.server 8000
```

然后访问：

```text
http://localhost:8000/
```

## 技术栈

- HTML / CSS / JavaScript
- ECharts
- D3.js
- Three.js

## 数据说明

项目数据主要用于课程设计与可视化展示。若继续扩展，可以补充实时天气 API、更多城市样本、数据清洗流程说明，以及自动化构建脚本。
