# Quack Attack
*An alarm system that when motion is detected it messages you on slack and can be controlled remotely through [QuackyOS](https://quackyos.com)*

-----

## Table of Contents
- [Features](#features)
- [Circuit](#circuit)
- [Setup](#setup)
- [How To Run](#how to run)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](https://github.com/donnie58744/Quack-Attack-Pi/blob/main/LICENSE)

### Features

- #### [QuackyOS](https://www.quackyos.com/?openWindow=QuackAttack) Remote Control

  <img src="README_IMGS/QuackAttack-QuackyOS-UI.png" alt="QuackAttack-QuackyOS-UI" style="zoom:67%;" />
  
- #### [Slack Messaging Alerts](#slack messaging alerts)

### Circuit

![Circuit](README_IMGS/Alarm-Sys-CIRCUIT.png)

### Setup

- #### Electronics
	- Raspberry PI
	- PIR Sensor Model #: HC-SR501
	- 4 LEDs
	- 2 Buttons

- #### Py Library Requirements:

	```
	pip install RPi.GPIO
	```

	```
	pip install mfrc522
	```

- #### Raspberry PI

	**(GPIO pins are in board mode)**

	- Green Light Pin: 40
	- Blue Light Pin: 31
	- Yellow Light Pin: 16
	- Red Light Pin: 12
	- Green Button Pin: 35
	- Yellow Button Pin: 37
	- Sensor Data Pin: 11 **You might need to adjust the IR Sensor Sensitivity and Time Delay**

- #### Slack Messaging Alerts

  - Create Slack Webhook, [Heres How](https://api.slack.com/messaging/webhooks)

  - Edit the python file and change the webhookUrl varible to your slack webhook
  
  - Now you can recive alerts from the Alarm on Slack!


### How To Run

```python3 main.py```

### Usage

- #### Buttons
  - Green Button
    - Starts a timer so you have time to leave the area

   - Yellow Button
     - Toggles the alarm on and off

- #### Lights

  - Green Light
    - Timer has started and will cycle through all the lights twice
  - Yellow Light
    - Alarm is On/Off
  - Red Light
    - Motion has been detected

### Contributing

- Donovan Whysong (Afghan Coder) - Head Of Programming
- Erik Whysong - Head Of Engineering

### License

- View [Here](https://github.com/donnie58744/Quack-Attack-Pi/blob/main/LICENSE)
