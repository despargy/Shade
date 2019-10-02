class Pins():

    def __init__(self):

        self.pin_heaterA = 40  # pin for Heater A
        self.pin_heaterB =  38 # pin for Heater B

        #self.pin_powerA = 36 # @TODO change it in boot/config.txt
        #self.pin_powerB = 36 # @TODO change it in boot/config.txt

        self.ADC_pin_direction = 26  # Direction GPIO Pin OK
        self.ADC_pin_step = 32  # Step GPIO Pin OK

        self.DMC_pin_direction = 31  # Direction GPIO Pin OK
        self.DMC_pin_step = 36  # Step GPIO Pin OK

        #self.pin_amp = 36 # pin for Amplifier
        #@TODO uncomment pin led tx
        self.pin_led_tx = 24 # pin for Amplifier


