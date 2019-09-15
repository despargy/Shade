from time import sleep
import RPi.GPIO as GPIO
import Pins as pins

class Motor:

    def __init__(self):
        self.direction = 0
        self.step_counter = 0
        self.pin_direction = None  # Direction GPIO Pin
        self.pin_step = None  # Step GPIO Pin

    def go_to_zero_based_on_direction(self, direction):
        pass

    def go_to_zero_based_on_current_position(self, current_possition):
        pass

class MotorADC(Motor):

    __instance = None

    def __init__(self):

        if MotorADC.__instance is not None:
            raise Exception("This class is a singleton!") #logger
        else:
            super(MotorADC, self).__init__()
            self.step_size = 0.9
            self.pin_direction = pins.Pins().ADC_pin_direction  # Direction GPIO Pin OK
            self.pin_step = pins.Pins().ADC_pin_step # Step GPIO Pin OK
            self.period = .1
            self.p_high = 0.05
            self.p_low = 0.95
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin_direction, GPIO.OUT)
            GPIO.setup(self.pin_step, GPIO.OUT)
            MotorADC.__instance = self

    @staticmethod
    def get_instance():
        if MotorADC.__instance is None:
            MotorADC()
        return MotorADC.__instance

    def act(self, count_steps, direction):
        if type(count_steps) is int and not count_steps<0 and direction in [0,1]:
            self.direction = direction
            GPIO.output(self.pin_direction, self.direction)
            for x in range(count_steps):
                GPIO.output(self.pin_step, GPIO.HIGH)
                sleep(self.period*self.p_high)
                GPIO.output(self.pin_step, GPIO.LOW)
                sleep(self.period*self.p_low)
        else:
            pass

class MotorDMC(Motor):

    __instance = None

    def __init__(self):

        if MotorDMC.__instance is not None:
            raise Exception("This class is a singleton!")  # logger
        else:
            super(MotorDMC, self).__init__()
            self.step_size = 1.8
            self.pin_direction = pins.Pins().DMC_pin_direction  # Direction GPIO Pin OK
            self.pin_step = pins.Pins().DMC_pin_step  # Step GPIO Pin OK
            self.period = .15
            self.p_high = 0.05
            self.p_low = 0.95
            self.deploy_direction = 0
            self.retrieve_direction = 1
            #@TODO deploy n' small steps
            self.deploy_steps = 360
            self.small_steps = 10
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin_direction, GPIO.OUT)
            GPIO.setup(self.pin_step, GPIO.OUT)
            MotorDMC.__instance = self

    @staticmethod
    def get_instance():
        if MotorDMC.__instance is None:
            MotorDMC()
        return MotorDMC.__instance

    def motor_deploy(self):
        GPIO.output(self.pin_direction, self.deploy_direction)
        for x in range(self.deploy_steps):
            GPIO.output(self.pin_step, GPIO.HIGH)
            sleep(self.period*self.p_high)
            GPIO.output(self.pin_step, GPIO.LOW)
            sleep(self.period*self.p_low)
        print('DMC MOTOR DEPLOYED')

    def motor_retrieve(self):
        GPIO.output(self.pin_direction, self.retrieve_direction)
        for x in range(self.deploy_steps):
            GPIO.output(self.pin_step, GPIO.HIGH)
            sleep(self.period*self.p_high)
            GPIO.output(self.pin_step, GPIO.LOW)
            sleep(self.period*self.p_low)
        print('DMC MOTOR RETRIEVED')

    def motor_push(self):

        GPIO.output(self.pin_direction, self.deploy_direction)
        for x in range(self.small_steps):
            GPIO.output(self.pin_step, GPIO.HIGH)
            sleep(self.period*self.p_high)
            GPIO.output(self.pin_step, GPIO.LOW)
            sleep(self.period*self.p_low)
        print('DMC MOTOR PUSH')

    def motor_pull(self):
        GPIO.output(self.pin_direction, self.retrieve_direction)
        for x in range(self.small_steps):
            GPIO.output(self.pin_step, GPIO.HIGH)
            sleep(self.period*self.p_high)
            GPIO.output(self.pin_step, GPIO.LOW)
            sleep(self.period*self.p_low)
            print('DMC MOTOR PULL')

    def act(self, count_steps, direction):
        if type(count_steps) is int and not count_steps<0 and direction in [0,1]:
            self.direction = direction
            GPIO.output(self.pin_direction, self.direction)
            for x in range(count_steps):
                GPIO.output(self.pin_step, GPIO.HIGH)
                sleep(self.period*self.p_high)
                GPIO.output(self.pin_step, GPIO.LOW)
                sleep(self.period*self.p_low)
            print('act')
        else:
            pass
            print('error in action')

