import sys, time
sys.path.insert(0, "..")         
from camera import setup_camera
from detection import parse_poses
from config import POSE_MODEL

imx500, picam2, intrinsics, frame_w, frame_h = setup_camera(POSE_MODEL, "pose estimation")

while True:
    faces = parse_poses(picam2.capture_metadata(), imx500)
    if faces:
        f = max(faces, key=lambda f: f.score)
        print(f"face x={f.center[0]:+.2f} y={f.center[1]:+.2f} score={f.score:.2f}")
    else:
        print("no face")
    time.sleep(0.2)