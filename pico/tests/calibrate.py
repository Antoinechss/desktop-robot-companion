from machine import PWM, Pin
import time

pan = PWM(Pin(14)); pan.freq(50)
tilt = PWM(Pin(15)); tilt.freq(50)

PAN_CENTER, PAN_MIN, PAN_MAX = 115, 50, 155
TILT_CENTER, TILT_MIN, TILT_MAX = 45, 10, 100

def go(servo, angle):
    servo.duty_ns(int(500000 + (angle / 180) * 2000000))

def sweep(name, servo, start, end, step=5, pause=0.6):
    print("---", name, start, "->", end)
    direction = 1 if end > start else -1
    for a in range(start, end + direction, step * direction):
        go(servo, a)
        print(name, a)
        time.sleep(pause)

# Centre
go(pan, PAN_CENTER); go(tilt, TILT_CENTER)
time.sleep(2)

# Tilt: up to the limit, down to the limit, back to centre
sweep("tilt", tilt, TILT_CENTER, TILT_MIN)
sweep("tilt", tilt, TILT_MIN, TILT_MAX)
sweep("tilt", tilt, TILT_MAX, TILT_CENTER)

# Pan: right to the limit, left to the limit, back to centre
sweep("pan", pan, PAN_CENTER, PAN_MIN)
sweep("pan", pan, PAN_MIN, PAN_MAX)
sweep("pan", pan, PAN_MAX, PAN_CENTER)

print("done")