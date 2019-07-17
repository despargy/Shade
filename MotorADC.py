from time import sleep
#import RPi.GPIO as GPIO

class MotorADC():
    def __init__(self):
        self.step_size = 1.8
        self.direction = 0
        self.step_counter = 0
        self.pin_direction = 20 # Direction GPIO Pin
        self.pin_step = 21  # Step GPIO Pin
        self.pin_sleep = 22
        print("motorADC created ")

    def act(self, count_steps, direction):
        self.direction = direction
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_direction, GPIO.OUT)
        GPIO.setup(self.pin_step, GPIO.OUT)
        GPIO.output(self.pin_direction, self.direction)

        delay = .0208

        for x in range(count_steps):
            GPIO.output(self.pin_step, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.pin_step, GPIO.LOW)
            sleep(delay)


