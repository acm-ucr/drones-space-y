class PIDController:
    '''
    Kp, Ki, Kd: Simulation Parameters (For tuning)
    setpoint: Desired value
    dt: change in time
    '''

    def __init__(self, Kp, Ki, Kd, setpoint, dt):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.dt = dt
        self.integral = 0
        self.previous_error = 0

    def update(self, current_value):
        error = self.setpoint - current_value
        self.integral += error * self.dt
        # Avoid division by zero if dt is very small or zero
        if self.dt > 1e-9:
            derivative = (error - self.previous_error) / self.dt
        else:
            derivative = 0.0
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.previous_error = error
        return output

    def reset(self):
        self.integral = 0
        self.previous_error = 0
