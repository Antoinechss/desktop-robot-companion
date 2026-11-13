# --- Body recognition model (outdated)
MODEL = "/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk"
CONFIDENCE_THRESHOLD = 0.5
PERSON_CLASS = 0

# --- Face recognition model
POSE_MODEL = "/usr/share/imx500-models/imx500_network_higherhrnet_coco.rpk"
POSE_SIZE_H_W = (480, 640)
POSE_THRESHOLD = 0.3      # per-person confidence
KP_THRESHOLD = 0.3        # per-keypoint confidence


# --- Serial link to the Pico
SERIAL_LINK = "/dev/ttyACM0"
SPEED = 115200

# --- Tracking Behaviour
ALPHA = 0.4  # EMA smoothing
DEAD_ZONE = 0.02  # min change in center_x before sending a new command
MIN_INTERVAL = 0.1  # min seconds between two commands to the Pico
LOST_TIMEOUT = 3.0  # seconds without anyone before the head returns to center
