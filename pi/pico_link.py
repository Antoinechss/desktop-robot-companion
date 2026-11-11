from config import SERIAL_LINK, SPEED
import serial

def open_link(): 
    """Opens serial port for communication between the Pi and the Pico"""
    return serial.Serial(SERIAL_LINK, SPEED, timeout=1)

def send(ser, command: str): 
    """sends a command to the serial port"""
    data = (command + "\n").encode()
    ser.write(data)

