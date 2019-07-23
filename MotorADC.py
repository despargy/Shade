from time import sleep
#import RPi.GPIO as GPIO


class Motor:

    def __init__(self):
        self.step_size = 1.8
        self.direction = 0
        self.step_counter = 0
        self.pin_direction = None  # Direction GPIO Pin
        self.pin_step = None  # Step GPIO Pin
        self.pin_sleep = None  # Sleep Pin
        self.period = .005
        self.p_high = 0.95
        self.p_low = 0.05


class MotorADC(Motor):

    __instance = None

    def __init__(self):

        if MotorADC.__instance != None:
            raise Exception("This class is a singleton!") #logger
        else:
            super(MotorADC, self).__init__()
            self.pin_direction = 13  # Direction GPIO Pin
            self.pin_step = 11  # Step GPIO Pin
            self.pin_sleep = 7  # Sleep Pin
#            GPIO.setmode(GPIO.BOARD)
#            GPIO.setup(self.pin_direction, GPIO.OUT)
#            GPIO.setup(self.pin_step, GPIO.OUT)
#            GPIO.setup(self.pin_sleep, GPIO.OUT)
#            GPIO.output(self.pin_sleep, GPIO.HIGH)
            print("motorADC created ") #logger
            MotorADC.__instance = self

    def get_instance(self):
        if MotorADC.__instance == None:
            MotorADC()
        return MotorADC.__instance

    def act(self, count_steps, direction):
        if type(count_steps) in [int] and not count_steps<0 and direction in [0,1]:
            self.direction = direction
#            GPIO.output(self.pin_direction, self.direction)

            #for x in range(count_steps):
                #print("\t",x)
#                GPIO.output(self.pin_step, GPIO.HIGH)
                #sleep(self.period*self.p_high)
#                GPIO.output(self.pin_step, GPIO.LOW)
                #sleep(self.period*self.p_low)
        else:
            print("Didn't permit action to motorADC") #logger

