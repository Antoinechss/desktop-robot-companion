from machine import Pin
import time

led = Pin(25, Pin.OUT)

while True:          # un microcontrôleur ne s'arrête jamais : boucle infinie
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1) 