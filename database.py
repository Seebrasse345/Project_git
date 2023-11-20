import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect('sensor_data.db')

def create_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_readings (
                            sensor_name TEXT PRIMARY KEY,
                            location TEXT,
                            temperatures TEXT,
                            humidities TEXT,
                            timestamps TEXT)''')
        conn.commit()

def update_sensor_data(sensor_name, temperature, humidity):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    location = "53.38102899, -1.48647327"  # Set location for each update

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT temperatures, humidities, timestamps FROM sensor_readings WHERE sensor_name = ?', (sensor_name,))
        row = cursor.fetchone()

        new_temperatures = f"{row[0]},{temperature}" if row else str(temperature)
        new_humidities = f"{row[1]},{humidity}" if row else str(humidity)
        new_timestamps = f"{row[2]},{current_time}" if row else current_time

        cursor.execute('''INSERT OR REPLACE INTO sensor_readings 
                          (sensor_name, location, temperatures, humidities, timestamps)
                          VALUES (?, ?, ?, ?, ?)''', 
                          (sensor_name, location, new_temperatures, new_humidities, new_timestamps))
        conn.commit()

def get_device_sensor_data(device_id, start_time, end_time):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT temperatures, humidities, timestamps FROM sensor_readings WHERE sensor_name = ?', (device_id,))
        row = cursor.fetchone()
        if row:
            temperatures = row[0].split(',')
            humidities = row[1].split(',')
            timestamps = row[2].split(',')
            sensor_data = [(float(temp), float(hum)) for temp, hum, timestamp in zip(temperatures, humidities, timestamps)
                           if start_time <= datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') <= end_time]
            return sensor_data
        else:
            return []

