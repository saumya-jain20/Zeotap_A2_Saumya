import requests
import sqlite3
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Configurable settings
API_KEY = '9ec77dd00186a29a2ca49a0dbfc9cdb4'
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
API_URL = "https://api.openweathermap.org/data/2.5/weather"
INTERVAL = 300  # Interval to poll the API (e.g., 300 seconds = 5 minutes)
TEMP_THRESHOLD = 35.0  # Temperature threshold for alerts in Celsius
ALERT_CONSECUTIVE_THRESHOLD = 2  # Number of consecutive breaches before alert

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather
                      (city TEXT, timestamp INTEGER, temp REAL, feels_like REAL, main TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS alerts
                      (city TEXT, timestamp INTEGER, alert_message TEXT)''')
    conn.commit()
    conn.close()

# Get weather data from OpenWeatherMap
def get_weather_data(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}  # Using metric for Celsius
    response = requests.get(API_URL, params=params)
    return response.json()

# Store weather data in the database
def store_weather_data(city, data):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO weather (city, timestamp, temp, feels_like, main) 
                      VALUES (?, ?, ?, ?, ?)''', 
                   (city, data['dt'], data['main']['temp'], data['main']['feels_like'], data['weather'][0]['main']))
    conn.commit()
    conn.close()

# Retrieve daily rollups and aggregates
def calculate_daily_summary(city):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    
    # Calculate daily aggregates
    today_start = int(time.mktime(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timetuple()))
    cursor.execute('''SELECT AVG(temp), MAX(temp), MIN(temp), main
                      FROM weather WHERE city = ? AND timestamp >= ? GROUP BY main
                      ORDER BY COUNT(main) DESC LIMIT 1''', (city, today_start))
    data = cursor.fetchone()
    
    conn.close()
    return data

# Check for threshold breach and trigger alert
def check_thresholds(city, data):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    
    # Check temperature threshold (e.g., if temp > 35 for 2 consecutive updates)
    cursor.execute('''SELECT temp FROM weather WHERE city = ? ORDER BY timestamp DESC LIMIT 2''', (city,))
    temps = cursor.fetchall()
    
    if len(temps) >= ALERT_CONSECUTIVE_THRESHOLD and all(t[0] > TEMP_THRESHOLD for t in temps):
        alert_message = f"ALERT: {city} has exceeded {TEMP_THRESHOLD}°C for {ALERT_CONSECUTIVE_THRESHOLD} consecutive updates."
        cursor.execute('''INSERT INTO alerts (city, timestamp, alert_message) 
                          VALUES (?, ?, ?)''', (city, int(time.time()), alert_message))
        print(alert_message)
    
    conn.commit()
    conn.close()

# Main function to process weather data
def monitor_weather():
    init_db()  # Ensure DB is initialized
    
    while True:
        for city in CITIES:
            data = get_weather_data(city)
            store_weather_data(city, data)
            check_thresholds(city, data)
        
        time.sleep(INTERVAL)  # Poll at the configured interval

# Visualization
def visualize(city):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    
    # Retrieve last 7 days of data
    seven_days_ago = int(time.mktime((datetime.now() - timedelta(days=7)).timetuple()))
    cursor.execute('''SELECT timestamp, temp FROM weather WHERE city = ? AND timestamp >= ?''', (city, seven_days_ago))
    data = cursor.fetchall()
    
    # Plot the temperature trend
    timestamps = [datetime.fromtimestamp(row[0]) for row in data]
    temps = [row[1] for row in data]
    
    plt.plot(timestamps, temps, label=city)
    plt.xlabel('Time')
    plt.ylabel('Temperature (Celsius)')
    plt.title(f'Temperature Trend for {city}')
    plt.legend()
    plt.show()

    conn.close()

if __name__ == '__main__':
    try:
        monitor_weather()
    except KeyboardInterrupt:
        print("Monitoring stopped.")
