import sys, select, time
from machine import PWM, Pin

# --- Servo setup 
servo = PWM(Pin(14))
servo.freq(50)

def set_angle(angle):
    angle = max(0, min(180, angle))
    pulse_width_ns = int(500000 + (angle / 180.0) * 2000000)
    servo.duty_ns(pulse_width_ns)

# --- System Read 
poll = select.poll()
poll.register(sys.stdin, select.POLLIN) # Data available for reading

def parse_order(line): 
    """
    Checks line format, parses content and orders 
    Converts cx_scaled position into angle for the servo 
    Fetches emotion for face orders
    """
    line_items = line.strip().split()

    if not line_items: 
        return None

    # --- Pan Servo order 
    if line_items[0] == 'look': 
        try: 
            cx_scaled = float(line_items[1]) # Read the scaled detection x 
            cx_scaled = max(-1, min(1, cx_scaled)) # clamp between [-1, 1]
            servo_angle = 45 * cx_scaled + 90
            return ("look", servo_angle)
        except (ValueError, IndexError): 
            return None
        
    # --- Face order 
    if line_items[0] == 'emo': 
        try: 
            emotion = line_items[1]
            return ("emo", emotion) 
        except IndexError: 
            return None

while True: 
    if poll.poll(0): 
        line = sys.stdin.readline()
        order = parse_order(line)
        if order is not None: 
            cmd, value = order
            if cmd == "look": 
                set_angle(value)
    time.sleep(0.01)


