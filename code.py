# LunarX Bot: PCB Tester
# Yu Hin Hau
# Feb 28, 2024

import board
import digitalio
import time
import pwmio
from adafruit_motor import motor
from adafruit_motor import servo

# LED
LED = digitalio.DigitalInOut(board.IO15)
LED.direction = digitalio.Direction.OUTPUT

# Right Motor
pwmA1 = pwmio.PWMOut(board.IO39)
pwmA2 = pwmio.PWMOut(board.IO37)
motorA = motor.DCMotor(pwmA1, pwmA2)
motorA.throttle = 1

# Left Motor
pwmB1 = pwmio.PWMOut(board.IO35)
pwmB2 = pwmio.PWMOut(board.IO33)
motorB = motor.DCMotor(pwmB1, pwmB2)
motorB.throttle = 1

# Direction
direction = 1

# Claw
pwmClaw = pwmio.PWMOut(board.IO40, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
clawServo = servo.Servo(pwmClaw)
state = 1

# Sensor Test
EN_L = digitalio.DigitalInOut(board.IO5)
EN_L.direction = digitalio.Direction.INPUT

EN_R = digitalio.DigitalInOut(board.IO3)
EN_R.direction = digitalio.Direction.INPUT

IRT_L = digitalio.DigitalInOut(board.IO2)
IRT_L.direction = digitalio.Direction.INPUT

IRT_R = digitalio.DigitalInOut(board.IO1)
IRT_R.direction = digitalio.Direction.INPUT

IR_L = digitalio.DigitalInOut(board.IO11)
IR_L.direction = digitalio.Direction.INPUT

IR_F = digitalio.DigitalInOut(board.IO9)
IR_F.direction = digitalio.Direction.INPUT

IR_R = digitalio.DigitalInOut(board.IO7)
IR_R.direction = digitalio.Direction.INPUT

# Timer
t0 = time.time()

while True:
    LED.value = 1
    time.sleep(0.2)
    LED.value = 0
    time.sleep(0.2)

    if (time.time() - t0 > 2):
        direction *= -1
        motorA.throttle = direction
        motorB.throttle = direction
        
        if (state > 0):
            clawServo.angle = 30
        else:
            clawServo.angle = 90
        
        print(clawServo.angle)
        state *= -1
        t0 = time.time()

    print("-------------------")
    print(f"EN: {EN_L.value}\t{EN_R.value}\t")
    print(f"IRT: {IRT_L.value}\t{IRT_R.value}\t")
    print(f"IR: {IR_L.value}\t{IR_F.value}\t{IR_R.value}\t")

