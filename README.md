# Fuel Price Display (Edge Demo)

This project simulates a gas station fuel price sign using MQTT and Pillow. It can run either with real MQTT data or with simulated price updates in a Podman container on Red Hat Device Edge.

---
Architecture- There are three containers that make this fuel pricing demo. 

price-publisher: Generates and publishes gas prices

mqtt-broker: Routes messages between publisher and subscribers (MQTT)

price-viewer-mqtt: Subscribes to price updates and displays them in fullscreen using Pillow and FEH
```
+---------------------+          +----------------------+
|                     |          |                      |
|  price-publisher    |          |  price-viewer-mqtt   |
|  ----------------   |          |  ------------------  |
|  Publishes fuel     |          |  Subscribes to       |
|  prices to MQTT     +--------->  'station/price'      |
|  topic              |          |  topic and renders    |
|                     |          |  full-screen display  |
+---------------------+          +----------------------+
             |                               |
             |                               |
             v                               v
               +--------------------------+
               |                          |
               |     mqtt-broker          |
               |  (Eclipse Mosquitto)     |
               |                          |
               +--------------------------+


```

---

## Container Roles

### `price-publisher`

- Simulates fluctuating gas prices every few seconds
- Publishes to the topic `station/price`
- Written in Python with `paho-mqtt`
- Container is rebuilt from a `Containerfile` that copies `publisher.py`
- Uses environment variables:
  - `MQTT_BROKER=host.containers.internal`
  - `PUBLISH_INTERVAL=5` (seconds)

### `mqtt-broker`

- Provides MQTT communication service using Eclipse Mosquitto
- Listens on port `1883`
- Lightweight, single-purpose container
- Configuration is stored in `mosquitto.conf` with `allow_anonymous true`

### `price-viewer-mqtt`

- Subscribes to the `station/price` MQTT topic
- Creates a PNG image of the current price using Pillow
- Displays image fullscreen using `feh` in kiosk mode
- Uses a 7-segment-style digital font (DSEG7Classic)
- Environment variables:
  - `MQTT_BROKER=host.containers.internal`
  - `DISPLAY=$DISPLAY` (for X11 forwarding)

---

## What is MQTT?

**MQTT (Message Queuing Telemetry Transport)** is a lightweight messaging protocol used for pub-sub (publish-subscribe) communication. It's ideal for IoT and sensor networks because it’s simple, fast, and efficient.

In this project:

- `price-publisher` **publishes** messages to a topic
- `price-viewer-mqtt` **subscribes** to that topic and reacts to updates
- `mqtt-broker` acts as the **middleman** that routes messages

---

## Requirements

- Red Hat Enterprise Linux 9+ or Fedora
- Podman (rootless or root)
- X11 forwarding enabled (for viewer)

---

## Usage

1. Start the MQTT Broker  
   ```bash
   podman run -d --name mqtt-broker \
     -p 1883:1883 \
     -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf:Z \
     docker.io/eclipse-mosquitto:latest

2. Build and Run the Publisher
```bash
cd fuel-price-publisher
podman build -t localhost/fuel-price-publisher .
podman run -d --name price-publisher \
  -e MQTT_BROKER=host.containers.internal \
  localhost/fuel-price-publisher```

3. **Build and Run the Viewer**
```bash
   cd fuel-price-viewer
podman build -f Containerfile.mqtt -t localhost/fuel-price-viewer:mqtt .
podman run -d --name price-viewer-mqtt \
  -e DISPLAY=$DISPLAY \
  -e MQTT_BROKER=host.containers.internal \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd)/output:/output:Z \
  --security-opt label=type:container_runtime_t \
  localhost/fuel-price-viewer:mqtt


---

## 🔧 Local Development

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/fuel-price-display.git
cd fuel-price-display

When working with testing prior to adding changes to the container use python venv env to work with
NOTES:
python3 -m venv .venv
source .venv/bin/activate
pip install pillow paho-mqtt
pip freeze > requirements.txt

