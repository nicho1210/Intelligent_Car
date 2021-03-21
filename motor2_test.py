import RPi.GPIO as gpio
import time

#Initial motor parameter
motor_driver_time = 1000
motor_left_io = [12,25]
motor_right_io = [13,7]

#Initial motor speed  -1.0 (Reverse) ~ 1.0 (Forward)
motor_speed_left = 0.2
motor_speed_right = 0.2

#Initial switcher parameter
start = False
key_occur = False

# Install GPIO
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#Setup motor IO
for amount in range(0,2):
    gpio.setup(motor_left_io[amount],gpio.OUT)
    gpio.setup(motor_right_io[amount],gpio.OUT)

gpio.output(motor_left_io[0],gpio.LOW)
gpio.output(motor_left_io[1],gpio.LOW)

gpio.output(motor_right_io[0],gpio.LOW)
gpio.output(motor_right_io[1],gpio.LOW)

#Setup switcher and led IO
sw_io = 17
led_io = 2
gpio.setup(sw_io,gpio.IN)
gpio.setup(led_io,gpio.OUT)
gpio.output(led_io,gpio.LOW)

#Sonar detect loop
while(1):
    #Start or stop process
    sw_input = gpio.input(sw_io)
    if key_occur == False and sw_input == 1:
        key_occur = True
    elif key_occur == True and sw_input == 0:
        key_occur = False
        if start:
            start = False
            gpio.output(led_io,gpio.LOW)
        else:
            start = True
            gpio.output(led_io,gpio.HIGH)

    if (start):
        motor_left_speed = motor_speed_left
        motor_right_speed = motor_speed_right
    else:
        motor_left_speed = 0
        motor_right_speed = 0

    #Setup left motor counter and dirrection
    if (motor_left_speed >= 0):
        left_high_single = motor_driver_time*motor_left_speed
        left_motor_dir = 0
    else:
        left_high_single = motor_driver_time*-motor_left_speed
        left_motor_dir = 1

    #Setup right motor counter and dirrection
    if (motor_right_speed >= 0):
        right_high_single = motor_driver_time*motor_right_speed
        right_motor_dir = 0
    else:
        right_high_single = motor_driver_time*-motor_right_speed
        right_motor_dir = 1

    #motor control loop
    for i in range(0,motor_driver_time):
        #Setup left motor control output
        if (i < left_high_single):        
            gpio.output(motor_left_io[left_motor_dir],gpio.HIGH)
        else:
            gpio.output(motor_left_io[left_motor_dir],gpio.LOW)

        #Setup right motor control output
        if (i < right_high_single):        
            gpio.output(motor_right_io[right_motor_dir],gpio.HIGH)
        else:
            gpio.output(motor_right_io[right_motor_dir],gpio.LOW)

gpio.cleanup()
