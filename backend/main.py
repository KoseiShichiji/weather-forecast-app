from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import requests
import romkan
import json

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL接続情報
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "xquk59",
    "database": "weatherForecast",
}

# OpenWeatherMap APIキー
API_TOKEN = "49ffe79df3664f91a32b0ee522dcbbb2"

# 都道府県のリスト
prefectures = [
    "Hokkaido", "Aomori", "Iwate", "Miyagi", "Akita", "Yamagata", "Fukushima",
    "Ibaraki", "Tochigi", "Gunma", "Saitama", "Chiba", "Tokyo", "Kanagawa",
    "Niigata", "Toyama", "Ishikawa", "Fukui", "Yamanashi", "Nagano", "Gifu",
    "Shizuoka", "Aichi", "Mie", "Shiga", "Kyoto", "Osaka", "Hyogo", "Nara",
    "Wakayama", "Tottori", "Shimane", "Okayama", "Hiroshima", "Yamaguchi",
    "Tokushima", "Kagawa", "Ehime", "Kochi", "Fukuoka", "Saga", "Nagasaki",
    "Kumamoto", "Oita", "Miyazaki", "Kagoshima", "Okinawa"
]

# DBからデータ取得
def get_weather_from_mysql(city: str):
    try:
        # MySQL接続
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # MySQLから天気情報取得
        query = "SELECT weather,iconImage FROM weatherForecast WHERE prefecture = %s"
        cursor.execute(query, (city,))
        result = cursor.fetchall()
        return result

    except mysql.connector.Error as err:
        raise err

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 天気APIからデータ取得
def get_weather_from_api(city: str):
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,  # 都市名で取得
                "appid": API_TOKEN,
                "units": "metric",
                "lang": "ja",
            },
        )
        weather_data = response.json()
        return weather_data

    except requests.RequestException as err:
        raise err

# 天気予報を取得してDBにインサート
def insert_weather_into_db(city: str, weather_data: dict):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        # MySQLに天気情報を挿入
        insert_query = "INSERT INTO weatherForecast (prefecture, weather, iconImage) VALUES (%s, %s, %s)"
        # print("weather_data", weather_data)
        insert_values = (
            city, weather_data['weather'][0]['description'], weather_data['weather'][0]['icon'])
        cursor.execute(insert_query, insert_values)
        connection.commit()

    except mysql.connector.Error as err:
        raise err

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# 全都道府県の天気予報を取得してDBにインサート
for city in prefectures:
    try:
        # 天気APIからデータ取得
        weather_data = get_weather_from_api(city)

        # データベースにインサート
        insert_weather_into_db(city, weather_data)

    except Exception as err:
        print(f"Error processing {city}: {err}")


@app.get("/weather")
def get_weather(city: str):
    try:
        result_from_mysql = get_weather_from_mysql(city)
        return {"result_from_mysql": result_from_mysql}

    except (mysql.connector.Error, requests.RequestException) as err:
        return {"error": str(err)}


@app.get("/weatherAPI")
def get_weatherAPI(city: str):
    try:
        result_from_api = get_weather_from_api(city)
        insert_weather_into_db(city, result_from_api)
        return {"weather_from_api": result_from_api}

    except (mysql.connector.Error, requests.RequestException) as err:
        return {"error": str(err)}


# @app.get("/")
# def Hello():
#     return {"Hello": "World!"}


# @app.get("/weather")
# def get_weather(city: str):
#     try:
#         # MySQL接続
#         connection = mysql.connector.connect(**db_config)
#         cursor = connection.cursor()

#         # MySQLから天気情報取得
#         query = "SELECT weather FROM weatherForecast WHERE prefecture = %s"
#         cursor.execute(query, (city,))
#         result = cursor.fetchall()

#         # OpenWeatherMap APIから天気情報取得
#         response = requests.get(
#             "https://api.openweathermap.org/data/2.5/weather",
#             params={
#                 "q": city,  # 都市名で取得
#                 "appid": API_TOKEN,
#                 "units": "metric",
#                 "lang": "ja",
#             },
#         )

#         weather_data = response.json()
#         # print(weather_data.weather[0])

#         # MySQLに天気情報を挿入
#         # insert_query = "INSERT INTO weatherForecast (prefecture, weather) VALUES (%s, %s)"
#         # insert_values = (city, json.dumps(weather_data))
#         # cursor.execute(insert_query, insert_values)
#         # connection.commit()
#         return {"weather_from_mysql": result, "weather_from_api": weather_data}

#     except mysql.connector.Error as err:
#         return {"error": str(err)}

#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
