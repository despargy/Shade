import time
import math
import Antenna as antenna
import MotorADC as motor


#class to represent subsystem's proccess of ADC
class ADC():

    __instance = None
    #constructor
    #, Master, DataManager

    def __init__(self):
        if ADC.__instance != None:
            raise Exception("This class is a singleton!")
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
            self.motor_adc = motor.MotorADC()
            self.antenna_adc = antenna.Antenna()
            #self.master = master
            #self.datamanager = datamanager
            ADC.__instance = self


    def get_instance(self):
        if ADC.__instance == None:
            ADC()
        return ADC.__instance


    def start(self):
        isDeployed = True #!!!!!!!!!!! #self.master.isdeployed
        while not isDeployed:
            time.sleep(60)
        self.run_auto()


    #Auto mode of ADC
    def run_auto(self):
        isManual = False #!!!!!!!!!!!!! # #self.master.isdeployed
        while True:
            while isManual:
                time.sleep(2)
            print("ADC run auto\n")
            self.compass = self.get_compass_data() #self.datamanager.dictionary['angle_c']
            self.gps = self.get_gps_data()
            #self.gps[0] = self.get_gps_data() #self.datamanager.dictionary['gps_x]
            #self.gps[1] = self.get_gps_data() #self.datamanager.dictionary['gps_y']
            self.calc_new_position()
            c_step = self.convert_to_steps()
            self.notify_DMC_motor(c_step, self.direction)
            self.move_ADC_motor(c_step, self.direction)
            self.antenna_adc.update_position(c_step*self.motor_adc.step_size, self.direction)
            self.log_last_position(self.antenna_adc.counter_for_overlap)


    def get_compass_data(self):
        x = float(input("give compass\n"))
        #x = self.datamanager.dictionary['angle_c']
        return x


    def get_gps_data(self):
        x = float(input("give gps x\n"))
        y = float(input("give gps y\n"))
        return [x,y]


    def log_last_position(self, dif):
        pass #
    def notify_DMC_motor(self,a,b):
        pass
    def move_ADC_motor(self,c,d):
        self.motor_adc.act(c,d)
    def convert_to_steps(self):
        c_step = int(self.difference / self.motor_adc.step_size)
        return c_step
    def set_position(self):
        pass
    def scan(self):
        pass
    def calc_new_position(self):
    #calc GEOMETRY
        thresshold  = 0.1
        if abs(self.GS[0] - self.gps[0]) < thresshold:
            # in same yy' axis
            if self.GS[1] < self.gps[1]:
                theta = 180
            else:
                theta = 0
        else:
            fi = math.atan(abs(self.gps[0] - self.GS[0]) / abs(self.gps[1] - self.GS[1])) * 180 / math.pi
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
                    self.antenna_adc.sign_for_counter_overlap = -1
                else:
                    self.difference = dif1
                    self.direction = 1  # clockwise
                    self.antenna_adc.sign_for_counter_overlap = +1
            else:
                if self.antenna_adc.check_isinoverlap(dif2, -1):  # anti-clockwise
                    self.difference = dif1
                    self.direction = 1  # clockwise
                    self.antenna_adc.sign_for_counter_overlap = +1
                else:
                    self.difference = dif2
                    self.direction = 0  # anti-clockwise
                    self.antenna_adc.sign_for_counter_overlap = -1
        else:
            dif2 = theta_antenna_pointing - theta
            dif1 = 360 - dif2
            if dif1 <= dif2:
                if self.antenna_adc.check_isinoverlap(dif1, +1):  # clockwise
                    self.difference = dif2
                    self.direction = 0  # ani-clockwise
                    self.antenna_adc.sign_for_counter_overlap = -1
                else:
                    self.difference = dif1
                    self.direction = 1  # clockwise
                    self.antenna_adc.sign_for_counter_overlap = +1
            else:
                if self.antenna_adc.check_isinoverlap(dif2, -1):  # anti-clockwise
                    self.difference = dif1
                    self.direction = 1  # clockwise
                    self.antenna_adc.sign_for_counter_overlap = +1
                else:
                    self.difference = dif2
                    self.direction = 0  # anti-clockwise
                    self.antenna_adc.sign_for_counter_overlap = -1

        print("dif = \n", self.difference, "dir = \n", self.direction)

if __name__ == '__main__':
    adc_obj = ADC()
    adc_obj.start()

