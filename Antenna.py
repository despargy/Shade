class Antenna():


    __instance = None


    #constructor
    def __init__(self):
        """
            state: is used or not
            position: degrees of antenna's base rotated by motor
            degrees_counter_for_overlap: counter to check for overlap
            overlap_thress: maximun degrees that antenna is able to rotate = 360 + overlap
        """
        if Antenna.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.position = 0
            self.overlap_thress = 380
            self.counter_for_overlap = self.position
            self.sign_for_counter_overlap = +1
            Antenna.__instance = self

    def get_instace(self):
        if Antenna.__instance == None:
             Antenna()
        else:
            return Antenna.__instance

    #function to update if antenna is used or not
    def update_position(self, difference, sign):
        if type(difference) in [float, int] and (difference > 0) and sign in [-1,+1]:
            self.position = self.position + sign*difference
            if self.position < 0:
                self.position = 360 - abs(self.position)
            elif self.position > 360:
                self.position -= 360
            self.counter_for_overlap = self.counter_for_overlap + self.sign_for_counter_overlap*difference


    def check_isinoverlap(self, next_plus_angle, sign):
        if type(next_plus_angle) in [float, int] and sign in [-1, +1]:
            if self.counter_for_overlap + sign*next_plus_angle > self.overlap_thress:
                return True
            elif self.counter_for_overlap + sign*next_plus_angle < -(self.overlap_thress - 360):
                return True
            else:
                return False
        else:
            print("Wrong type of data  for overlap check")



