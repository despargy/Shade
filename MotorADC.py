from time import sleep
import RPi.GPIO as GPIO

class MotorADC():

    __instance = None


    def __init__(self):
        if MotorADC.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.step_size = 1.8
            self.direction = 0
            self.step_counter = 0
            self.pin_direction = 20 # Direction GPIO Pin
            self.pin_step = 21  # Step GPIO Pin
            self.pin_sleep = 22
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin_direction, GPIO.OUT)
            GPIO.setup(self.pin_step, GPIO.OUT)
            GPIO.setup(self.pin_sleep, GPIO.OUT)
            GPIO.output(self.pin_sleep, GPIO.HIGH)
            print("motorADC created ")
            MotorADC.__instance = self

    def get_instance(self):
        if MotorADC.__instance == None:
            MotorADC()
        return MotorADC.__instance


    def act(self, count_steps, direction):
        self.direction = direction
        GPIO.output(self.pin_direction, self.direction)
        delay = .0208

        for x in range(count_steps):
            print("\t",x)
            GPIO.output(self.pin_step, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.pin_step, GPIO.LOW)
            sleep(delay)


    def test(self):
        self.act(10, 1)
        print("18 degrees clockwise: DONE")
        self.act(10, 1)
        print("18 degrees anti-clockwise: DONE")
        self.act(100,1)
        print("180 degrees clockwise: DONE")
        self.act(100,0)
        print("180 degrees anti-clockwise: DONE")
        self.act(200,0)
        print("360 degrees anti-clockwise: DONE")
        self.act(200,1)
        print("360 degrees clockwise: DONE")


if __name__ == '__main__':
    motor = MotorADC()
    motor.test()