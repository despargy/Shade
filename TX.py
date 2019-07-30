from counterdown import CounterDown
from time import sleep


class TX:

    __instance = None

    def __init__(self, master_):

        if TX.__instance is not None:

            raise Exception('This class is a singleton!')
        else:

            self.master = master_
            self.info_logger = self.master.info_logger
            self.counterdown = CounterDown(master_)
            self.file_name_temperature = 'tx_temperature_file.txt'
            self.file_name_predefined_data = 'tx_predefined_data.txt'

    @staticmethod
    def get_instance():

        if TX.__instance is None:
            TX(None)
        return TX.__instance

    def start(self):
        self.info_logger.write_info('TX PROCESS START')
        self.tx_phase_zero()
        self.tx_until_kill()


    def transmite(self, file):
        self.info_logger.write_info('TX TRANSMITE'.format(file))
        print('TX TRANSMITE'.format(file))
        #@TODO FILE RUN
        pass

    def open_amplifier(self):
        self.master.status_vector['AMP_ON'] = 1
        pass

    def close_amplifier(self):
        self.master.status_vector['AMP_ON'] = 0
        pass

    def tx_phase_zero(self):
        while not self.master.status_vector['DEP_SUCS']:
            self.info_logger.write_info('TX WAIT')
            print('TX WAIT DEP SUCS')
            sleep(self.counterdown.tx_time_checks_deploy)

    def tx_until_kill(self):
        while not self.master.status_vector['KILL']:

            while self.master.get_command('TX_SLEEP') and not self.master.get_command('TX_AWAKE'):
                self.close_amplifier()
                self.master.status_vector['TX_ON'] = 0
                # self.master.status_vector['AMP_ON'] = 0 ???
                self.info_logger.write_warning('FORCE_TX_CLOSED')
                print('FORCE_TX_CLOSED')

            self.master.command_vector['TX_SLEEP'] = 0
            self.master.command_vector['TX_AWAKE'] = 0
            self.master.status_vector['TX_ON'] = 1
            self.open_amplifier()
            self.transmite(self.file_name_temperature)

            while not self.master.get_command('PRE'):
                pass
                #wait trans
            #kill process of varvariggos

            self.transmite(self.file_name_predefined_data)
            self.master.command_vector['PRE'] = 0
