#!/usr/bin/env python3
from gpiozero import AngularServo, Button
from signal import pause
import time, os

# Servo setup
servo = AngularServo(18, min_angle=0, max_angle=180,
                     min_pulse_width=0.0005, max_pulse_width=0.0025)

# Button setup
button = Button(23, pull_up=False)

def move_door():
    print("Button pressed -> Moving servo")
    servo.angle = 180  # open
    time.sleep(2)
    servo.angle = 90   # close after delay
    time.sleep(2)
    servo.angle = None
    print("Door closed")

# Bind event
button.when_pressed = move_door

print("Waiting for button press...")
pause()
