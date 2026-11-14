# --- Pins
SPI_SCK = 18
SPI_MOSI = 19
SPI_BAUD = 31_250_000
TFT_CS = 17
TFT_DC = 16
TFT_RST = 20
TFT_SIZE = 240
PAN_PIN = 14
TILT_PIN = 15

# --- Servo
SERVO_FREQ = 50
EASE = 0.15 # fraction of remaining distance to target covered every 10ms 
HALF_FOV = 33       # camera horizontal half-angle
HALF_VFOV = 26      # camera vertical half-angle
# Pan
PAN_CENTER = 115
PAN_MIN = 50
PAN_MAX = 155
# Tilt 
TILT_CENTER = 45
TILT_MIN = 10
TILT_MAX = 100

# --- Timings 
BLINK_DURATION = 150
BLINK_MIN = 2000
BLINK_MAX = 6000
GAZE_MIN = 1500
GAZE_MAX = 4000
IDLE_AFTER = 3000
SLEEP_AFTER = 30000

# --- Gaze 
GAZE_RANGE = 25