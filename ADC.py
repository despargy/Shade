import time
import math
import Antenna as antenna
import MotorADC as motoradc


class ADC:

    __instance = None

    def __init__(self, master_):

        if ADC.__instance != None:
            raise Exception('This class is a singleton!')
        else:
            """
                GS: x- axis y-axis of SHADE Ground Station - static
                gps: x- axis y-axis of Gondola's  current x,y-axis
                compass: data received from compass, degrees btwn North and Gondola 0,0
                antenna_adc: object of antenna instance
                direction: clockwise (1) or anti-clockwise(0) for antenna base rotation
                difference: degrees which are needed for antenna base rotation
            """
            self.GS = [1, 1]
            self.compass = 0
            self.gps = self.GS
            self.direction = 1
            self.difference = 0
            self.motor_adc = motoradc.MotorADC(self)
            self.antenna_adc = antenna.Antenna()
            self.master = master_
            self.valid_data = True
            ADC.__instance = self
            self.master.adcslogger.write_info('CREATED ADC')


    def get_instance(self):

        if ADC.__instance == None:
            ADC(None)
        return ADC.__instance

    def start(self):

        while not self.master.isDeployed:

            self.master.adcslogger.write_info('WAIT FOR DEP')
            time.sleep(2)

        self.run_auto()


    #Auto mode of ADC
    def run_auto(self):

        while True:

            while self.master.isManual:

                self.master.adcslogger.write_info('MANUAL ADC')
                time.sleep(2)

            self.master.adcslogger.write_info('AUTO ADC')
            self.valid_data = True
            self.get_compass_data() #self.datamanager.dictionary['angle_c']
            self.get_gps_data()
                #self.gps[0] = self.get_gps_data() #self.datamanager.dictionary['gps_x]
                #self.gps[1] = self.get_gps_data() #self.datamanager.dictionary['gps_y']
            if self.valid_data:

                self.calc_new_position()
                c_step = self.convert_to_steps(self.difference)
                self.log_last_position_before(c_step)
                self.notify_DMC_motor(c_step, self.direction)
                self.move_ADC_motor(c_step, self.direction)
                self.antenna_adc.update_position(c_step*self.motor_adc.step_size, self.direction)
                self.log_last_position_after()
            else:
                self.master.adcslogger.write_warning('NON action: invalid data')
            s = int(input("give step to set\n"))
            self.set_position(s)

    def get_compass_data(self):

        # x = self.datamanager.dictionary['angle_c']
        x = float(input("give compass\n"))
        if x is None:
            self.master.adcslogger.write_warning('Invalid compass data')
            self.valid_data = False
        else:
            self.compass = x


    def get_gps_data(self):

        # x = self.datamanager.dictionary['gps_x,y']
        x = float(input("give gps x\n"))
        y = float(input("give gps y\n"))
        if x is None or y is None:
            self.master.adcslogger.write_warning('Invalid gps data')
            self.valid_data = False
        else:
            self.gps = [x, y]


    def log_last_position_before(self, c_step):
        self.master.adcslogger.write_info('STEPS\t {}'.format(c_step))
        self.master.adcslogger.write_info('DEGREES {}'.format(self.difference))
        self.master.adcslogger.write_info('ACT FROM: {} TO {}'.format(self.antenna_adc.counter_for_overlap, self.direction))


    def log_last_position_after(self):
        self.master.adcslogger.write_info('DONE: {}'.format(self.antenna_adc.counter_for_overlap))

    def notify_DMC_motor(self,a,b):
        pass

    def move_ADC_motor(self,c,d):
        self.motor_adc.act(c,d)

    def convert_to_steps(self, dif):
        if self.motor_adc.step_size != 0:
            c_step = int(dif / self.motor_adc.step_size)
            return c_step
        else:
            self.master.adcslogger.write_warning('TRY division /0: check step size')
            return 0

    def set_position(self, set_step):
        if 0 <= set_step <= (360/self.motor_adc.step_size):
            self.init_motor_pose()
            direction = 1
            self.motor_adc.act(set_step, direction)
            self.antenna_adc.update_position(set_step*self.motor_adc.step_size, direction)
            self.master.adcslogger.write_info('SET IN {}'.format(self.antenna_adc.position))
        else:
            self.master.adcslogger.write_warning('Invalid SET_STEP')

    def scan(self):

        self.init_motor_pose()
        direction = 1
        self.motor_adc.act(int(360/self.motor_adc.step_size), direction)
        self.antenna_adc.update_position(360, direction)
        self.master.adcslogger.write_info('SCAN: ANTENNA IN {}'.format(self.antenna_adc.position))
        direction = 0
        self.motor_adc.act(int(360/self.motor_adc.step_size), direction)
        self.antenna_adc.update_position(360,direction)
        self.master.adcslogger.write_info('SCAN: ANTENNA IN {}'.format(self.antenna_adc.position))


    def init_motor_pose(self):

        c_steps = self.convert_to_steps(abs(self.antenna_adc.counter_for_overlap))
        if self.antenna_adc.counter_for_overlap < 0:
            direction = 1 # clockwise
        else:
            direction = 0 # anti-clockwise
        self.motor_adc.act(c_steps, direction)
        self.master.adcslogger.write_info('INIT MOTOR POSE')
        self.antenna_adc.update_position(c_steps*self.motor_adc.step_size, direction)
        self.master.adcslogger.write_info('antenna updated to {} with counter {}'.format(self.antenna_adc.position, self.antenna_adc.counter_for_overlap))

    def calc_new_position(self):
    #calc GEOMETRY
        thresshold = 0.1
        dx = abs(self.GS[0] - self.gps[0])
        dy = abs(self.gps[1] - self.GS[1])
        if dx < thresshold:
            # in same yy' axis
            if self.GS[1] < self.gps[1]:
                theta = 180
            else:
                theta = 0
        else:
            if dy < thresshold:
                dy = thresshold
            fi = math.atan(dx/dy) * 180 / math.pi
            if self.GS[0] < self.gps[0] and self.GS[1] < self.gps[1]:
                theta = 180 + fi #quartile = 1
            elif self.GS[0] < self.gps[0] and self.GS[1] > self.gps[1]:
                theta = 180 - fi #quartile = 2
            elif self.GS[0] > self.gps[0] and self.GS[1] > self.gps[1]:
                theta = fi #quartile = 3
            else:
               theta = 360 - fi # quartile = 4
     # end calc GEOMETRY
        theta_antenna_pointing = (self.antenna_adc.position + self.compass) % 360
        if theta_antenna_pointing < theta:
            dif1 = theta - theta_antenna_pointing
            dif2 = 360 - dif1
            if dif1 <= dif2:
                if self.antenna_adc.check_isinoverlap(dif1, +1):  # clockwise
                    self.difference = dif2
                    self.direction = 0  # ani-clockwise
                else:
                    self.difference = dif1
                    self.direction = 1  # clockwise
            else:
                if self.antenna_adc.check_isinoverlap(dif2, -1):  # anti-clockwise
                    self.difference = dif1
                    self.direction = 1  # clockwise
                else:
                    self.difference = dif2
                    self.direction = 0  # anti-clockwise
        else:
            dif2 = theta_antenna_pointing - theta
            dif1 = 360 - dif2
            if dif1 <= dif2:
                if self.antenna_adc.check_isinoverlap(dif1, +1):  # clockwise
                    self.difference = dif2
                    self.direction = 0  # ani-clockwise
                else:
                    self.difference = dif1
                    self.direction = 1  # clockwise
            else:
                if self.antenna_adc.check_isinoverlap(dif2, -1):  # anti-clockwise
                    self.difference = dif1
                    self.direction = 1  # clockwise
                else:
                    self.difference = dif2
                    self.direction = 0  # anti-clockwise

        self.master.adcslogger.write_info('Difference {} Direction {}'.format( self.difference, self.direction))

