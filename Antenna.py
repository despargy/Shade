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
def main():
    antenna_adc = Antenna("antenna_ADC",1.8)
    antenna_adc.bdeployed = True
    print(antenna_adc.bdeployed)
    antenna_adc.update_set_by_motor(210)
    print(antenna_adc.set_by_motor_in)
main()
