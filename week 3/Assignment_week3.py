#Task 1
import csv
import urllib.request
import json

#讀取數據
url1 = "https://raw.githubusercontent.com/Liu0329-Andrew/We_Help_Assignment/refs/heads/main/week%203/taipei-attractions-assignment-1"
url2 = "https://raw.githubusercontent.com/Liu0329-Andrew/We_Help_Assignment/refs/heads/main/week%203/taipei-attractions-assignment-2"

assert isinstance(url1, str), f"url1 必須是字串，但得到 {type(url1)}"
assert isinstance(url2, str), f"url2 必須是字串，但得到 {type(url2)}"

#初始化
spot_data = []
mrt_data = []
unique_stations = set()  # 使用集合來去重複的車站名稱
area = ["中正區", "萬華區", "中山區", "大同區", "大安區", "松山區", "信義區", "士林區", "北投區", "內湖區", "南港區", "文山區"]


response1 = urllib.request.urlopen(url1)
data1 = json.load(response1)

response2 = urllib.request.urlopen(url2)
data2 = json.load(response2)


    #處理景點的數據
for item1 in data1["data"]["results"]:
    serial_no = item1.get("SERIAL_NO")
    

    # 嘗試在資料 2 中找到相同 SERIAL_NO 的資料
    match = next((item2 for item2 in data2["data"] if item2["SERIAL_NO"] == serial_no), None)

    if match:
    #提取基本訊息
        spot_title = item1.get("stitle")
        longitude = item1.get("longitude")
        latitude = item1.get("latitude")
        #提取圖片連結有遇到一些問題
        image_url = "https" + item1["filelist"].split("https")[1]  #分隔出有效網址的範圍，利用split語法
        address = match.get("address", "")
        #提取區域 (中文地名)
        district = next((d for d in area if d in address), "未知區域")  # 根據區域列表匹配區域名稱
        
        #加入 spot.csv 資料(依照文件要求的格式)
        spot_data.append([spot_title, district, longitude, latitude, image_url])



for item2 in data2["data"]:
    StationName = item2["MRT"]
    unique_stations.add(StationName)
unique_stations = sorted(unique_stations, key=len, reverse=True)
station_attractions = {station: set() for station in unique_stations} #創建一個字典
matched_attractions = set() #已出現過的景點，不在匹配到其他捷運站

for attraction in data1["data"]["results"]: #歷遍資訊(各個字典)
    info = attraction.get("info", "").strip()
    stitle = attraction.get("stitle", "").strip() # 獲取景點的名稱（stitle）
    if stitle in matched_attractions:
        continue

    for station in unique_stations: #沒有重複的捷運站名稱
        # 簡化判斷：確保車站名稱完整匹配
        if station and station in info:  
            station_attractions[station].add(stitle)
            matched_attractions.add(stitle)  # 標記這個景點已經匹配過
            break
            




station_string = " ".join(unique_stations) 


#輸出spot.csv
with open("spot.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(spot_data)

#輸出 mrt.csv
with open("mrt.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for station in unique_stations:
        attractions = ",".join(station_attractions[station])  # 用逗號將景點名稱連接
        file.write(f"{station},{attractions}\n")  # 手動寫入每行

