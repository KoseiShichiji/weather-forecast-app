from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

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

@app.get("/")
def Hello():
    return {"Hello":"World!"}

@app.get("/weather")
def get_weather(city: str):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xquk59",
            database="weatherForecast"
        )
        cursor = connection.cursor()
        query = "SELECT * FROM weatherForecast WHERE prefecture = %s"
        cursor.execute(query, (city,))
        result = cursor.fetchall()

        return {"weather_data": result}

    except mysql.connector.Error as err:
        return {"error": str(err)}

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()