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
```
[Unit]
Description=Button Servo Controller
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/button_servo.py
Restart=on-failure
User=pi

[Install]
WantedBy=multi-user.target
```

(enable and start)
```
sudo chmod 644 /etc/systemd/system/button_servo.service
sudo systemctl daemon-reload
sudo systemctl enable button_servo.service
```
sudo systemctl start button_servo.service



---

1. Create Your Python Script
Make sure your button code is saved, for example as /home/pi/button.py, and is executable:

bash
chmod +x /home/pi/button.py
2. Create a Systemd Service File
Open the systemd directory in nano:

bash
sudo nano /etc/systemd/system/button.service
Paste the following (change the script path if needed):

text
[Unit]
Description=Run Button Script on Boot
After=multi-user.target

[Service]
Type=idle
User=pi
ExecStart=/usr/bin/python3 /home/pi/button.py
Restart=always

[Install]
WantedBy=multi-user.target
Save the file with Ctrl+O, press Enter, then Ctrl+X to exit.

3. Enable the Service
Reload the service manager:

bash
sudo systemctl daemon-reload
Enable the service to start on boot:

bash
sudo systemctl enable button.service
(Optional) Start the service now to test:

bash
sudo systemctl start button.service
4. Check Service Status/Logs
To see if your service is running or get error logs:

bash
sudo systemctl status button.service
sudo journalctl -u button.service

