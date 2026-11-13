import sys, select, time, random
from machine import PWM, Pin, SPI
import st7789py as st7789
from faces import EMOTIONS, compute_face, draw_face
from config import (
    SPI_BAUD,
    SPI_SCK,
    SPI_MOSI,
    TFT_SIZE,
    TFT_RST,
    TFT_DC,
    TFT_CS,
    PAN_PIN,
    SERVO_FREQ,
    BLINK_DURATION,
    BLINK_MIN,
    BLINK_MAX,
    IDLE_AFTER,
    SLEEP_AFTER,
    GAZE_RANGE,
    GAZE_MIN,
    GAZE_MAX,
    HALF_FOV,
    TILT_PIN,
    PAN_CENTER, 
    PAN_MIN, 
    PAN_MAX, 
    TILT_CENTER, 
    TILT_MIN, 
    TILT_MAX, 
    HALF_VFOV
)

# Clock on GP18, Data on GP19
# baudrate = speed : 31M bits/secs
spi = SPI(0, baudrate=SPI_BAUD, sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))

# --- Screen & bus setup, size and pluggins
tft = st7789.ST7789(  # Screen
    spi,
    TFT_SIZE,
    TFT_SIZE,  # Size
    reset=Pin(TFT_RST, Pin.OUT),  # RT control endpoint
    cs=Pin(TFT_CS, Pin.OUT),  # TC control endpoint
    dc=Pin(TFT_DC, Pin.OUT),  # DC control endpoint
)

# --- Servo setup
pan = PWM(Pin(PAN_PIN)); pan.freq(SERVO_FREQ)
tilt = PWM(Pin(TILT_PIN)); tilt.freq(SERVO_FREQ)


def set_angle(servo, angle, lo, hi):
    angle = max(lo, min(hi, angle))
    pulse_width_ns = int(500000 + (angle / 180.0) * 2000000)
    servo.duty_ns(pulse_width_ns)


# --- System Read
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)  # Data available for reading


def parse_order(line):
    """
    Checks line format, parses content and orders
    Converts cx_scaled cy_scaled position into angle for the servo
    Fetches emotion for face orders
    """
    line_items = line.strip().split()

    if not line_items:
        return None

    cmd = line_items[0]

    # --- Pan Servo order
    if cmd == "look":
        try:
            cx_scaled = float(line_items[1])  # Read the scaled detection x
            cx_scaled = max(-1, min(1, cx_scaled))  # clamp between [-1, 1]
            pan_angle = PAN_CENTER - HALF_FOV * cx_scaled 
            if len(line_items) > 2:
                cy_scaled = float(line_items[2])
                cy_scaled = max(-1, min(1, cy_scaled))
                tilt_angle = TILT_CENTER + HALF_VFOV * cy_scaled 
            else: 
                tilt_angle = None

            return ("look", (pan_angle, tilt_angle))
        except (ValueError, IndexError):
            return None

    # --- Face order
    elif cmd == "emo":
        try:
            emotion = line_items[1]
            if emotion in EMOTIONS:
                return ("emo", emotion)
        except IndexError:
            return None


def redraw(old_rects):
    new_rects = compute_face(emotion, gaze_dx, blinking)
    return draw_face(tft, old_rects, new_rects, EMOTIONS[emotion]["background_color"])


# ---- Main loop ----

now = time.ticks_ms()
mode = "idle"
idle_since = now
last_look = time.ticks_add(now, -10000)
gaze_dx = 0
next_gaze = now
emotion = "neutral"
blinking = False
next_event = time.ticks_add(now, 3000)

tft.fill(st7789.BLACK)
old_rects = redraw([])  # First draw

# Initial centering
set_angle(pan, PAN_CENTER, PAN_MIN, PAN_MAX)
set_angle(tilt, TILT_CENTER, TILT_MIN, TILT_MAX)

while True:
    now = time.ticks_ms()

    # --- Read serial port
    if poll.poll(0):
        line = sys.stdin.readline()
        order = parse_order(line)
        if order is not None:
            cmd, value = order
            if cmd == "look":
                pan_angle, tilt_angle = value
                set_angle(pan, pan_angle, PAN_MIN, PAN_MAX)
                if tilt_angle is not None:
                    set_angle(tilt, tilt_angle, TILT_MIN, TILT_MAX)
                last_look = now
                if mode == "sleeping":
                    emotion = "neutral"
                mode = "tracking"
                gaze_dx = 0
                old_rects = redraw(old_rects)

            elif cmd == "emo":
                blinking = False
                emotion = str(value)
                old_rects = redraw(old_rects)
                if mode == "sleeping": 
                    mode = "idle"
                    idle_since = now

    # --- Tracking -> Idle
    if mode == "tracking" and time.ticks_diff(now, last_look) >= IDLE_AFTER:
        mode = "idle"
        idle_since = now
        next_gaze = now

    # --- Idle -> Sleeping | Glance
    if mode == "idle":
        if time.ticks_diff(now, idle_since) >= SLEEP_AFTER:
            mode = "sleeping"
            emotion = "sleeping"
            gaze_dx = 0
            blinking = False
            old_rects = redraw(old_rects)
        elif time.ticks_diff(now, next_gaze) >= 0:
            gaze_dx = random.randint(-GAZE_RANGE, GAZE_RANGE)
            next_gaze = time.ticks_add(now, random.randint(GAZE_MIN, GAZE_MAX))
            old_rects = redraw(old_rects)

    # --- Blink management
    if time.ticks_diff(now, next_event) >= 0 and mode != "sleeping":
        if not blinking:  # Eyes open --> make them blink
            blinking = True
            next_event = time.ticks_add(now, BLINK_DURATION)
        else:  # Blinking --> make it reopen and set next random event
            blinking = False
            next_event = time.ticks_add(
                now, random.randint(BLINK_MIN, BLINK_MAX)
            )  # random time in 2-6 seconds
        old_rects = redraw(old_rects)

    time.sleep(0.01)
