class Pins():

    def __init__(self):

        self.pin_heaterA = 38  # pin for Heater A
        self.pin_heaterB =  36 # pin for Heater B

        #self.pin_powerA = 36 # @TODO change it in boot/config.txt
        #self.pin_powerB = 36 # @TODO change it in boot/config.txt

        self.ADC_pin_direction = 24  # Direction GPIO Pin OK
        self.ADC_pin_step = 26  # Step GPIO Pin OK

        self.DMC_pin_direction = 32  # Direction GPIO Pin OK
        self.DMC_pin_step = 31  # Step GPIO Pin OK
        self.DMC_pin_enable = 23

        #self.pin_amp = 36 # pin for Amplifier
        #@TODO uncomment pin led tx
        self.pin_led_tx = 40 # pin for Amplifier


