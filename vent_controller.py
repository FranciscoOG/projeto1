import paho.mqtt.client as mqtt
import ssl

with open('limit.txt', 'r') as f:
    limit = int(f.readline())

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("/tvoc")  # Subscribe to tvoc topic
    client.subscribe("/limit")  # Subscribe to limit topic sent by web interface
    client.subscribe("/on")  # Subscribe to on to send first limit value to webpage

# When messages are received
def on_message(client, userdata, msg):
    global limit
    if msg.topic == "/tvoc":
        tvoc = int(msg.payload)
        if tvoc >= 200 and tvoc <= limit:
            pwm = round(convert(tvoc, 200, limit, 25, 255))
        elif tvoc < 200:
            pwm = 25
        elif tvoc > limit:
            pwm = 255

        if prev_tvoc != tvoc:  # Fixed indentation here
            (rc, mid) = client.publish('/pwm', str(pwm))
            prev_tvoc = tvoc

    elif msg.topic == "/limit":
        limit = int(msg.payload)
        if limit > 3000 or limit < 200:
            limit = 1400
            (rc, mid) = client.publish('/limit', str(limit))
        with open('limit.txt', 'w') as f:
            f.write(str(limit))

    elif msg.topic == "/on":
        (rc, mid) = client.publish('/limit', str(limit))

# Calculates correct PWM depending on TVOC value received
def convert(value, min, max, c_min, c_max):
    value = ((value - min) * (c_max - c_min)) / (max - min) + c_min
    return value

# MQTT Client Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set("./certs/ca.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)
client.connect("192.168.1.134", 8883)
client.loop_forever()
