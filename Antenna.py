import Paths as paths
from file_read_backwards import FileReadBackwards


class Antenna:


    __instance = None


    #constructor
    def __init__(self):
        """
            position: degrees of antenna's base rotated by motor
            counter_for_overlap: counter to check for overlap
            overlap_thress: maximun degrees that antenna is able to rotate = 360 + overlap
        """
        if Antenna.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            try:
                self.paths = paths.Paths()
                file_name = "{dir}/{filename}".format(dir="Logs", filename='adcs.log')
                with FileReadBackwards(file_name, encoding="utf-8") as log_file:
                    for line in log_file:
                        position = line.decode().split(',')[0]
                        counter = line.decode().split(',')[1]
                        theta_antenna_pointing = line.split(',')[2]
                        theta = line.split(',')[3]
                        break
            except:
                #@TODO change the default init position and counter
                position = 0
                counter = 0
                theta_antenna_pointing = 0
                theta = 0
            self.position = position
            self.counter_for_overlap = counter
            self.theta = theta
            self.theta_antenna_pointing = theta_antenna_pointing
            self.overlap_thress = 380
            self.sign_for_counter = +1
            self.angle_plot = 0
            Antenna.__instance = self

    @staticmethod
    def get_instance():
        if Antenna.__instance is None:
             Antenna()
        else:
            return Antenna.__instance

    #function to update if antenna is used or not
    def update_position(self, difference, direction):
        if direction == 1:
            self.sign_for_counter = 1
        else:
            self.sign_for_counter = -1
        if type(difference) in [float, int] and (difference > 0):
            self.position = self.position + self.sign_for_counter*difference
            if self.position < 0:
                self.position = 360 - abs(self.position)
            elif self.position > 360:
                self.position -= 360
            self.counter_for_overlap = self.counter_for_overlap + self.sign_for_counter*difference


    def check_isinoverlap(self, next_plus_angle, sign):
        if type(next_plus_angle) in [float, int] and sign in [-1, +1]:
            if self.counter_for_overlap + sign*next_plus_angle > self.overlap_thress:
                return True
            elif self.counter_for_overlap + sign*next_plus_angle < -self.overlap_thress:
                return True
            else:
                return False
        else:
            print('false in overlap func')




