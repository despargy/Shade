from counterdown import CounterDown
from time import sleep
import sdr_simulation
import subprocess, sys, os, inspect, signal



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
        try:
            self.sdr_process = subprocess.call([sys.executable, os.path.join(get_script_dir(), 'sdr_simulation.py')])
            cmd = 'python3 sdr_simulation.py'
            self.sdr_process = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
            #subprocess.call("/home/despina/Dropbox/BEAM/Software/Shade/sdr_simulation.py", shell=True)
        #@TODO FILE RUN
        except:
            self.info_logger.write_error('SDR PROCESS COULD BE CALLED')
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

            self.master.command_vector['PRE'] = 0
            while self.master.get_command('TX_SLEEP'):
                self.close_amplifier()
                self.master.status_vector['TX_ON'] = 0
                # self.master.status_vector['AMP_ON'] = 0 ???
                self.info_logger.write_warning('FORCE_TX_CLOSED')
                print('FORCE_TX_CLOSED')
                if self.master.get_command('TX_AWAKE'):
                    self.master.command_vector['TX_SLEEP'] = 0
                    self.master.command_vector['TX_AWAKE'] = 0
                    self.master.status_vector['TX_ON'] = 1

            self.open_amplifier()
            self.transmite(self.file_name_temperature)

            while not self.master.get_command('PRE') and not self.master.get_command('TX_SLEEP'):
                print('wait for pre')
                sleep(self.counterdown.tx_check_to_stop)  # wait trans

            #kill sdr process
            #self.sdr_process.kill()
            os.killpg(os.getpgid(self.sdr_process.pid), signal.SIGTERM)  # Send the signal to all the process groups

            if self.master.get_command('PRE'):
                self.transmite(self.file_name_predefined_data)
                #wait to send data
                # kill sdr process
                self.sdr_process.kill()

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)