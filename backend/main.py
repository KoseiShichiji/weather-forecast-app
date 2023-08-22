from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import requests
import romkan
import json

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://43.207.162.160",
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
    # "host": "localhost",
    "host": "43.207.162.160",
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
    # 初期化
    connection = None
    try:
        # MySQL接続
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # MySQLから天気情報取得
        query = "SELECT weather,iconImage,temp,temp_max,temp_min FROM weatherForecast WHERE prefecture = %s"
        cursor.execute(query, (city,))
        result = cursor.fetchall()
        return result

    except mysql.connector.Error as err:
        raise err
    finally:
        if connection is not None and connection.is_connected():
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
        query = "SELECT COUNT(*) FROM weatherForecast WHERE prefecture = %s"
        cursor.execute(query, (city,))
        count = cursor.fetchone()[0]

        if count > 0:
            # 天気情報アップデート
            update_query = "UPDATE weatherForecast SET weather = %s, iconImage = %s, updatedAt = NOW(), temp = %s, temp_max = %s, temp_min = %s WHERE prefecture = %s"
            update_values = (
                weather_data['weather'][0]['description'], weather_data['weather'][0]['icon'],
                weather_data['main']['temp'], weather_data['main']['temp_max'], weather_data['main']['temp_min'], city)
            cursor.execute(update_query, update_values)
        else:
            # 天気情報がなかった場合はインサート
            insert_query = "INSERT INTO weatherForecast (prefecture, weather, iconImage, temp, temp_max, temp_min, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())"
            insert_values = (
                city, weather_data['weather'][0]['description'], weather_data['weather'][0]['icon'],
                weather_data['main']['temp'], weather_data['main']['temp_max'], weather_data['main']['temp_min'])
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

        # データベースにインサートまたはアップデート
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
