import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import pygame
from time import sleep

pygame.init()

WIDTH = 800
HEIGHT = 500


screen = pygame.display.set_mode([WIDTH, HEIGHT])

timer = pygame.time.Clock()
fps = 60
x_pos = 390
y_pos = 490
speed = 1
y_direction = 0

run = True

#Global Variables
time = 0
integral = 0
e_prev = 0

#We will need to create a PID controllelr for each axis of the drone
#Pitch (Up and Down)
#Yaw (Left and right)
#Roll (Side to side (up down))

# Kp, Ki, Kd are weights for each of the 3 measures
# Setpoint is the desired value
# Measurement is the current value
# Output MV is an arbitrary value(scale to match rotations)
def PID(Kp, Ki, Kd, setpoint, measurement):
    global time, integral, time_prev, e_prev

    # Value of offset - when the error is equal zero
    offset = 320
    
    # PID calculations
    e = setpoint - measurement
        
    P = Kp*e
    integral = integral + Ki*e*(time - time_prev)
    D = Kd*(e - e_prev)/(time - time_prev)

    # calculate manipulated variable - MV 
    MV = offset + P + integral + D
    
    # update stored data for next iteration
    e_prev = e
    time_prev = time
    return MV

#Function for the system
def system(t, temp, Tq):
    epsilon = 1
    tau = 4
    Tf = 300  
    Q = 2
    dTdt = 1/(tau*(1+epsilon)) * (Tf-temp) + Q/(1+epsilon)*(Tq-temp)
    return dTdt


def drawPlayer():
    pygame.draw.rect(screen, "orange", [x_pos, y_pos, 10, 10], 0, 5)

tspan = np.linspace(0,10,50)
Tq = 320
sol = odeint(system,300, tspan, args=(Tq,), tfirst=True)
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.plot(tspan,sol)

# number of steps
n = 250  



time_prev = 0
y0 = 300
deltat = 0.1
y_sol = [y0]
t_sol = [time_prev]  # Tq is chosen as a manipulated variable
Tq = 320  
q_sol = [Tq]
setpoint = 310
integral = 0
for i in range(1, n):
    time = i * deltat
    tspan = np.linspace(time_prev, time, 10)
    #Original Values: 0.6, 0.2, 0.1
    Tq = PID(0.6, 0.6, 0.1, setpoint, y_sol[-1])
    yi = odeint(system,y_sol[-1], tspan, args = (Tq,), tfirst=True)
    t_sol.append(time)
    y_sol.append(yi[-1][0])
    q_sol.append(Tq)
    time_prev = time

# for i in range(len(y_sol)):
#     print(y_sol[i])

plt.plot(t_sol, y_sol)
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.show()


index = 0
max = len(y_sol)

while run:
    timer.tick(fps)
    screen.fill("black")

    drawPlayer()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if index < max:
        previous = y_pos
        y_direction = (310 - y_sol[index])
        y_pos +=  speed * y_direction
        index += 1
            
            
    # for i in range(len(y_sol)):
    #     print("Entered Here! Wating for 5 seconds...")
    #     y_direction = (300 - y_sol[i]) / 2
    #     x_pos = speed * y_direction
    pygame.display.flip()
pygame.quit()
