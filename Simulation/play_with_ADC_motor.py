from Motor import MotorADC

class Master:

    __instance = None

    def __init__(self):

        self.status_vector = dict()
        self.command_vector = dict()
        self.motor_adc = MotorADC()
        Master.__instance = self

    @staticmethod
    def get_instance():

        if Master.__instance is None:
            Master()
        return Master.__instance

    def start(self):

        while True:
            act = input("type ACT or act\n")
            if act == 'ACT' or act =='act':
                count_steps = input("give steps - ONLY INTEGER\n")
                count_steps = int(count_steps)
                direction = input("give 0 (anti-clockwise) or 1 (clockwise)\n")
                count_steps = int(direction)
                self.motor_adc.act(count_steps, direction)


if __name__ == "__main__":

    print("""
        This is a program to test only ADC MOTOR control.
        Use commands:
        [+] ACT
        [+] an integer (e.x 5) # steps for motor - after ACT
        [+] 1 or 0 # for clockwise or anti-clockwise of motor - after ACT n' steps
        [+] KILL #to kill program 
        """)
    Master().start()
