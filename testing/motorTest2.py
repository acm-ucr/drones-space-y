import pigpio
import time

# GPIO pins connected to the ESC signal wires
ESC_PINS = [15, 16, 17, 18]  # Assuming motors are connected to GPIO pins 15, 16, 17, and 18

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon. Exiting.")
    exit()

# Send minimum throttle signal to each ESC to initialize (1000µs is usually idle)
for pin in ESC_PINS:
    pi.set_servo_pulsewidth(pin, 1000)
time.sleep(2)

print("Motors starting...")

# Gradually increase throttle for each motor
for pulsewidth in range(1000, 2000, 100):
    for pin in ESC_PINS:
        pi.set_servo_pulsewidth(pin, pulsewidth)
        print(f"Pulsewidth for motor on pin {pin}: {pulsewidth}µs")
    time.sleep(1)

# Stop motors
for pin in ESC_PINS:
    pi.set_servo_pulsewidth(pin, 1000)  # Set back to idle
time.sleep(1)

# Shut down pigpio
for pin in ESC_PINS:
    pi.set_servo_pulsewidth(pin, 0)  # Disable each ESC signal
pi.stop()

print("Motor test complete.")