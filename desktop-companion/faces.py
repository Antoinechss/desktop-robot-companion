from machine import Pin, SPI
import st7789py as st7789
import time, random
from time import ticks_diff

# Link to hardware
spi = SPI(0, baudrate=31_250_000, sck=Pin(18), mosi=Pin(19))
tft = st7789.ST7789(
    spi, 240, 240, 
    reset=Pin(20, Pin.OUT),   
    cs=Pin(17, Pin.OUT),      
    dc=Pin(16, Pin.OUT),    
)

# ----- Emotions library -----
"""
Format : {'emotion_name': {'eye_l': [(x, y, w, h), ...], 
                           'eye_r': [(x, y, w, h), ...], 
                           'mouth':[(x,y,w,h), ...],
                           'duration': float | None 
                           'face color': st7789.COLOUR,
                           'background_color': st7789.COLOUR,
                           'add_on': {'coords': [...] 'color': ...}
                           }, ... }
"""

EMOTIONS = {
    "neutral": {
        "eye_l": [(55, 60, 45, 70)],
        "eye_r": [(140, 60, 45, 70)],
        "mouth": [(85, 170, 70, 10)], 
        "face_color": st7789.WHITE,
        "duration": None, 
        "background_color": st7789.BLACK,
        "add_on": None
    },
    "neutral_l": {
        "eye_l": [(25, 60, 45, 70)],
        "eye_r": [(100, 60, 45, 70)],
        "mouth": [(70, 170, 70, 10)], 
        "face_color": st7789.WHITE,
        "duration": 2, 
        "background_color": st7789.BLACK,
        "add_on": None
    },
    "neutral_r": {
        "eye_l": [(95, 60, 45, 70)],
        "eye_r": [(170, 60, 45, 70)],
        "mouth": [(100, 170, 70, 10)],
        "face_color": st7789.WHITE,
        "duration": 2, 
        "background_color": st7789.BLACK,
        "add_on": None
    },
    "blink": {
        "eye_l": [(55, 80, 45, 5)],
        "eye_r": [(140, 80, 45, 5)],
        "mouth": [(85, 170, 70, 10)],
        "face_color": st7789.WHITE,
        "duration": 0.015, 
        "background_color": st7789.BLACK,
        "add_on": None
    },
    "wink": {
        "eye_l": [(55, 80, 45, 5)],
        "eye_r": [(140, 80, 45, 70)],
        "mouth": [(85, 170, 70, 10)],
        "face_color": st7789.WHITE,
        "duration": 0.02, 
        "background_color": st7789.BLACK,
        "add_on": None
    },
    "angry": {"eye_l": [(55, 60, 15, 70), (70, 70, 15, 60), (85, 80, 15, 50)],
        "eye_r": [(140, 80, 15, 50), (155, 70, 15, 60), (170, 60, 15, 70)],
        "mouth": [(95, 170, 50, 10), (85, 180, 10, 10), (145, 180, 10, 10)],
        "face_color": st7789.RED,
        "duration": None, 
        "background_color": st7789.BLACK, 
        "add_on": None
    },
    "sad": {"eye_l": [(55, 80, 15, 50), (70, 70, 15, 60), (85, 60, 15, 70)],
        "eye_r": [(140, 60, 15, 70), (155, 70, 15, 60), (170, 80, 15, 50)],
        "mouth": [(95, 170, 50, 10), (85, 180, 10, 10), (145, 180, 10, 10)],
        "face_color": st7789.WHITE,
        "duration": None, 
        "background_color": st7789.BLACK, 
        "add_on": None
    },
    "happy": {
        "eye_l": [(55, 60, 45, 55)],
        "eye_r": [(140, 60, 45, 55)],
        "mouth": [(95, 170, 50, 10), (85, 160, 10, 10), (145, 160, 10, 10)], 
        "face_color": st7789.WHITE,
        "duration": None, 
        "background_color": st7789.BLACK,
        "add_on": None
    },
    "suspicious": {
        "eye_l": [(55, 80, 45, 10)],
        "eye_r": [(140, 80, 45, 10)],
        "mouth": [(85, 170, 70, 10)],
        "face_color": st7789.WHITE,
        "duration": None, 
        "background_color": st7789.BLACK,
        "add_on": None
    },
    "surprise": {"eye_l": [(55, 60, 45, 70)],
        "eye_r": [(140, 60, 45, 70)],
        "mouth": [(100, 160, 40, 30)],
        "face_color": st7789.WHITE,
        "duration": None, 
        "background_color": st7789.BLACK, 
        "add_on": None
    },
    "sleeping": {
        "eye_l": [(55, 80, 45, 3)],
        "eye_r": [(140, 80, 45, 3)],
        'mouth': [(85, 173, 70, 4)],
        "face_color": st7789.CYAN,
        "duration": None, 
        "background_color": st7789.BLACK,
        "add_on": None
    },
    "blush": {
        "eye_l": [(55, 60, 45, 30)],
        "eye_r": [(140, 60, 45, 30)],
        "mouth": [(95, 170, 50, 10), (85, 160, 10, 10), (145, 160, 10, 10)], 
        "face_color": st7789.WHITE,
        "duration": None, 
        "background_color": st7789.BLACK,
        "add_on": {'coords': [(35, 130, 30, 14), (175, 130, 30, 14)], 'color': st7789.color565(255, 110, 150)}
    },
}

# ----- Rendering Function -----

def render_emotion(emotion: str, tft): 
    """Fetches face params and renders on hardware"""
    emo =  EMOTIONS[emotion]
    face_color = emo['face_color']

    # --- Background
    background_color = emo['background_color']
    tft.fill(background_color) 

    # --- Render Eyes : 
    for r in emo['eye_l']: 
        tft.fill_rect(*r, face_color) 
    for r in emo['eye_r']: 
        tft.fill_rect(*r, face_color) 

    # --- Render Mouth
    for r in emo['mouth']: 
        tft.fill_rect(*r, face_color) 

    # --- Render Add Ons 
    if emo['add_on'] is not None: 
        for r in emo['add_on']['coords']: 
            tft.fill_rect(*r, emo['add_on']['color']) 

# ----- MAIN LOOP ----- 

"""
Random gazes between left, right, blink from a neutral face. 
Sleeps after a given time of inactivity. 
"""

SLEEP_AFTER = 30000 # 30s

last_activity = time.time()
asleep = False

while True: 

    now = time.time()
    render_emotion('neutral', tft)
    time.sleep(random.randint(1, 5))
    next_gaze = random.choice(['neutral_l', 'neutral_r', 'blink'])
    render_emotion(next_gaze, tft)
    time.sleep(EMOTIONS[next_gaze]['duration'])

    if ticks_diff(now, last_activity) > SLEEP_AFTER: 
        while True: 
            render_emotion('sleeping', tft)
            time.sleep(10)



