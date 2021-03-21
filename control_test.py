import RPi.GPIO as gpio
import tt01_control as control

setup_speed = [-1.0,-1.0]

#System initial
control.control_initial()
control.motor_stop()
detect_value = control.sonar_detect_all()


while True:
    detect_value = control.loop()

    control.set_speed(setup_speed)
