import PIDController as PIDController #PIDController.py

# 

import time
import board
import busio
import signal
import sys
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass
i2c.unlock()

# Setup PCA9685
pca = PCA9685(i2c)
pca.frequency = 50  # Standard for ESCs
time.sleep(1)

# Convert microseconds to 16-bit duty cycle
def pulse_us_to_duty(pulse_us):
    pulse_length = 1000000 / pca.frequency
    return int((pulse_us / pulse_length) * 0xFFFF)

# Emergency stop on Ctrl+C
def emergency_stop(signal_received, frame):
    print("\n[!] Emergency Stop Triggered! Setting all motors to 1000µs...")
    for ch in motor_channels:
        pca.channels[ch].duty_cycle = pulse_us_to_duty(1000)
    time.sleep(1)
    pca.deinit()
    print("PCA9685 deinitialized. Exiting.")
    sys.exit(0)

signal.signal(signal.SIGINT, emergency_stop)

# GET IMU DATA

def get_dt():
    return 0

def get_accel_values(): 
    return 0, 0, 0

def get_rotation_values():
    return 0, 0, 0
    
# CONTROLLER DATA

controller_data = {
    'x': {'Kp': 0, 'Ki': 0, 'Kd': 0, 'setpoint': 0}, 
    'y': {'Kp': 0, 'Ki': 0, 'Kd': 0, 'setpoint': 0}, 
    'z': {'Kp': 0, 'Ki': 0, 'Kd': 0, 'setpoint': 0}, 
    'pitch': {'Kp': 0, 'Ki': 0, 'Kd': 0, 'setpoint': 0},
    'roll': {'Kp': 0, 'Ki': 0, 'Kd': 0, 'setpoint': 0}, 
    'yaw': {'Kp': 0, 'Ki': 0, 'Kd': 0, 'setpoint': 0}, 
}

# INITIALIZE PID CONTROLLERS

controllers = {}

for idx, (key, data) in enumerate(controller_data.items()): # Init controllers
    controllers[key] = PIDController.PIDController(data['Kp'],data['Ki'],data['Kd'],data['setpoint'])

for c in controllers: # Ensure controllers are intiialized
    controllers[c].display()

values = ('x', 'y', 'z', 'pitch', 'roll', 'yaw')

# Motor Functions

def set_motor_speed(channel:int , speed:int):
    motor_speeds[motor_channel]["current"] = max(speed, motor_speeds[motor_channel]["max"]) # Bounds Checking
    pca.channels[channel].duty_cycle = pulse_us_to_duty(motor_speeds[motor_channel]["current"])

def get_motor_speed(channel:int) -> int:
    return motor_speeds[motor_channel]["current"]

# Define motor pins (channels) and their initial speeds and max speeds
motor_channels = [0, 4, 9, 12]  # Assigning motors to channels 0, 5, 9, 13
motor_speeds = {
    0: {"current": 1000, "max": 1300},  # Motor 1: Starts at 1000µs, max at 1400µs
    4: {"current": 1000, "max": 1300},  # Motor 2: Starts at 1000µs, max at 1500µs
    9: {"current": 1000, "max": 1300},  # Motor 3: Starts at 1000µs, max at 1600µs
    12: {"current": 1000, "max": 1300}  # Motor 4: Starts at 1000µs, max at 1700µs
}
try:
    # Initialize the drone
    for motor_channel in motor_channels:
        #pca.channels[motor_channel].duty_cycle = pulse_us_to_duty(motor_speeds[motor_channel]["current"])
        # Above line should be same as bottom line
        set_motor_speed(motor_channel, get_motor_speed(motor_channel))
    time.sleep(5)

    while(True): 
        data = {}
        dt = get_dt()
        data['x'], data['y'], data['z'] = get_accel_values()
        data['pitch'], data['roll'], data['yaw'] = get_rotation_values()

        correction = {}
        for val in values:
            correction[val] = controllers[val].update(data[val], dt)
            
        # Adjust Pitch Correction
            pitch_correction = correction['pitch']
            # Do something to adjust for correction
            speed_correction = 0
            set_motor_speed(0, speed_correction)

        # Adjust Roll Correction
            yaw_correction = correction['pitch']
            # Do something to adjust for correction
            speed_correction = 0
            set_motor_speed(0, speed_correction)

        # Adjust Yaw Correction
            yaw_correction = correction['pitch']
            # Do something to adjust for correction
            speed_correction = 0
            set_motor_speed(0, speed_correction)

finally:
    # Final cleanup if not already stopped
    for motor_channel in motor_channels:
        pca.channels[motor_channel].duty_cycle = pulse_us_to_duty(1000)
    pca.deinit()
    print("PCA9685 deinitialized.")







