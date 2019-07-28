from time import sleep
from master import Master

class CounterDown:

    def __init__(self):
        self.master = Master.get_instance()
        self.heat_time_check_awake = 3*60
        self.heat_time_runs = 50
        self.heat_time_updates_data = 10
        self.adc_time_checks_deploy = 3*60
        self.adc_wait_manual_ends = 20
        self.adc_time_runs = 10
        self.dmc_time_left_auto_deploy = 5  # 2*60*60 #ex. 2hours
        self.dmc_timeout_cmd = 3  # ex. 1 min
        self.dmc_time_to_sleep = 2  # ex. 2hours
        self.dmc_wait_others_to_killed = 5
        self.master_checks_dep_sucs = 2
        self.master_time_breaks_adc_man = 3*60
        self.master_time_checks_adc_man_cmd = 2
        self.timeout_cmd = 60

    def countdown0(self, t):
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.master.infologger.write_info('{}'.format(timeformat, end='\r'))
            sleep(1)
            t -= 1

    def countdown1(self, t, cmd):
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.master.infologger.write_info('{}'.format(timeformat, end='\r'))
            sleep(1)
            t -= 1
            if self.master.get_command(cmd):
                break

    def countdown2(self, t, cmd1, cmd2):
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.master.infologger.write_info('{}'.format(timeformat, end='\r'))
            sleep(1)
            t -= 1
            # WARNING
            if self.master.get_command(cmd1):
                return 1
            elif self.master.get_command(cmd2):
                return 2

    def countdown3(self, t, cmd1, cmd2, cmd3):
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.master.infologger.write_info('{}'.format(timeformat, end='\r'))
            sleep(1)
            t -= 1
            # WARNING
            if self.master.get_command(cmd1):
                return 1
            elif self.master.get_command(cmd2):
                return 2
            elif self.master.get_command(cmd3):
                return 3