import RPi.GPIO as gpio
import time

#Initial sonar parameter
sonar_trig_time = 100
sonar_echo_time = 2000
sonar_amount = 3
sonar_trig_io = [5,19,20]
sonar_echo_io = [6,26,21]

#Exchange rate to mm
sonar_exchange_rate = 1.12

# Install GPIO
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#Setup sonar IO
for amount in range(0,sonar_amount):
    gpio.setup(sonar_trig_io[amount],gpio.OUT)
    gpio.output(sonar_trig_io[amount],gpio.LOW)
    gpio.setup(sonar_echo_io[amount],gpio.IN)

#Sonar detect Loop
while(1):
    output_string = ""
    
    for amount in range(0,sonar_amount):
        for i in range(0,sonar_trig_time):
            gpio.output(sonar_trig_io[amount],gpio.HIGH)

        gpio.output(sonar_trig_io[amount],gpio.LOW)

        high_single = 0
        for i in range(0,sonar_echo_time):
            if(gpio.input(sonar_echo_io[amount])):
                high_single+=1

        output_string += str((int)(high_single*sonar_exchange_rate)) + ","

    print(output_string)
    time.sleep(1)

gpio.cleanup()
