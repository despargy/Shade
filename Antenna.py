class Antenna:
    def __init__(self, name, step):
        self.name = name
        self.step_size = step
        self.bdeployed = False
        self.state = True
        self.set_by_motor_in = 0
    def update_state(self, state):
        self.state = state
        print("state updated")
        print(self.state)
        return
    def update_set_by_motor(self, a):
        self.set_by_motor_in = a
    def test(self):
        self.bdeployed = True
        print(self.bdeployed)
        self.update_set_by_motor(210)
        print(self.set_by_motor_in)

