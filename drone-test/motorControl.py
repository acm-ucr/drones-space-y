# Different functions to control motors

import pigpio
import time
import subprocess
import threading

# set pin numbers for each motor
class motor:
    pin = 0
    speed = 1000
    running = False

    def __init__(self, esc_pin):
        esc_pin = esc_pin

motors = [ motor(15),
    motor(0),
    motor(0),
    motor(0) ]

# set min range and max range
minRange = 1000
maxRange = 2000

# initialize pigpio & terminal commands?
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon. Exiting.")
    exit()

command = f"sudo pigs s 15 {minRange}"
process = subprocess.run(command, shell=True, caputre_output=True,text=True)
command = f"sudo pigs s 15 {maxRange}"
process = subprocess.run(command, shell=True, caputre_output=True,text=True)

# increase speed of motor
def increaseSpeed(motor:motor, inc:int):
    motor.speed += inc
    pi.set_servo_pulsewidth(motor.pin, motor.speed)
    print(f"Increasing speed to: {motor.speed}µs")

# decrease speed of motor
def decreaseSpeed(motor:motor, dec:int):
    motor.speed -= dec
    pi.set_servo_pulsewidth(motor.pin, motor.speed)

# sets a speed for all motors
def setSpeed(initialSpeed:int):
    for motor in motors:
        motor.speed = initialSpeed
    
def startMotors():
    #Starts and applies maintain speed to all motors
    for motor in motors:
        threading.Thread(target=motor.maintain_speed, daemon=True).start()

    print(f"starting motors at speed{motor.speed}")

def stopMotors():
    for motor in motors:
        motor.running = False
        pi.set_servo_pulsewidth(motor.pin, 0)
    print('stopped all motors')

def displayInfo():
    for i, motor in enumerate(motors):
        print(motor)

def motorTest(ESC_PIN):
    # send minimum throttle signal to the ESC to initialize
    pi.set_servo_pulsewidth(ESC_PIN, 1000)  # 1000µs is usually the ESC idle
    time.sleep(2)

    print("Motor starting...")

    for pulsewidth in range(minRange, maxRange, 100):
        pi.set_servo_pulsewidth(ESC_PIN, pulsewidth)
        print(f"Pulsewidth: {pulsewidth}µs")
        time.sleep(1)

    # stop motor
    pi.set_servo_pulsewidth(ESC_PIN, 1000)
    time.sleep(1)

    # shut down pigpio
    pi.set_servo_pulsewidth(ESC_PIN, 0)
    pi.stop()
    print("Motor test complete.")


for motor in motors:
    print(motor, "test is starting")
    motorTest(motors[motor])

startMotors()
