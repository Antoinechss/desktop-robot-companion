from camera import setup_camera
from pico_link import open_link, send
from detection import parse_detections, parse_poses
import time
from config import ALPHA, LOST_TIMEOUT, MIN_INTERVAL, DEAD_ZONE, MODEL, POSE_MODEL

# --- Setup
imx500, picam2, intrinsics, frame_w, frame_h = setup_camera(POSE_MODEL, "pose estimation")
ser = open_link()


# --- State variables
smooth_x = None
smooth_y = None
last_sent_x = 0.0
last_sent_y = 0.0
last_sent_time = time.monotonic()
last_seen_time = time.monotonic()
centered = False

try:
    while True:
        now = time.monotonic()
        faces = parse_poses(picam2.capture_metadata(), imx500)
        # Case A: ≥1 target detected
        if faces:
            target = max(faces, key=lambda f: f.score) # pick biggest score face
            centered = False
            last_seen_time = now

            # EMA Smoothing of target center
            x = target.center[0]
            y = target.center[1]
            if smooth_x is None:
                smooth_x, smooth_y = x, y
            else:
                smooth_x = ALPHA * x + (1 - ALPHA) * smooth_x
                smooth_y = ALPHA * y + (1 - ALPHA) * smooth_y

            if now - last_sent_time > MIN_INTERVAL and (
                abs(smooth_x - last_sent_x) > DEAD_ZONE
                or abs(smooth_y - last_sent_y) > DEAD_ZONE
            ):
                send(ser, f"look {smooth_x:.2f} {smooth_y:.2f}")
                last_sent_time = now
                last_sent_x = smooth_x
                last_sent_y = smooth_y

        # Case B: 0 target detected, back to neutral after timeout
        else:
            if now - last_seen_time > LOST_TIMEOUT and not centered:
                send(ser, "look 0.0 0.0")
                centered = True
                smooth_x = None
                smooth_y = None
                last_sent_time = now
                last_sent_x = 0.0
                last_sent_y = 0.0

finally:
    ser.close()
