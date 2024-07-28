from machine import Pin, PWM
import utime
import json
from connections import connect_mqtt, connect_internet
from constants import ssid, mqtt_server, mqtt_user, mqtt_pass
from dht import DHT11

# Motor control pins for the L298N
IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)
IN3 = Pin(4, Pin.OUT)
IN4 = Pin(5, Pin.OUT)

# Servo control
servo = PWM(Pin(15))
servo.freq(50)

def set_angle(angle):
    duty = int(40 + (angle / 180.0) * 115)
    servo.duty_u16(duty)

def forward():
    IN1.high()
    IN2.low()
    IN3.high()
    IN4.low()

def backward():
    IN1.low()
    IN2.high()
    IN3.low()
    IN4.high()

def rotate_clockwise():
    IN1.high()
    IN2.low()
    IN3.low()
    IN4.high()

def rotate_counterclockwise():
    IN1.low()
    IN2.high()
    IN3.high()
    IN4.low()

def stop():
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.low()

# Sensor reading
sensor = DHT11(Pin(28))

def read_sensors():
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    data = {
        "temperature": temp,
        "humidity": hum
    }
    return json.dumps(data)

# Function to handle an incoming message
def cb(topic, msg):
    print(f"Topic: {topic}, Message: {msg}")
    if topic == b'rover/control':
        command = msg.decode('utf-8')
        if command == "forward":
            forward()
        elif command == "backward":
            backward()
        elif command == "cw":
            rotate_clockwise()
        elif command == "ccw":
            rotate_counterclockwise()
        elif command == "stop":
            stop()
        elif command.startswith("servo"):
            angle = int(command.split()[1])
            set_angle(angle)

def main():
    try:
        connect_internet(ssid)
        client = connect_mqtt(mqtt_server, mqtt_user, mqtt_pass)
        client.set_callback(cb)
        client.subscribe(b'rover/control')

        while True:
            client.check_msg()
            sensor_data = read_sensors()
            client.publish(b'rover/sensors', sensor_data)
            utime.sleep(5)
    
    except KeyboardInterrupt:
        print('Keyboard interrupt')

if __name__ == "__main__":
    main()
