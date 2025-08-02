# Fuel Price Display (Edge Demo)

This project simulates a gas station fuel price sign using MQTT and Pillow. It can run either with real MQTT data or with simulated price updates in a Podman container on Red Hat Device Edge.

---
Architecture
┌────────────────────────┐     ┌────────────────────────────┐
│ Pricing Container      │     │ Display Container          │
│ ─ Updates PNG file     │ ==> │ ─ Shows PNG in fullscreen  │
│ ─ Writes to /output    │     │ ─ Reads /output            │
└────────────────────────┘     └────────────────────────────┘
                 Shared volume (/output) mounted with :Z






---

## 🔧 Local Development

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/fuel-price-display.git
cd fuel-price-display

