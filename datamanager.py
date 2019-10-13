#DataManager

import smbus
import time
import ms5803py
import mag3110
import serial
import as7262
import statistics
import math
#import Paths as paths

class DataManager:
    #constructor
        def __init__(self,master,infologger,datalogger):
                self.master = master
                self.infologger = infologger
                self.datalogger = datalogger
                self.gps_port = "/dev/ttyACM0"
                self.imu_port = "/dev/ttyACM1"
                self.bus = smbus.SMBus(1)
                #@TODO TBD
                self.P0 = 1015
                self.dictionary = dict()
                self.last_compass = 0
                try:
                        self.compass = mag3110.compass()
                        self.master.status_vector["COMPASS"] = 1			
                except:
                        self.infologger.write_error("DataManager: Can't connect to compass.")
                        self.master.status_vector["COMPASS"] = 0
                try:		
                        self.compass.loadCalibration()
                except FileNotFoundError:	
                        self.infologger.write_error("DataManager: Can't locate the calibration file.")
                        self.master.status_vector["COMPASS"] = 0
                try:			
                        self.altimeter = ms5803py.MS5803()
                        self.master.status_vector["ALTIMETER"] = 1			
                except:
                        self.infologger.write_error("DataManager: Can't connect to altimeter.")
                        self.master.status_vector["ALTIMETER"] = 0		
                try:			
                        self.ser_gps = serial.Serial(self.gps_port, baudrate=9600, timeout=0.5)
                        self.master.status_vector["GPS"] = 1			
                except:
                        self.infologger.write_error("DataManager: Can't connect to GPS.")
                        self.master.status_vector["GPS"] = 0		
                try:    			
                        self.ser_imu = serial.Serial(self.imu_port, baudrate=9600, timeout=0.5)
                        self.master.status_vector["IMU"] = 1			
                except:
                        self.infologger.write_error("DataManager: Can't connect to IMU.")
                        self.master.status_vector["IMU"] = 0
                try:
                        self.infrared = as7262.AS7262()
                        self.master.status_vector["INFRARED"] = 1			
                except:
                        self.infologger.write_error("DataManager: Can't connect to infrared sensor.")
                        self.master.status_vector["INFRARED"] = 0
                        		
        def start(self):
                self.init_dict()
                while True:
                        self.read_temp_A()
                        self.read_temp_B()
                        self.read_altitude(self.P0)
                        self.read_amp_temp()
                        self.read_gps()
                        self.read_compass()
                        self.read_imu()
                        self.read_inf_temp()
                        self.read_ras_temp()
                        self.write_tx_file()
                        self.datalogger.write_info(self.get_log_data())
                        time.sleep(5)
        
        def init_dict(self):
                self.dictionary["temp_A"] = None
                self.dictionary["temp_B"] = None
                self.dictionary["int_temp"] = None
                self.dictionary["inf_temp"] = None
                self.dictionary["amp_temp"] = None
                self.dictionary["ras_temp"] = None
                self.dictionary["pressure"] = None
                self.dictionary["altitude"] = None
                self.dictionary["time_gps"] = None
                self.dictionary["gps_y"] = None
                self.dictionary["gps_x"] = None
                self.dictionary["altitude_gps"] = None
                self.dictionary["angle_c"] = None
                self.dictionary["time_imu"] = None
                self.dictionary["accelX"] = None
                self.dictionary["accelY"] = None
                self.dictionary["accelZ"] = None
                self.dictionary["gyroX"] = None
                self.dictionary["gyroY"] = None
                self.dictionary["gyroZ"] = None
                self.dictionary["magX"] = None
                self.dictionary["magY"] = None
                self.dictionary["magZ"] = None
                       
   
        def get_log_data(self):
                return_string = "{} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {}, {}, {}, {}, {}"
                return return_string.format(
                 self.dictionary["temp_A"],
                 self.dictionary["temp_B"],
                 self.dictionary["int_temp"],
                 self.dictionary["inf_temp"],
                 self.dictionary["amp_temp"],
                 self.dictionary["ras_temp"],
                 self.dictionary["pressure"],
                 self.dictionary["altitude"],
                 self.dictionary["time_gps"],
                 self.dictionary["gps_y"],
                 self.dictionary["gps_x"],
                 self.dictionary["altitude_gps"],
                 self.dictionary["angle_c"],
                 self.dictionary["time_imu"],
                 self.dictionary["accelX"],
                 self.dictionary["accelY"],
                 self.dictionary["accelZ"],
                 self.dictionary["gyroX"],
                 self.dictionary["gyroY"],
                 self.dictionary["gyroZ"],
                 self.dictionary["magX"],
                 self.dictionary["magY"],
                 self.dictionary["magZ"]
               )
       
        def get_data(self, name):
                try:
                        return self.dictionary[name]
                except:
                        return None
                
        def read_temp_A(self):
                try:
                        #self.infologger.write_info("Reading external temperature...")
                        # TCN75A address, 0x48(72)
                        # Select configuration register, 0x01(01)
                        #       0x60(96)    12-bit ADC resolution
                        self.bus.write_byte_data(0x48, 0x01, 0x60)

                        time.sleep(0.5)

                        # TCN75A address, 0x48(72)
                        # Read data back from 0x00(00), 2 bytes
                        # temp MSB, temp LSB
                        data = self.bus.read_i2c_block_data(0x48, 0x00, 2)
                        # Convert the data to 12-bits
                        temp = ((data[0] * 256) + (data[1] & 0xF0)) / 16
                        if temp > 2047:
                                temp -= 4096
                        cTemp = temp * 0.0625
                        self.dictionary['temp_A'] = cTemp
                        self.master.status_vector["TEMP_A"] = 1
                        #self.infologger.write_info("Finished reading external temperature.")
                except: 
                        self.infologger.write_error("Error: I2C: reading temperature A.")
                        self.master.status_vector["TEMP_A"] = 0

        def read_temp_B(self):
                try:
                        #self.infologger.write_info("Reading external temperature...")
                        # TCN75A address, 0x4c)
                        # Select configuration register, 0x01(01)
                        #       0x60(96)    12-bit ADC resolution
                        self.bus.write_byte_data(0x4c, 0x01, 0x60)

                        time.sleep(0.5)

                        # TCN75A address, 0x4c(76)
                        # Read data back from 0x00(00), 2 bytes
                        # temp MSB, temp LSB
                        data = self.bus.read_i2c_block_data(0x4c, 0x00, 2)
                        # Convert the data to 12-bits
                        temp = ((data[0] * 256) + (data[1] & 0xF0)) / 16
                        if temp > 2047:
                                temp -= 4096
                        cTemp = temp * 0.0625
                        self.dictionary['temp_B'] = cTemp
                        self.master.status_vector["TEMP_B"] = 1
                        #self.infologger.write_info("Finished reading external temperature.")
                except: 
                        self.infologger.write_error("Error: I2C: reading temperature B.")
                        self.master.status_vector["TEMP_B"] = 0

                
        def read_amp_temp(self):
                try:
                        # TCN75A address, 0x4a(74)
                        # Select configuration register, 0x01(01)
                        #       0x60(96)    12-bit ADC resolution
                        self.bus.write_byte_data(0x4a, 0x01, 0x60)

                        time.sleep(0.5)

                        # TCN75A address, 0x48(72)
                        # Read data back from 0x00(00), 2 bytes
                        # temp MSB, temp LSB
                        data = self.bus.read_i2c_block_data(0x4a, 0x00, 2)
                        # Convert the data to 12-bits
                        temp = ((data[0] * 256) + (data[1] & 0xF0)) / 16
                        if temp > 2047:
                                temp -= 4096
                        cTemp = temp * 0.0625
                        self.dictionary['amp_temp'] = cTemp
                        self.master.status_vector["AMP_TEMP"] = 1
                except: 
                        self.infologger.write_error("Error: I2C: reading amplifier temperature.")
                        self.master.status_vector["AMP_TEMP"] = 0
 

        def read_altitude(self, p0):
                try:
                        raw_temperature = self.altimeter.read_raw_temperature(osr=4096)
                        raw_pressure = self.altimeter.read_raw_pressure(osr=4096)
                        press, temp = self.altimeter.convert_raw_readings(raw_pressure, raw_temperature)
                        alt = (44330.0 * (1 - pow(press / p0, 1 / 5.255)))
                        self.dictionary['int_temp']= format(temp)
                        self.dictionary['pressure'] = format(press)
                        self.dictionary['altitude'] = format(alt)
                        self.master.status_vector["ALTIMETER"] = 1
                except:
                        self.infologger.write_error("Error: I2C: reading altimeter.")
                        self.master.status_vector["ALTIMETER"] = 0

        def read_gps(self):
                try:
                        while True:
                                data = self.ser_gps.readline()
                                s = b' '
                                if data[0:6] == b'$GNGGA':
                                        s = data.decode().split(",")
                                        if s[12] == '0':
                                                print("no satellite data available")
                                        #time = s[1]
                                        #lat = s[2]
                                        #dirLat = s[3]
                                        #lon = s[4]
                                        #dirLon = s[5]
                                        #numsat = s[6]
                                        #alt = s[9]
                                        #checksum = s[12]
                                        lat = float(s[2])
                                        if s[3] == 'S':
                                                lat = -lat
                                        lon = float(s[4])
                                        if s[5] == 'W':
                                                lon = -lon
                                        self.dictionary['time_gps'] = s[1]
                                        self.dictionary['gps_y'] = self.dmm_to_dd(lat)
                                        self.dictionary['gps_x'] = self.dmm_to_dd(lon)
                                        alt = float(s[9])
                                        self.dictionary['altitude_gps'] = alt
                                        break
                        self.master.status_vector["GPS"] = 1		
                except:
                        self.infologger.write_error("Error: Serial: reading GPS receiver.")
                        self.master.status_vector["GPS"] = 0


        def dmm_to_dd(self, x):
                s1 = math.floor(x / 100)
                s11 = (x - s1 * 100) / 60
                x = s1 + s11
                print(x)
                return x

        def read_compass(self):
                try:
                        angle = self.compass.getBearing()
                        #dif1 = abs(angle - self.last_compass)
                        #dif2 = 360 - dif1
                        #dif = min(dif1, dif2)
                        #if dif < 120 :
                        self.dictionary['angle_c'] = angle
                        self.master.status_vector["COMPASS"] = 1
                                #self.last_compass = angle
                except:
                        self.infologger.write_error("Error: I2C: reading compass.")
                        self.master.status_vector["COMPASS"] = 0

        def read_imu(self):
                try:
                        data = self.ser_imu.readline()
                        s = data.decode().split(",")
                        self.dictionary['time_imu'] = s[0]
                        self.dictionary['accelX'] = s[1]
                        self.dictionary['accelY'] = s[2]
                        self.dictionary['accelZ'] = s[3]
                        self.dictionary['gyroX'] = s[4]
                        self.dictionary['gyroY'] = s[5]
                        self.dictionary['gyroZ'] = s[6]
                        self.dictionary['magX'] = s[7]
                        self.dictionary['magY'] = s[8]
                        self.dictionary['magZ'] = s[9].strip("\r\n")
                        self.master.status_vector["IMU"] = 1
                except:
                        self.infologger.write_error("Error: Serial: reading IMU.")
                        self.master.status_vector["IMU"] = 0
	
        def read_color(self):
                #@TODO TBD
                white_thress = 290
                black_thress = 18
                try:
                        as7262.soft_reset()
                        hw_code, hw_version, fw_version = as7262.get_version()
                        as7262.set_gain(2)
                        as7262.set_integration_time(0.1)
                        as7262.set_measurement_mode(3)
                        as7262.set_illumination_led(1)
                        values = as7262.get_calibrated_values()
                        as7262.set_measurement_mode(3)
                        as7262.set_illumination_led(0)
                        string = ("{},{},{},{},{},{}").format(*values)
                        colors = string.split(",")
                        r = float(colors[0])
                        o = float(colors[1])
                        y = float(colors[2])
                        g = float(colors[3])
                        b = float(colors[4])
                        v = float(colors[5])
                        float_colors = list(map(float, colors))
                        max_c = max(float_colors)
                        max_s = 'RED'
                        if o == max_c :
                                max_c = o
                                max_s = 'RED' #'ORANGE'
                        elif r == max_c :
                                max_c = r
                                max_s = 'RED' #'RED'
                        elif y == max_c :
                                max_c = y
                                max_s = 'YELLOW' 
                        elif g == max_c :
                                max_c = g
                                max_s = 'GREEN' 
                        elif b == max_c :
                                max_c = b
                                max_s = 'BLUE'  
                        elif v == max_c :
                                max_c = v
                                max_s = 'BLUE' #'VIOLET'
                        mean = statistics.mean(float_colors)
                        if mean < black_thress :
                                max_s = 'BLACK'
                        elif mean > white_thress :
                                max_s = 'WHITE'
                        return max_s
                except:
                        self.infologger.write_error("Error: I2C: reading color.")
                        self.master.status_vector["INFRARED"]=0
                        return 'ERROR'

        def read_inf_temp(self):
                try:
                        while True:
                                status = self.bus.read_byte_data(0x49,0x00)
                                if (status & 0b00000010) == 0:
                                        break
                                else:
                                        pass
                        self.bus.write_byte_data(0x49,0x01,0x06)
                        while True:
                                status = self.bus.read_byte_data(0x49, 0x00)
                                if (status & 0b00000001) == 0x01:
                                        break
                                else:
                                        pass
                        inf_temp = self.bus.read_byte_data(0x49, 0x02)
                        self.dictionary['inf_temp'] = inf_temp
                except:
                        self.infologger.write_error("Error: I2C: reading infrared temperature.")
                        self.master.status_vector["INFRARED"]=0


        def read_ras_temp(self):
                try:
                        ras_temp = int(open('/sys/class/thermal/thermal_zone0/temp').read())/1e3
                        self.dictionary['ras_temp'] = ras_temp
                except:
                        self.infologger.write_error("Error: Ras: reading temperature")


        def write_tx_file(self):
                try:
                        f = open("tx_file.txt","w")
                        #time = self.dictionary['time_gps']
                        #temp = self.dictionary['temp_A']
                        str = self.get_tx_str()
                        f.write(str)
                        f.close()
                except:
                        self.infologger.write_error("Error: Handling TX file.")
	
        def get_tx_str(self):
                return_string = "(UTC):  ,External temperature {}"
                return return_string.format(
                 self.dictionary["temp_A"],
                 #self.dictionary["time_gps"],
                )
        
        
        	
if __name__ == '__main__':
	data_obj = DataManager()
	data_obj.start()
