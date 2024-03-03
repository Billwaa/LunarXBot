# LunarX Bot Library
# Yu Hin Hau
# 3/3/2024
# billwaahau@gmail.com


import time
import board
import digitalio
import pwmio

from adafruit_motor import motor
from adafruit_motor import servo


class Bot:

    def __init__(self):

        ## Actuators

        # LED
        self.LED = digitalio.DigitalInOut(board.IO15)
        self.LED.direction = digitalio.Direction.OUTPUT

        # Right Motor
        pwmA1 = pwmio.PWMOut(board.IO39)
        pwmA2 = pwmio.PWMOut(board.IO37)
        self.motorR = motor.DCMotor(pwmA1, pwmA2)
        self.motorR.throttle = 0

        # Left Motor
        pwmB1 = pwmio.PWMOut(board.IO35)
        pwmB2 = pwmio.PWMOut(board.IO33)
        self.motorL = motor.DCMotor(pwmB1, pwmB2)
        self.motorL.throttle = 0

        # Claw
        pwmClaw = pwmio.PWMOut(board.IO40, duty_cycle=2 ** 15, frequency=50)
        self.claw = servo.Servo(pwmClaw)

        ## Sensors
        self.encoderL = digitalio.DigitalInOut(board.IO5)
        self.encoderL.direction = digitalio.Direction.INPUT

        self.encoderR = digitalio.DigitalInOut(board.IO3)
        self.encoderR.direction = digitalio.Direction.INPUT

        self.trackerL = digitalio.DigitalInOut(board.IO2)
        self.trackerL.direction = digitalio.Direction.INPUT

        self.trackerR = digitalio.DigitalInOut(board.IO1)
        self.trackerR.direction = digitalio.Direction.INPUT

        self.obstacleL = digitalio.DigitalInOut(board.IO11)
        self.obstacleL.direction = digitalio.Direction.INPUT

        self.obstacleF = digitalio.DigitalInOut(board.IO9)
        self.obstacleF.direction = digitalio.Direction.INPUT

        self.obstacleR = digitalio.DigitalInOut(board.IO7)
        self.obstacleR.direction = digitalio.Direction.INPUT

        ## Program Parameters

        # Claw Angle
        self.angleClawClosed = 10
        self.angleClawOpened = 60

        # LED Timer
        self.time_LED = time.monotonic()
        self.LEDState = True
        self.LED.value = self.LEDState


    # Blink LED
    def blink(self, duration = 0.2):

        if (time.monotonic() - self.time_LED > duration):
            self.LEDState = not self.LEDState
            self.LED.value = self.LEDState
            self.time_LED = time.monotonic()


    ## Claw Commands

    # Command the Claw to Specific Angle
    def clawAngle(self, angle):
        self.claw.angle = angle

    # Command the Claw to Close
    def clawClose(self, angle = -1):

        if angle == -1:
            self.claw.angle = self.angleClawClosed
        else:
            self.claw.angle = angle

    # Command the Claw to Open
    def clawOpen(self, angle = -1):

        if angle == -1:
            self.claw.angle = self.angleClawClosed
        else:
            self.claw.angle = angle

