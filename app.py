from flask import Flask, jsonify, render_template
from mqtt_sensor_finder import SensorDataProcessor  # Corrected import statement
import threading
import database
import paho
import weatherapi
app = Flask(__name__)
database.create_table()

# Create an instance of the SensorDataProcessor
sensor_processor = SensorDataProcessor()

# Function to start the MQTT client in a separate thread
def start_mqtt_client():
    sensor_processor.run_mqtt_client()

# Start the MQTT client thread when the Flask application starts
mqtt_thread = threading.Thread(target=start_mqtt_client)
mqtt_thread.daemon = True
mqtt_thread.start()

@app.route('/')
def index():
    # Serve the webpage that will display sensor data
    return render_template('index.html')

@app.route('/data')
def data():
    # Use the get_data method from the sensor_processor to fetch the latest sensor data
    temperature, humidity = sensor_processor.get_data()
    # Ensure that the data is not None before sending
    temperature = 23
    humidity = 40
    #These are just debug values for when im at home since no range to update them
    if temperature is not None and humidity is not None:
        return jsonify({
            'temperature': temperature,
            'humidity': humidity
        })
    else:
        # In case the data is None, send a message indicating that data is not available
        return jsonify({'message': 'Sensor data not available yet'}), 503
@app.route('/heatmap-data')
def heatmap_data():
    device_id = "eui-a8610a32303f7904"  # Device ID
    lat, lon = 53.38102899, -1.48647327  # Device coordinates
    data = weatherapi.get_heatmap_data(device_id, lat, lon)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False, port=3000)
