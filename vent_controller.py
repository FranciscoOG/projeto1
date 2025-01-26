import paho.mqtt.client as mqtt

limit = 6000

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("/tvoc")       # Subscribe to tvoc topic
    client.subscribe("/limit")  # Subscribe to limit topic send by web interface


def on_message(client, userdata, msg):
    global limit
    if msg.topic == "/tvoc":
        # Encrypt and forward to /encrypted
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
    

def convert(value, min, max, c_min, c_max):
        value = ((value - min) * (c_max - c_min)) / (max - min) + c_min
        return value


# MQTT Client Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username="admin", password="admin")
client.connect("192.168.1.134", 1883)  # Adjust broker IP and port
client.loop_forever()