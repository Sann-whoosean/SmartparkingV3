import paho.mqtt.client as mqtt
from mqtt_handler import init_mqtt

def create_mqtt_client():

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) 

    init_mqtt(client)

    client.connect("broker.hivemq.com", 1883, 60)
    
    client.loop_start()
    
    return client

mqtt_client = create_mqtt_client()