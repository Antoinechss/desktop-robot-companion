# Testing serial port --> pi --> pico --> servo linkeage
import serial, time

# Connecting to the pi's serial port 
SERIAL_LINK = "/dev/ttyACM0"
SPEED = 115200
ser = serial.Serial(SERIAL_LINK, SPEED, timeout=1)

# Test loop of orders
for _ in range(3): 
    for i in range(-10, 11): 
        ser.write(f"look {i * 0.1:.2f}\n".encode())
        time.sleep(0.1)
    for i in range(10, -11, -1): 
        ser.write(f"look {i * 0.1:.2f}\n".encode())
        time.sleep(0.1)
ser.write(b"look 0\n")
ser.close()

