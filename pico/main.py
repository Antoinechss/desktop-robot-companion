import sys, select, time, random
from machine import PWM, Pin, SPI
import st7789py as st7789
from faces import EMOTIONS, compute_face, draw_face

# Clock on GP18, Data on GP19
# baudrate = speed : 31M bits/secs
spi = SPI(0, baudrate=31_250_000, sck=Pin(18), mosi=Pin(19))

# --- Screen & bus setup, size and pluggins
tft = st7789.ST7789(  # Screen
    spi,
    240,
    240,  # Size
    reset=Pin(20, Pin.OUT),  # RT control endpoint
    cs=Pin(17, Pin.OUT),  # TC control endpoint
    dc=Pin(16, Pin.OUT),  # DC control endpoint
)

# --- Servo setup
servo = PWM(Pin(14))
servo.freq(50)


def set_angle(angle):
    angle = max(0, min(180, angle))
    pulse_width_ns = int(500000 + (angle / 180.0) * 2000000)
    servo.duty_ns(pulse_width_ns)


# --- System Read
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)  # Data available for reading


def parse_order(line):
    """
    Checks line format, parses content and orders
    Converts cx_scaled position into angle for the servo
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
            servo_angle = 33 * cx_scaled + 90
            return ("look", servo_angle)
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


# --- Emotion neutral start
emotion = "neutral"
old_rects = []
tft.fill(st7789.BLACK)
new_rects = compute_face(emotion, 0, False)
old_rects = draw_face(tft, old_rects, new_rects, EMOTIONS[emotion]['background_color'])
blinking = False
next_event = time.ticks_ms()

while True:
    now = time.ticks_ms()

    # --- Blink management
    if time.ticks_diff(now, next_event) >= 0 and emotion != "sleeping": 
        if not blinking: # Eyes open --> make them blink 
            blinking = True
            next_event = time.ticks_add(now, 150)
        else:  # Blinking --> make it reopen and set next random event
            blinking = False 
            next_event = time.ticks_add(now, random.randint(2000, 6000)) # random time in 2-6 seconds 
        new_rects = compute_face(emotion, 0, blinking)
        old_rects = draw_face(tft, old_rects, new_rects, EMOTIONS[emotion]['background_color']) 

    if poll.poll(0):
        line = sys.stdin.readline()
        order = parse_order(line)
        if order is not None:
            cmd, value = order
            if cmd == "look":
                set_angle(value)
            elif cmd == "emo":
                blinking = False
                emotion = str(value)
                new_rects = compute_face(emotion, 0, blinking)
                old_rects = draw_face(tft, old_rects, new_rects, EMOTIONS[emotion]['background_color'])
    time.sleep(0.01)
