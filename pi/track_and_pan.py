from camera import setup_camera
from pico_link import open_link, send
from detection import parse_poses
import time
from config import LOST_TIMEOUT, MIN_INTERVAL, DEAD_ZONE, POSE_MODEL, K

# --- Setup
imx500, picam2, intrinsics, frame_w, frame_h = setup_camera(POSE_MODEL, "pose estimation")
ser = open_link()


# --- State variables
last_sent_time = time.monotonic()
last_seen_time = time.monotonic()
centered = False
head_x = 0.0
head_y = 0.0

try:
    while True:
        now = time.monotonic()
        faces = parse_poses(picam2.capture_metadata(), imx500)
        # Case A: ≥1 target detected
        if faces:
            target = max(faces, key=lambda f: f.score) # pick biggest score face
            centered = False
            last_seen_time = now

            x, y = target.center
            if now - last_sent_time > MIN_INTERVAL and (abs(x) > DEAD_ZONE or abs(y) > DEAD_ZONE):
                if abs(x) > DEAD_ZONE:
                    head_x += K * x
                if abs(y) > DEAD_ZONE:
                    head_y += K * y

                # Clamp to [-1, 1]
                head_x = max(-1.0, min(1.0, head_x))
                head_y = max(-1.0, min(1.0, head_y))

                send(ser, f"look {head_x:.2f} {head_y:.2f}")
                last_sent_time = now

        # Case B: 0 target detected, back to neutral after timeout
        else:
            if now - last_seen_time > LOST_TIMEOUT and not centered:
                send(ser, "look 0.0 0.0")
                centered = True
                head_x, head_y = 0.0, 0.0
                last_sent_time = now

finally:
    ser.close()
