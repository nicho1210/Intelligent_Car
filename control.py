import RPi.GPIO as gpio
import time

#Initial sonar parameter
sonar_trig_time = 100
sonar_echo_time = 2000
sonar_amount = 3
sonar_trig_io = [5,19,20]
sonar_echo_io = [6,26,21]
sonar_counter = sonar_echo_time
sonar_output = [0,0,0]
sonar_high_single = [0,0,0]

#Exchange rate to mm
sonar_exchange_rate = 4.0

#Initial motor parameter
motor_driver_time = 100
motor_left_io = [12,25]
motor_right_io = [13,7]

#Initial motor speed  -1.0 (Reverse) ~ 1.0  (Forward)
motor_dir = [0,0]
motor_counter = 0
motor_high_single = [0,0]

def control_initial():
    # Install GPIO
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)

    #Setup sonar IO
    for amount in range(0,sonar_amount):
        gpio.setup(sonar_trig_io[amount],gpio.OUT)
        gpio.output(sonar_trig_io[amount],gpio.LOW)
        gpio.setup(sonar_echo_io[amount],gpio.IN)

    #Setup motor IO
    for amount in range(0,2):
        gpio.setup(motor_left_io[amount],gpio.OUT)
        gpio.setup(motor_right_io[amount],gpio.OUT)

    gpio.output(motor_left_io[0],gpio.LOW)
    gpio.output(motor_left_io[1],gpio.LOW)

    gpio.output(motor_right_io[0],gpio.LOW)
    gpio.output(motor_right_io[1],gpio.LOW)

def control_cleanup():
    gpio.cleanup()

def get_echo_time():
    return sonar_echo_time

def sonar_trigger(channel):
    for i in range(0,sonar_trig_time):
        if i == 0:
            gpio.output(sonar_trig_io[channel],gpio.HIGH)
    gpio.output(sonar_trig_io[channel],gpio.LOW)

def sonar_trigger_all():
    for i in range(0,sonar_trig_time):
        if i == 0:
            for amount in range(0,sonar_amount):
                gpio.output(sonar_trig_io[amount],gpio.HIGH)

    for amount in range(0,sonar_amount):
        gpio.output(sonar_trig_io[amount],gpio.LOW)

def sonar_detect_all():
    sonar_trigger_all()

    sonar_high_single = [0,0,0]
    for i in range(0,sonar_echo_time):
        for amount in range(0,sonar_amount):
            if(gpio.input(sonar_echo_io[amount])):
                sonar_high_single[amount] += 1

    for amount in range(0,sonar_amount):
        sonar_output[amount] = (int)(sonar_high_single[amount]*sonar_exchange_rate)

    sonar_counter = sonar_echo_time
    return sonar_output

def set_speed(speed):
    global motor_dir
    global motor_high_single

    #Setup left motor counter and dirrection
    if (speed[0] >= 0):
        motor_high_single[0] = motor_driver_time*speed[0]
        motor_dir[0] = 0
        gpio.output(motor_left_io[1],gpio.LOW)
    else:
        motor_high_single[0] = motor_driver_time*-speed[0]
        motor_dir[0] = 1
        gpio.output(motor_left_io[0],gpio.LOW)

    #Setup right motor counter and dirrection
    if (speed[1] >= 0):
        motor_high_single[1] = motor_driver_time*speed[1]
        motor_dir[1] = 0
        gpio.output(motor_right_io[1],gpio.LOW)
    else:
        motor_high_single[1] = motor_driver_time*-speed[1]
        motor_dir[1] = 1
        gpio.output(motor_right_io[0],gpio.LOW)

def motor_stop():
    global motor_high_single

    gpio.output(motor_left_io[0],gpio.LOW)
    gpio.output(motor_left_io[1],gpio.LOW)
    gpio.output(motor_right_io[0],gpio.LOW)
    gpio.output(motor_right_io[1],gpio.LOW)
    motor_high_single = [0,0]

def loop():
    global sonar_counter
    global sonar_high_single
    global motor_counter
    global motor_left_io
    global motor_right_io
    global motor_dir
    global motor_high_single

    #Sonar trigger if change channel
    if sonar_counter >= sonar_echo_time:
        for amount in range(0,sonar_amount):
            sonar_output[amount] = (int)(sonar_high_single[amount]*sonar_exchange_rate)

        sonar_trigger_all()
        sonar_counter = 0
        sonar_high_single = [0,0,0]

    #Sonar detect
    for amount in range(0,sonar_amount):
        if(gpio.input(sonar_echo_io[amount])):
            sonar_high_single[amount] += 1

    sonar_counter += 1

    #Setup left motor control output
    if (motor_counter < motor_high_single[0]):        
        gpio.output(motor_left_io[motor_dir[0]],gpio.HIGH)
    else:
        gpio.output(motor_left_io[motor_dir[0]],gpio.LOW)

    #Setup right motor control output
    if (motor_counter < motor_high_single[1]):        
        gpio.output(motor_right_io[motor_dir[1]],gpio.HIGH)
    else:
        gpio.output(motor_right_io[motor_dir[1]],gpio.LOW)

    motor_counter += 1
    if (motor_counter >= motor_driver_time):
        motor_counter = 0

    return sonar_output
