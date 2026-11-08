"""First test at displaying an image on the OLED screen through the Pico controller"""
from machine import Pin, SPI
import st7789py as st7789

# Clock on GP18, Data on GP19
# baudrate = speed : 31M bits/secs
spi = SPI(0, baudrate=31_250_000, sck=Pin(18), mosi=Pin(19))

# 2. L'écran : le bus + sa taille + les 3 broches de contrôle
tft = st7789.ST7789( # Screen
    spi, 240, 240, # Size 
    reset=Pin(20, Pin.OUT),   # RT control endpoint  
    cs=Pin(17, Pin.OUT),      # TC control endpoint  
    dc=Pin(16, Pin.OUT),      # DC control endpoint  
)

# White eyes and mouth over black frame 
tft.fill(st7789.BLACK)
tft.fill_rect(55, 60, 45, 70, st7789.WHITE)    
tft.fill_rect(140, 60, 45, 70, st7789.WHITE)   
tft.fill_rect(85, 170, 70, 10, st7789.WHITE) 