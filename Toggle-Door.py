#!/usr/bin/env python3
from gpiozero import AngularServo, Button
from signal import pause
import time

# Setup for GPIO pins
servo = AngularServo(
    18,                    # Servo signal pin
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025
)
button = Button(23, pull_up=False)  # Button connected to GPIO 23 and GND

# Track the door state
door_open = False

def toggle_door():
    global door_open
    if not door_open:
        print("Opening door...")
        servo.angle = 180
        time.sleep(1)
        servo.angle = None
        door_open = True
        print("Door opened")
    else:
        print("Closing door...")
        servo.angle = 90
        time.sleep(1)
        servo.angle = None
        door_open = False
        print("Door closed")

# Run toggle_door every time the button is pressed
button.when_pressed = toggle_door

print("Ready. Press the button to toggle door.")
pause()  # Keeps the script running and responsive
