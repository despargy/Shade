from Motor import MotorDMC
import elinkmanager
import threading
import sys

class Master:

    __instance = None

    def __init__(self, ground_ip):

        self.status_vector = dict()
        self.command_vector = dict()
        self.ground_ip = ground_ip
        self.elink = elinkmanager.ELinkManager(self,self.ground_ip)
        self.thread_elink = None
        self.motor_adc = MotorDMC()
        Master.__instance = self

    @staticmethod
    def get_instance():

        if Master.__instance is None:
            Master()
        return Master.__instance

    def init_status_vector(self):
        # Experiment
        self.status_vector['KILL'] = 0

    def init_command_vector(self):
        self.command_vector['ACT'] = 0

    def start(self):

        self.init_experiment()
        while not self.get_command('KILL'):
            if self.get_command('ACT'):
                count_steps = input()
                direction = input()
                try:
                    count_steps = int(count_steps)
                    direction = int(direction)
                    self.motor_adc.act(count_steps, direction)
                except:
                    pass
            self.command_vector['ACT'] = 0
        self.status_vector['KILL'] = 1
        print('end')

    def init_experiment(self):
        self.init_status_vector()
        self.init_command_vector()
        self.init_elink()

    def init_elink(self):
        self.thread_elink = threading.Thread(target=self.elink.start).start()

    def get_command(self, command):
        try:
            return self.command_vector[command]
        except:
            return 0


if __name__ == "__main__":

    __again = True

    if len(sys.argv) != 2:
        print("""
              [+] Run master program with one argument.
              [+] The argument indicates the ground IP
              [+] e.g python play_with_DMC_motor.py 195.168.0.1

              [+] For Testing purposes use 'local' as argument
              [+] to simulate a connection locally
              [+] e.g python play_with_DMC_motor.py local
              """)
    else:
        print("""
            This is a program to test only DMC MOTOR control.
            Use commands:
            [+] ACT
            [+] an integer (e.x 5) # steps for motor - after ACT
            [+] 1 or 0 # for clockwise or anti-clockwise of motor - after ACT n' steps
            [+] KILL #to kill program 
            """)
        ground_ip = sys.argv[1]
        Master(ground_ip).start()
