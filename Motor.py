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


class MotorADC(Motor):

    __instance = None

    def __init__(self):

        if MotorADC.__instance is not None:
            raise Exception("This class is a singleton!") #logger
        else:
            super(MotorADC, self).__init__()
            self.pin_direction = 13  # Direction GPIO Pin
            self.pin_step = 11  # Step GPIO Pin
            self.pin_sleep = 7  # Sleep Pin
            self.period = .005
            self.p_high = 0.95
            self.p_low = 0.05
#            GPIO.setmode(GPIO.BOARD)
#            GPIO.setup(self.pin_direction, GPIO.OUT)
#            GPIO.setup(self.pin_step, GPIO.OUT)
#            GPIO.setup(self.pin_sleep, GPIO.OUT)
#            GPIO.output(self.pin_sleep, GPIO.HIGH)
            MotorADC.__instance = self

    def get_instance(self):
        if MotorADC.__instance is None:
            MotorADC()
        return MotorADC.__instance

    def act(self, count_steps, direction):
        if type(count_steps) in [int] and not count_steps<0 and direction in [0,1]:
            self.direction = direction
            #GPIO.output(self.pin_direction, self.direction)
            #for x in range(count_steps):
                #GPIO.output(self.pin_step, GPIO.HIGH)
                #sleep(self.period*self.p_high)
                #GPIO.output(self.pin_step, GPIO.LOW)
                #sleep(self.period*self.p_low)
        else:
            pass
            #self.adc.adcslogger.write_warning("Didn't permit action to motorADC")


class MotorDMC(Motor):

    __instance = None

    def __init__(self):

        if MotorDMC.__instance is not None:
            raise Exception("This class is a singleton!")  # logger
        else:
            super(MotorDMC, self).__init__()
            self.pin_direction = 14  # Direction GPIO Pin
            self.pin_step = 12  # Step GPIO Pin
            self.pin_sleep = 8  # Sleep Pin
            self.period = .005
            self.p_high = 0.95
            self.p_low = 0.05
            self.deploy_direction = 1
            self.retrieve_direction = 0
            self.deploy_steps = 300
            self.small_steps = 3
            #GPIO.setmode(GPIO.BOARD)
            #GPIO.setup(self.pin_direction, GPIO.OUT)
            #GPIO.setup(self.pin_step, GPIO.OUT)
            #GPIO.setup(self.pin_sleep, GPIO.OUT)
            #GPIO.output(self.pin_sleep, GPIO.HIGH)
            MotorDMC.__instance = self


    def get_instance(self):
        if MotorDMC.__instance is None:
            MotorDMC()
        return MotorDMC.__instance

    def motor_deploy(self):
        #GPIO.output(self.pin_direction, self.deploy_direction)
        #for x in range(self.deploy_steps):
            #GPIO.output(self.pin_step, GPIO.HIGH)
            #sleep(self.period*self.p_high)
            #GPIO.output(self.pin_step, GPIO.LOW)
            #sleep(self.period*self.p_low)
        print('DEPLOYED')

    def motor_retrieve(self):
        #GPIO.output(self.pin_direction, self.retrieve_direction)
        #for x in range(self.deploy_steps):
            #GPIO.output(self.pin_step, GPIO.HIGH)
            #sleep(self.period*self.p_high)
            #GPIO.output(self.pin_step, GPIO.LOW)
            #sleep(self.period*self.p_low)
        print('RETRIEVED')

    def motor_push(self):

        # GPIO.output(self.pin_direction, self.deploy_direction)
        # for x in range(self.small_steps):
        # GPIO.output(self.pin_step, GPIO.HIGH)
        # sleep(self.period*self.p_high)
        # GPIO.output(self.pin_step, GPIO.LOW)
        # sleep(self.period*self.p_low)
        print('PUSH')

    def motor_pull(self):
        # GPIO.output(self.pin_direction, self.retrieve_direction)
        # for x in range(self.small_steps):
            # GPIO.output(self.pin_step, GPIO.HIGH)
            # sleep(self.period*self.p_high)
            # GPIO.output(self.pin_step, GPIO.LOW)
            # sleep(self.period*self.p_low)
            print('PULL')