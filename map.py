import pandas as pd
import folium

# 讀取 CSV 文件
df_lodging = pd.read_csv('/Users/sumo/Documents/program/Python/map/lodging.csv')
df_tourist_attraction = pd.read_csv('/Users/sumo/Documents/program/Python/map/attraction.csv')
df_restaurant = pd.read_csv('/Users/sumo/Documents/program/Python/map/restaurant.csv')

# 過濾出新竹市的資料
df_lodging_hsinchu = df_lodging[df_lodging['formatted_address'].str.contains("新竹")]
df_tourist_attraction_hsinchu = df_tourist_attraction[df_tourist_attraction['formatted_address'].str.contains("新竹")]
df_restaurant_hsinchu = df_restaurant[df_restaurant['formatted_address'].str.contains("新竹")]

# 隨機選擇一個早餐餐廳
breakfast = df_restaurant_hsinchu.sample(1).iloc[0]

# 隨機選擇兩個景點（上午和下午各一個）
morning_attraction = df_tourist_attraction_hsinchu.sample(1).iloc[0]
afternoon_attraction = df_tourist_attraction_hsinchu.sample(1).iloc[0]

# 隨機選擇一個不同的午餐餐廳
lunch = df_restaurant_hsinchu[df_restaurant_hsinchu['place_id'] != breakfast['place_id']].sample(1).iloc[0]

# 隨機選擇一個不同的晚餐餐廳
dinner = df_restaurant_hsinchu[
    (df_restaurant_hsinchu['place_id'] != breakfast['place_id']) & 
    (df_restaurant_hsinchu['place_id'] != lunch['place_id'])
].sample(1).iloc[0]

# 隨機選擇一個住宿地點
lodging = df_lodging_hsinchu.sample(1).iloc[0]

# 創建地圖
m = folium.Map(location=[24.8138, 120.9675], zoom_start=12)

# 添加標記到地圖
def add_marker(m, row, color):
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['name'],
        icon=folium.Icon(color=color)
    ).add_to(m)

add_marker(m, breakfast, 'blue')
add_marker(m, morning_attraction, 'green')
add_marker(m, lunch, 'blue')
add_marker(m, afternoon_attraction, 'green')
add_marker(m, dinner, 'blue')
add_marker(m, lodging, 'red')

# 保存地圖到 HTML 文件
m.save('/Users/sumo/Documents/program/Python/map/hsinchu_trip_planner_map.html')

# 輸出行程規劃
print("新竹一日遊行程：")
print(f"早餐：{breakfast['name']} - {breakfast['formatted_address']}")
print(f"上午景點：{morning_attraction['name']} - {morning_attraction['formatted_address']}")
print(f"午餐：{lunch['name']} - {lunch['formatted_address']}")
print(f"下午景點：{afternoon_attraction['name']} - {afternoon_attraction['formatted_address']}")
print(f"晚餐：{dinner['name']} - {dinner['formatted_address']}")
print(f"住宿：{lodging['name']} - {lodging['formatted_address']}")
