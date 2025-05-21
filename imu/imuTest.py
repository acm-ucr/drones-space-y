from mpu6050 import mpu6050
from smbus import SMBus
import time

sensor = mpu6050(0x68)
print("Sensor found!")

normal = []

while(True):
    time.sleep(1)
    
    gyro = sensor.get_gyro_data()
    if not normal:
        normal.append(gyro['y'])
    accel = sensor.get_accel_data()

    if (abs(gyro['y'] - normal[0]) > 10):
        normal[0] = gyro['y']
        print("Leaning Forward...")
    else:
        print("Normal/leaning backwards")

    # print("Accelrometer: ", accel)
    # print("Gyroscope: ", gyro)
    # print()
    # print()
