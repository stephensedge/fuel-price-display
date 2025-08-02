import time
import math
import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw, ImageFont
import os

# Load font
FONT_PATH = "./fonts/DSEG7Classic-Bold.ttf"
FONT_SIZE = 100
if os.path.exists(FONT_PATH):
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
else:
    font = ImageFont.load_default()

def update_display(price):
    img = Image.new('RGB', (400, 200), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    price_text = f"${float(price):.2f}"
    bbox = draw.textbbox((0, 0), price_text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((400 - w) / 2, (200 - h) / 2), price_text, font=font, fill=(255, 0, 0))
    img.save("output/current_price.png")
    print(f"Displayed new price: {price_text}")

# --- Config ---
BROKER = os.getenv("MQTT_BROKER", "localhost")
TOPIC = "station/price"
USE_MQTT = os.getenv("USE_MQTT", "false").lower() == "true"

# --- MQTT Logic ---
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    update_display(payload)

def run_mqtt():
    client = mqtt.Client("price_display_subscriber")
    client.on_message = on_message
    client.connect(BROKER, 1883)
    client.subscribe(TOPIC)
    client.loop_forever()

# --- Simulation Logic ---
def run_simulation():
    t = 0
    while True:
        price = 3.00 + 0.5 * math.sin(t)
        update_display(price)
        t += 0.1
        time.sleep(1)

# --- Main ---
if USE_MQTT:
    print("Starting in MQTT mode...")
    run_mqtt()
else:
    print("Starting in Simulation mode...")
    run_simulation()
