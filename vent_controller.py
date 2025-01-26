import paho.mqtt.client as mqtt
import ssl

limit = 6000

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("/tvoc")       # Subscribe to tvoc topic
    client.subscribe("/limit")  # Subscribe to limit topic send by web interface

# When messages are received

def on_message(client, userdata, msg):
    global limit
    if msg.topic == "/tvoc":
        tvoc = int(msg.payload)
        if tvoc >= 200 and tvoc <= limit:
            tvoc = round(convert(tvoc,200,limit,25,255))
            (rc,mid)=client.publish('/pwm',str(tvoc))
        elif tvoc <200:
            (rc,mid)=client.publish('/pwm','25')
        elif tvoc > limit:
            (rc,mid)=client.publish('/pwm','255')
    elif msg.topic == "/limit":
        limit = int(msg.payload)
    
# calculates correct PWM depending on TVOC value received

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
