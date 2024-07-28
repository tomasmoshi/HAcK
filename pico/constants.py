from dotenv import load_dotenv
import os
SSID = os.getenv('HAcK-Project-WiFi-1')
PASSWORD = os.getenv('UCLA.HAcK.2024.Summer')
# MQTT configuration
CONNECT_URL = os.getenv('mqtts://6d8f865c2be44d7ca70d8dff7cedaa2c.s1.eu.hivemq.cloud:8883')
MQTT_USER = os.getenv('Nodeserver')
MQTT_PASS = os.getenv('Nodeserver1')