from counterdown import CounterDown
from time import sleep
import subprocess, sys, os, threading
import Paths as paths
import RPi.GPIO as GPIO
import Pins as pins

class TX:

    __instance = None

    def __init__(self, master_):

        if TX.__instance is not None:

            raise Exception('This class is a singleton!')
        else:

            self.master = master_
            self.info_logger = self.master.info_logger
            self.counterdown = CounterDown(master_)
            self.sdr_process = None
            self.file_name_temperature = paths.Paths().tx_file
            self.file_name_predefined_data = paths.Paths().tx_file_pre_data
            self.TX_code_file = 'sdr_TX.py'
            self.TX_code_sin = 'sin_TX.py'
            self.pin_led_tx = pins.Pins().pin_led_tx
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin_led_tx, GPIO.OUT)
            GPIO.output(self.pin_led_tx, GPIO.LOW)
    @staticmethod
    def get_instance():

        if TX.__instance is None:
            TX(None)
        return TX.__instance

    def start(self):
        self.info_logger.write_info('TX PROCESS START')
        self.tx_phase_zero()
        self.tx_phase_available()


    def tx_phase_zero(self):
        while not self.master.status_vector['DEP_SUCS'] and not self.master.status_vector['KILL']:
            self.info_logger.write_info('TX: WAIT')
            sleep(self.counterdown.tx_time_checks_deploy)

    def tx_phase_available(self):

        while not self.master.status_vector['KILL']:

            self.master.command_vector['SIN'] = 0

            if self.master.get_command('TX_SLEEP'):
                self.master.command_vector['TX_SLEEP'] = 0
                self.phase_tx_sleep()

            #open led
            self.led_on()

            #start transmition of temp-pre
            threading.Thread(target=self.start_tx, args=(self.TX_code_file,)).start()
            self.master.info_logger.write_info('TX: SDR TRANSMIT')

            #on transmition
            while not self.master.get_command('SIN') and not self.master.get_command('TX_SLEEP') and not self.master.status_vector['KILL']:
                sleep(self.counterdown.tx_check_to_stop_transmition)

            #kill transmition of temp-pre
            self.master.info_logger.write_info('TX: SDR STOP MAIN TRANSMIT')
            self.kill_tx(self.TX_code_file)

            #close led
            self.led_off()

            #SIN mode @TODO be done
            if self.master.get_command('SIN'):
                self.master.command_vector['SIN'] = 0
                self.master.info_logger.write_info('TX: SIN COMMAND')
                # open led
                self.led_on()

                # start transmition of temp-pre
                threading.Thread(target=self.start_tx, args=(self.TX_code_sin,)).start()
                self.master.info_logger.write_info('TX: SDR TRANSMIT SIN')
                sleep(self.counterdown.tx_duration_sin)
                #KILL SIN
                # kill transmition of sin
                self.master.info_logger.write_info('TX: SDR STOP MAIN TRANSMIT')
                self.kill_tx(self.TX_code_sin)

                # close led
                self.led_off()

        # kill sdr process
        self.master.info_logger.write_info('TX: NON-AV')


    def led_on(self):
        self.master.status_vector['AMP_ON'] = 1
        GPIO.output(self.pin_led_tx, GPIO.HIGH)
        self.master.status_vector['TX_ON'] = 1

    def led_off(self):
        self.master.status_vector['AMP_ON'] = 0
        GPIO.output(self.pin_led_tx, GPIO.LOW)
        self.master.status_vector['TX_ON'] = 0

    def phase_tx_sleep(self):
        self.led_off()
        self.master.status_vector['TX_ON'] = 0
        self.info_logger.write_warning('TX: FORCE_TX_CLOSED')
        self.master.command_vector['TX_AWAKE'] = 0

        while not self.master.get_command('TX_AWAKE') and not self.master.status_vector['KILL']:
            sleep(self.counterdown.tx_check_to_stop_transmition)

        self.master.command_vector['TX_SLEEP'] = 0
        self.master.command_vector['TX_AWAKE'] = 0
        self.master.status_vector['TX_ON'] = 1

    def start_tx(self, name):
        os.system('python2 {name}'.format(name=name))

    def kill_tx(self, name):
        temp_filename = 'tmp_pid'
        os.system('ps -ef | grep {name} > {temp_filename}'.format(name=name, temp_filename=temp_filename))
        with open(temp_filename, 'r') as tmp:
            lines = tmp.readlines()
            for line in lines:
                compoments = line.split()
                curr_name = compoments[-1]
                curr_command = compoments[-2]

                if curr_name == name and curr_command == 'python2':
                    pid = compoments[1]
                    os.system('kill -9 {pid}'.format(pid=pid))
                    os.system('rm -f {temp_filename}'.format(temp_filename=temp_filename))
