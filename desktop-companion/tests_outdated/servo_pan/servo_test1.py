# Testing the hardware and pluggings with a first angle direct order

from machine import Pin, PWM
servo = PWM(Pin(14))
servo.freq(50)
servo.duty_ns(2_000_000)   

