class Antenna:
    #constructor
    def __init__(self, name, step):
        """ name: name of antenna
            step: step size of motor 1.8
            bdeployed: antenna is deployed
            state: is used or not
            set_by_motor_in: degrees of antenna's base rotated by motor
            degrees_counter_for_overlap: counter to check for overlap
            overlap_thress: maximun degrees that antenna is able to rotate = 360 + overlap
        """
        self.name = name
        self.step_size = step
        self.bdeployed = False
        self.state = True
        self.set_by_motor_in = 0
        self.counter_for_overlap = 0
        self.overlap_thress = 380

    #function to update if antenna is used or not
    def update_state(self, state):
        self.state = state
        print("state updated")
        print(self.state)

    #function to update the degrees of antenna's base rotated by motor
    def update_set_by_motor(self, a):
        self.set_by_motor_in = a

    def check_isinoverlap(self, next_plus_angle, sign):
        if self.counter_for_overlap + sign*next_plus_angle > self.overlap_thress:
            return True
        else:
            return False

    def update_counter_for_overlap(self, next_plus_angle, sign):
        self.counter_for_overlap += sign*next_plus_angle

    #function for testing the Antenna class
    def test(self):
        self.bdeployed = True
        print(self.bdeployed)
        self.update_set_by_motor(210)
        print(self.set_by_motor_in)

