import time
import os
import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw, ImageFont
import subprocess

# Settings
OUTPUT_PATH = "/output/current_price.png"
BROKER = os.getenv("MQTT_BROKER", "localhost")
TOPIC = "station/price"

FONT_PATH = "/fonts/DSEG7Classic-Bold.ttf"
FONT_SIZE = 100
font = ImageFont.truetype(FONT_PATH, FONT_SIZE) if os.path.exists(FONT_PATH) else ImageFont.load_default()

# Draw new price to screen
def update_display(price):
    try:
        img = Image.new('RGB', (400, 200), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        price_text = f"${float(price):.2f}"
        bbox = draw.textbbox((0, 0), price_text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((400 - w) / 2, (200 - h) / 2), price_text, font=font, fill=(255, 0, 0))
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        img.save(OUTPUT_PATH)
        print(f"✅ Updated display to: {price_text}")
    except Exception as e:
        print(f"❌ Error drawing image: {e}")

# MQTT message received
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"📩 MQTT Message received: {payload}")
    update_display(payload)

# MQTT connection established
def on_connect(client, userdata, flags, rc):
    print(f"🔌 Connected to MQTT broker at {BROKER} with result code {rc}")
    client.subscribe(TOPIC)
    print(f"📡 Subscribed to topic: {TOPIC}")

# Set up MQTT client
print(f"🔄 Connecting to MQTT broker at {BROKER}...")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER, 1883)
except Exception as e:
    print(f"❌ MQTT connection failed: {e}")
    exit(1)

client.loop_start()

# Start fullscreen viewer
subprocess.Popen(["feh", "--fullscreen", "--hide-pointer", "--reload", "1", "--auto-zoom", OUTPUT_PATH])

# Stay alive
while True:
    time.sleep(1)
