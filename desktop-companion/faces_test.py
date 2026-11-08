from machine import Pin, SPI
import st7789py as st7789
import sys, time, random, select

# Link to hardware 
spi = SPI(0, baudrate=31_250_000, sck=Pin(18), mosi=Pin(19))
tft = st7789.ST7789(
    spi, 240, 240, 
    reset=Pin(20, Pin.OUT),   
    cs=Pin(17, Pin.OUT),      
    dc=Pin(16, Pin.OUT),    
)

# Face template settings 
 
EYE_CENTERS = (78, 162)
EYE_Y = 100

# ----- Emotions library -----
"""
Format : {'emotion_name': {'eye_l': (x, y, w, h), 
                           'eye_r': (x, y, w, h), 
                           'mouth': (x, y, w, h), 
                           'duration': u | None, 
                           'face color': st7789.COLOUR
                           'background_color': st7789.COLOUR}}
"""

EMOTIONS = {
    'neutral': {'eye_l': (55, 60, 45, 70), 
                'eye_r': (140, 60, 45, 70), 
                'mouth': (85, 170, 70, 10), 
                'duration': None, 
                'face_color': st7789.WHITE,
                'background_color': st7789.BLACK}, 
    'neutral_left': {'eye_l': (25, 60, 45, 70), 
                'eye_r': (100, 60, 45, 70), 
                'mouth': (85, 170, 70, 10), 
                'duration': None, 
                'face_color': st7789.WHITE,
                'background_color': st7789.BLACK}, 
    'neutral_right': {},
    'blink': {'eye_l': (55, 80, 45, 5), 
                'eye_r': (140, 80, 45, 5), 
                'mouth': (85, 170, 70, 10), 
                'duration': 0.015, 
                'face_color': st7789.WHITE,
                'background_color': st7789.BLACK}, 
    'wink': {},
    'angry': {},
    'sad': {},
    'happy': {},
    'suspicious': {},
    'surprise': {},
    'sleeping': {},
    'blush': {}
}

# ----- Rendering loop -----
emotion = 'neutral' # Default set to Neutral

# Fetch emotion params
x_eye_l, y_eye_l, w_eye_l, h_eye_l = EMOTIONS[emotion]['eye_l']
x_eye_r, y_eye_r, w_eye_r, h_eye_r = EMOTIONS[emotion]['eye_r']
x_mouth, y_mouth, w_mouth, h_mouth = EMOTIONS[emotion]['mouth']
duration = EMOTIONS[emotion]['duration']
background_color = EMOTIONS[emotion]['background_color']
face_color = EMOTIONS[emotion]['face_color']

while True: 
    tft.fill(background_color)
    tft.fill_rect(x_eye_l, y_eye_l, w_eye_l, h_eye_l, face_color)    
    tft.fill_rect(x_eye_r, y_eye_r, w_eye_r, h_eye_r, face_color)   
    tft.fill_rect(x_mouth, y_mouth, w_mouth, h_mouth, face_color) 
    time.sleep(40)