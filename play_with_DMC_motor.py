from Motor import MotorDMC

class Master:

    __instance = None

    def __init__(self):

        self.status_vector = dict()
        self.command_vector = dict()
        self.motor_dmc = MotorDMC()
        Master.__instance = self

    @staticmethod
    def get_instance():

        if Master.__instance is None:
            Master()
        return Master.__instance

    def start(self):

        while True:
            act = input("type ACT or act\n")
            if act == 'ACT' or act == 'act':
                count_steps = input("give steps - ONLY INTEGER\n")
                direction = input("give 0 (anti-clockwise) or 1 (clockwise)\n")
                self.motor_dmc.act(count_steps, direction)


if __name__ == "__main__":

    print("""
        This is a program to test only DMC MOTOR control.
        Use commands:
        [+] ACT
        [+] an integer (e.x 5) # steps for motor - after ACT
        [+] 1 or 0 # for clockwise or anti-clockwise of motor - after ACT n' steps
        [+] KILL #to kill program 
        """)
    Master().start()
