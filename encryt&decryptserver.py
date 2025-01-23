import paho.mqtt.client as mqtt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Load keys
with open('private.pem', 'rb') as f:
    private_key = RSA.import_key(f.read())

with open('public.pem', 'rb') as f:
    public_key = RSA.import_key(f.read())

# Encrypt message
def encrypt_message(message):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(message.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

# Decrypt message
def decrypt_message(encrypted_message):
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_bytes = base64.b64decode(encrypted_message)
    decrypted = cipher.decrypt(encrypted_bytes)
    return decrypted.decode('utf-8')

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("/tvoc")       # Subscribe to plaintext topic
    client.subscribe("/encrypted")  # Subscribe to encrypted topic

def on_message(client, userdata, msg):
    if msg.topic == "/tvoc":
        # Encrypt and forward to /encrypted
        plaintext = msg.payload.decode('utf-8')
        encrypted = encrypt_message(plaintext)
        print(f"Encrypted message: {encrypted}")
        client.publish("/encrypted", encrypted)

    elif msg.topic == "/encrypted":
        # Decrypt and forward to /alert
        encrypted = msg.payload.decode('utf-8')
        decrypted = decrypt_message(encrypted)
        print(f"Decrypted message: {decrypted}")
        client.publish("/alert", decrypted)

# MQTT Client Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.134", 1883, 60)  # Adjust broker IP and port
client.loop_forever()