import time
import random
import os
import paho.mqtt.client as mqtt

broker = os.getenv("MQTT_BROKER", "localhost")
topic = "station/price"
interval = int(os.getenv("PUBLISH_INTERVAL", "5"))

client = mqtt.Client()
client.connect(broker, 1883)
client.loop_start()

while True:
    price = round(random.uniform(3.25, 4.25), 2)
    print(f"Publishing price: {price}", flush=True)
    client.publish(topic, f"{price}")
    time.sleep(interval)
