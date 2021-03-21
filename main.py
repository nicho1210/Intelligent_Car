import RPi.GPIO as gpio
import time
import jd01_control as control

#General parameter  initial
speed = 0.3
start = False
key_occur = False
output_time = 0
output_counter = 0
calculate_time = 100
calculate_counter = 0
setup_speed = [0,0]

#Collide parameter initial
collide_distance = 100
collide_turn_rate = 0.8
collide_speed = [0,0]

#Duck parameter initial
duck_distance = 200
duck_speed = [speed,speed]

#System initial
control.control_initial()
control.motor_stop()
detect_value = control.sonar_detect_all()

#Setup switcher and led GPIO pin 
sw_io = 17
led_io = 2
gpio.setup(sw_io,gpio.IN)
gpio.setup(led_io,gpio.OUT)
gpio.output(led_io,gpio.LOW)

#Collide Process
def collide(value):
    global speed
    global collide_turn_rate

    if (value[0] < value[2]):
        collide_speed[0] = speed*collide_turn_rate
        collide_speed[1] = -speed*collide_turn_rate
    else:
        collide_speed[0] = -speed*collide_turn_rate
        collide_speed[1] = speed*collide_turn_rate

    return collide_speed

#Duck process
def  duck(value):
    global speed
    global duck_speed_down

    if (value[0] < value[2]):
        duck_speed[0] = speed
        duck_speed[1] = speed*(1 - (value[2] - value[0])/control.get_echo_time())
    else:
        duck_speed[0] = speed*(1 - (value[0] - value[2])/control.get_echo_time())
        duck_speed[1] = speed

    return duck_speed

def calculate(calculate_value):
    global speed
    global collide_distance
    global duck_distance
    
    #print(calculate_value)
        
    if (calculate_value[0] < collide_distance or calculate_value[2] < collide_distance) and (calculate_value[1] < collide_distance):
        calculate_speed = collide(calculate_value)
    elif calculate_value[1] < collide_distance:
        calculate_speed = collide(calculate_value)
    elif calculate_value[0] < duck_distance or calculate_value[2] < duck_distance:
        calculate_speed = duck(calculate_value)
    else:
        calculate_speed = [speed,speed]

    return calculate_speed

#Major loop
while True:
    #Start or stop process
    sw_input = gpio.input(sw_io)
    if key_occur == False and sw_input == 1:
        key_occur = True
    elif key_occur == True and sw_input == 0:
        key_occur = False
        if start:
            start = False
            gpio.output(led_io,gpio.LOW)
            control.motor_stop()
        else:
            start = True
            gpio.output(led_io,gpio.HIGH)

    #Sonar detect and motor control
    detect_value = control.loop()

    #Calculate direction process
    calculate_counter += 1
    if (calculate_counter >= calculate_time):
        setup_speed = calculate(detect_value)
        calculate_counter = 0

        #Motor control
        if start:
            control.set_speed(setup_speed)

    #Output information
    if (output_time != 0):
        output_counter += 1
        if (output_counter >= output_time):
            print(start," -- ",detect_value[0],",",detect_value[1],",",detect_value[2]," ---- ",setup_speed[0],",",setup_speed[1])
            output_counter = 0

