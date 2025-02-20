


import pigpio
import time
import subprocess

# gpio pin connected to the esc signal wire

ESC_PIN = 15

# initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon. Exiting.")
    exit()

command = "sudo pigs s 15 2000"
process = subprocess.run(command, shell=True. caputre_output=True,text=True)
command = "sudo pigs s 15 2000"
process = subprocess.run(command, shell=True. caputre_output=True,text=True)


# send minimum throttle signal to the ESC to initialize
pi.set_servo_pulsewidth(ESC_PIN, 1000)  # 1000µs is usually the ESC idle
time.sleep(2)

print("Motor starting...")

# gradually increase throttle
for pulsewidth in range(1000, 2000, 100):
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