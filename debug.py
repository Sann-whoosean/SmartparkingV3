import paho.mqtt.client as mqtt
import time

BROKER = "broker.hivemq.com"
PORT = 1883


topics = [
    "parking/sandy/rfid/entry",
    "parking/sandy/rfid/exit",
    "parking/sandy/entry/servo",
    "parking/sandy/exit/servo",
    "parking/sandy/lcd"
]

def on_connect(client, userdata, flags, reasonCode, properties=None):
    print("Connected to broker:", reasonCode)
    # Subscribe semua topik
    for t in topics:
        client.subscribe(t)
        print("Subscribed:", t)

# Callback saat ada message masuk
def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}, Payload: {msg.payload.decode()}")

client = mqtt.Client(protocol=mqtt.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_start()

# Publish dummy message ke tiap topik biar keliatan
for t in topics:
    client.publish(t, "TEST", retain=True)
    print(f"Published 'TEST' ke {t}")
    time.sleep(0.5)  # biar nggak nabrak

try:
    while True:
        time.sleep(1)  # biar client tetap running
except KeyboardInterrupt:
    client.loop_stop()
    print("Stopped")