Components:
- breadboard
- raspi 5
- jumper cables
- servo motor

  
GPIO
- GND (brown wire)
- GPIO 18 (orange wire)
- 5V (red wire)


Commands to get the code to run on boot
chmod +x /home/pi/button_servo.py

(create service file)
sudo nano /etc/systemd/system/button_servo.service

(configuration)
[Unit]
Description=Button Servo Controller
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/button_servo.py
Restart=on-failure
User=pi

[Install]
WantedBy=multi-user.target

(enable and start)
sudo chmod 644 /etc/systemd/system/button_servo.service
sudo systemctl daemon-reload
sudo systemctl enable button_servo.service
sudo systemctl start button_servo.service
