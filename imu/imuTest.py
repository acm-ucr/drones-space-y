from mpu6050 import mpu6050
from smbus import SMBus
import time

sensor = mpu6050(0x68)

while(True):
    time.sleep(0.5)
    
    gyro = sensor.get_gyro_data()
    accel = sensor.get_accel_data()

    print("Accelrometer: ", accel)
    print("Gyroscope: ", gyro)