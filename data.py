import googlemaps
import pandas as pd
import folium

# 初始化 Google Maps 客戶端
gmaps = googlemaps.Client(key='AIzaSyA0kMosszZnnwYVx2hg7Q8l9bwDfIujinc')

# 台灣各縣市名稱
cities = [
    "臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市",
    "基隆市", "新竹市", "嘉義市", "新竹縣", "苗栗縣", "彰化縣",
    "南投縣", "雲林縣", "嘉義縣", "屏東縣", "宜蘭縣", "花蓮縣",
    "臺東縣", "澎湖縣"
]

location_types = ['restaurant', 'tourist_attraction', 'lodging']
all_places_details = {place_type: [] for place_type in location_types}

# 獲取各地區的地點 ID 並獲取詳細資訊
for city in cities:
    place_ids = {place_type: [] for place_type in location_types}
    try:
        geocode_result = gmaps.geocode(city)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            # 對每種類型的地點進行搜尋
            for place_type in location_types:
                places_result = gmaps.places_nearby(location=location, radius=25000, type=place_type, language='zh-TW')
                place_ids[place_type].extend([place['place_id'] for place in places_result['results']])
        else:
            print(f"無法找到 {city} 的地理編碼結果")
    except Exception as e:
        print(f"獲取 {city} 地點時發生錯誤: {e}")

    unique_place_ids = {place_type: list(set(ids)) for place_type, ids in place_ids.items()}

    for place_type, ids in unique_place_ids.items():
        for place_id in ids:
            try:
                place_details = gmaps.place(place_id=place_id, language='zh-TW')
                if 'geometry' in place_details['result']:
                    all_places_details[place_type].append(place_details['result'])
            except Exception as e:
                print(f"獲取地點 ID {place_id} 的詳細資訊時發生錯誤: {e}")

# 轉換為 pandas DataFrame 並保存為 CSV
for place_type, details in all_places_details.items():
    df = pd.DataFrame(details)
    if not df.empty:
        df['latitude'] = df['geometry'].apply(lambda x: x['location']['lat'])
        df['longitude'] = df['geometry'].apply(lambda x: x['location']['lng'])
        df.to_csv(f'places_details_{place_type}.csv', index=False, encoding='utf-8-sig')

# 創建地圖
m = folium.Map(location=[23.5, 121], zoom_start=7)

# 定義標記顏色
colors = {
    'restaurant': 'blue',
    'tourist_attraction': 'green',
    'lodging': 'red'
}

# 添加標記
for place_type, details in all_places_details.items():
    for detail in details:
        folium.Marker(
            location=[detail['geometry']['location']['lat'], detail['geometry']['location']['lng']],
            popup=detail['name'],
            icon=folium.Icon(color=colors[place_type])
        ).add_to(m)

# 保存地圖到 HTML 文件
m.save('trip_planner_map.html')

# 顯示加到的資料筆數
for place_type, details in all_places_details.items():
    print(f"{place_type} 類型地點總數: {len(details)}")