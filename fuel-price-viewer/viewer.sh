#!/bin/bash
set -e

OUTPUT_DIR=/output
IMAGE=$OUTPUT_DIR/current_price.png

# Wait for image to appear
while [ ! -f "$IMAGE" ]; do
  echo "Waiting for image..."
  sleep 1
done

# Launch viewer in fullscreen, auto-refreshing
feh --fullscreen --hide-pointer --reload 1 --auto-zoom "$IMAGE"
