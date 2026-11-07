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

# Emotions library 
# Angy 
# Sad 
# Happy 
# Suspicious 
# Love 

# EMOTIONS = 


while True: 
    # Blinks every 5 secs 
    tft.fill(st7789.BLACK)
    tft.fill_rect(55, 60, 45, 70, st7789.WHITE)    
    tft.fill_rect(140, 60, 45, 70, st7789.WHITE)   
    tft.fill_rect(85, 170, 70, 10, st7789.WHITE) 
    time.sleep(20)
    tft.fill(st7789.BLACK)
    tft.fill_rect(55, 80, 45, 5, st7789.WHITE)    
    tft.fill_rect(140, 80, 45, 5, st7789.WHITE)   
    tft.fill_rect(85, 170, 70, 10, st7789.WHITE) 
    time.sleep(0.02)