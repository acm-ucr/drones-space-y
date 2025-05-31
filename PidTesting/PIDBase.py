import PIDController as PIDController

'''
Base code for PID Tuning with controllers for pitch, roll, yaw
Resultant is a dict with corrections for each measure 
'''


# Init PID controllers

def get_dt():
    return 0

def get_accel_values(): 
    return 0, 0, 0

def get_rotation_values():
    return 0, 0, 0

if __name__ == "__main__":
    controller_data = {
        'x': {'Kp': 0, 'Ki': 0, 'Kd': 0, 'setpoint': 0}, 
        'y': {'Kp': 0, 'Ki': 0, 'Kd': 0, 'setpoint': 0}, 
        'z': {'Kp': 0, 'Ki': 0, 'Kd': 0, 'setpoint': 0}, 
        'pitch': {'Kp': 0, 'Ki': 0, 'Kd': 0, 'setpoint': 0},
        'roll': {'Kp': 0, 'Ki': 0, 'Kd': 0, 'setpoint': 0}, 
        'yaw': {'Kp': 0, 'Ki': 0, 'Kd': 0, 'setpoint': 0}, 
    }

    controllers = {}

    for idx, (key, data) in enumerate(controller_data.items()): # Init controllers
        controllers[key] = PIDController.PIDController(data['Kp'],data['Ki'],data['Kd'],data['setpoint'])

    for c in controllers: # Ensure controllers are intiialized
        controllers[c].display()

    values = ('x', 'y', 'z', 'pitch', 'roll', 'yaw')
    
    while (True):
        # Get imu values
        data = {}
        dt = get_dt()
        data['x'], data['y'], data['z'] = get_accel_values()
        data['pitch'], data['roll'], data['yaw'] = get_rotation_values()

        # Calculate correction

        correction = {}
        for val in values:
            correction[val] = controllers[val].update(data[val], dt)
            print(correction[val])
            









