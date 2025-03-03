
import pigpio
import time
import subprocess

# set pin numbers for each motor
motors = {
    "Motor1": 15,
    "Motor2": 0,
    "Motor3": 0,
    "Motor4": 0,
}

# set min range and max range
minRange = 1000
maxRange = 2000

# initialize pigpio & terminal commands?
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon. Exiting.")
    exit()

command = "sudo pigs s 15 1000"
process = subprocess.run(command, shell=True, caputre_output=True,text=True)
command = "sudo pigs s 15 2000"
process = subprocess.run(command, shell=True, caputre_output=True,text=True)

    # gradually increase throttle
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