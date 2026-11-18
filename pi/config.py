# --- Body detection model (kept as a fallback, not used by track_and_pan)
MODEL = "/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk"
CONFIDENCE_THRESHOLD = 0.5   # min detection confidence
PERSON_CLASS = 0             # COCO class id for "person"

# --- Pose model (face position: nose, eyes as fallback)
POSE_MODEL = "/usr/share/imx500-models/imx500_network_higherhrnet_coco.rpk"
POSE_SIZE_H_W = (480, 640)   # keypoint space (height, width) used by the parser
POSE_THRESHOLD = 0.3         # per-person confidence
KP_THRESHOLD = 0.3           # per-keypoint confidence

# --- Serial link to the Pico
SERIAL_LINK = "/dev/ttyACM0"
SPEED = 115200

# --- Tracking (relative P-controller, camera on the head)
K = 0.3              # P-gain: fraction of the face offset corrected per step
DEAD_ZONE = 0.05     # min face offset from the image centre before correcting
MIN_INTERVAL = 0.1   # min seconds between two corrections sent to the Pico
LOST_TIMEOUT = 3.0   # seconds without a face before the head returns to centre