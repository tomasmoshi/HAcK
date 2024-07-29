from connections import connect_mqtt, connect_internet
#from constants import SSID, PASSWORD, MQTT_SERVER, MQTT_USER, MQTT_PASS
from Temperature import read_temperature
from ultrasonic_sensor import measure_distance
import movement
import time

SSID = 'HAck-Project-WiFi-1'
PASSWORD = 'UCLA.HAcK.2024.Summer'

# MQTT configuration
MQTT_SERVER = '6d8f865c2be44d7ca70d8dff7cedaa2c.s1.eu.hivemq.cloud'
MQTT_USER = 'Nodeserver'
MQTT_PASS = 'Nodeserver1'

def cb(topic, msg):
    print(f"Topic: {topic}, Message: {msg}")
    command = msg
    if command == b"forward":
        print('hello')
        movement.forward()
    elif command == b"backward":
        movement.backward()
    elif command == b"left":
        movement.rotate_clockwise()
    elif command == b"right":
        movement.rotate_counterclockwise()
    elif command == b"stop":
        movement.stop()
    elif b"servo" in command:
        try:
            angle = int(command.decode().split(" ")[1])
            movement.set_angle(angle)
        except (IndexError, ValueError):
            print("Invalid servo command format")

def main():
    try:
        print("Connecting to the internet...")
        connect_internet('HAck-Project-WiFi-1', 'UCLA.HAcK.2024.Summer')
        print("Connecting to MQTT...")
        client = connect_mqtt('6d8f865c2be44d7ca70d8dff7cedaa2c.s1.eu.hivemq.cloud', 'Nodeserver', 'Nodeserver1')
        client.set_callback(cb)
        client.subscribe("direction")
        print("Connected to MQTT and subscribed to 'direction' topic")

        while True:
            try:
                client.check_msg()
                time.sleep(0.2)  # Check MQTT messages more frequently

                temp, hum = read_temperature()
                distance = measure_distance()

                if temp is not None and hum is not None and distance is not None:
                    temp_str = f"Temperature: {temp} C"
                    hum_str = f"Humidity: {hum} %"
                    distance_str = f"Distance: {distance} cm"
                    client.publish("temp", temp_str)
                    client.publish("humidity", hum_str)
                    client.publish("distance", distance_str)
                    print(f"Published - {temp_str}, {hum_str}, {distance_str}")
                
                time.sleep(.5)

            except Exception as e:
                print(f"Error in main loop: {e}")

    except KeyboardInterrupt:
        print('Keyboard interrupt')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()