from camera import setup_camera
from pico_link import open_link, send
from detection import parse_detections
import time
from config import ALPHA, LOST_TIMEOUT, MIN_INTERVAL, DEAD_ZONE

# --- Setup
imx500, picam2, intrinsics, frame_w, frame_h = setup_camera()
ser = open_link()

# --- State variables
smooth = None
last_sent_value = 0
last_sent_time = time.monotonic()
last_seen_time = time.monotonic()
centered = False

try:
    while True:
        now = time.monotonic()
        frame_detections = parse_detections(
            picam2.capture_metadata(), imx500, picam2, intrinsics, frame_w, frame_h
        )
        # Case A: ≥1 target detected
        if frame_detections:
            target = max(
                frame_detections, key=lambda d: d.box[2] * d.box[3]
            )  # pick biggest detected box by w*h
            centered = False
            last_seen_time = now

            # EMA Smoothing of target center
            x = target.center[0]
            if smooth is None:
                smooth = x
            else:
                smooth = ALPHA * x + (1 - ALPHA) * smooth

            if (
                now - last_sent_time > MIN_INTERVAL
                and abs(smooth - last_sent_value) > DEAD_ZONE
            ):
                send(ser, f"look {smooth:.2f}")
                last_sent_time = now
                last_sent_value = smooth

        # Case B: 0 target detected, back to neutral after timeout
        else:
            if now - last_seen_time > LOST_TIMEOUT and not centered:
                send(ser, "look 0.0")
                centered = True
                smooth = None
                last_sent_time = now
                last_sent_value = 0.0

finally:
    ser.close()
