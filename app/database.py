import sqlite3
from datetime import datetime
from app.services.weather import fetch_weather

DATABASE = "app/weather.sqlite"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        temperature REAL NOT NULL,
        description TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect(DATABASE)

def save_weather_data(city: str):
    weather = fetch_weather(city)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO weather (city, temperature, description)
        VALUES (?, ?, ?)
    """, (weather["city"], weather["temperature"], weather["description"]))
    conn.commit()
    conn.close()

def get_weather_data(city: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather WHERE city = ?", (city,))
    result = cursor.fetchall()
    conn.close()
    return result

def update_weather_data(city: str):
    weather = fetch_weather(city)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE weather
        SET temperature = ?, description = ?, timestamp = ?
        WHERE city = ?
    """, (weather["temperature"], weather["description"], datetime.now(), city))
    conn.commit()
    conn.close()

def delete_weather_data(city: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weather WHERE city = ?", (city,))
    conn.commit()
    conn.close()
