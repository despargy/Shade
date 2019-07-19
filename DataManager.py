#DataManager

import smbus
import time
import ms5803py
import mag3110
import serial
#import loggerd


class DataManager:
    #constructor
    def __init__(self):
        self.gps_port = "/dev/ttyACM0"
        self.imu_port = "/dev/ttyACM1"
        self.compass = mag3110.compass()
        self.compass.loadCalibration()
        # Get I2C bus
        self.bus = smbus.SMuBus(1)
        self.altimeter = ms5803.MS5803()
        self.ser_gps = serial.Serial(self.gps_port, baudrate=9600, timeout=0.5)
        self.ser_imu = serial.Serial(self.imu_port, baudrate=9600, timeout=0.5)
        self.P0 = 1007
        self.dictionary = dict()

    def start(self):
        while True:
            self.read_temp()
            self.read_altitude(self.P0)
            self.read_gps()
            self.read_compass()
            self.read_imu()
            #logger
            print("Read all sensors")
            print(self.dictionary)
            #ekxwrisi se arxeio
            time.sleep(3)

    def read_temp(self):
        #logger
        print("Reading external temperature.")
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
        self.dictionary['ext_temp'] = cTemp

    def read_altitude(self, p0):
        #logger
        print("Reading altimeter..")
        raw_temperature = self.altimeter.read_raw_temperature(osr=4096)
        raw_pressure = self.altimeter.read_raw_pressure(osr=4096)
        press, temp = self.altimeter.convert_raw_readings(raw_pressure, raw_temperature)
        alt = (44330.0 * (1 - pow(press / p0, 1 / 5.255)))
        self.dictionary['int_temp']= raw_temperature
        self.dictionary['pressure'] = raw_pressure
        self.dictionary['altitude'] = alt

    def read_gps(self):
        #logger
        print("Reading GPS...")
        data = self.ser_gps.readline()
        s1 = b' '
        s2 = b' '
        if data[0:6] == b'$GNGLL':
            s1 = data.decode().split(",")
            if s1[7] == '0':
                print("no satellite data available")
            #time = s1[5]
            #lat = s1[1]
            #dirLat = s1[2]
            #lon = s1[3]
            #dirLon = s1[4]
            #stat = s1[6]
            #checksum = s1[7]
        if data[0:6] == b'$GNGGA':
            s2 = data.decode().split(",")
            if s2[12] == '0':
                print("no satellite data available")
            #time = s2[1]
            #lat = s2[2]
            #dirLat = s2[3]
            #lon = s2[4]
            #dirLon = s2[5]
            #numsat = s2[6]
            #alt = s2[9]
            #checksum = s2[12]
        if s1[6]!= 'A':
            self.read_gps()
        else:
            lat = float(s1[1])/100
            if s1[2] == 'S':
                lat = -lat
            lon = float(s1[3])
            if s1[4] == 'W':
                lon = -lon
            self.dictionary['time_gps'] = s1[1]
            self.dictionary['gps_y'] = lat
            self.dictionary['gps_x'] = lon
            alt = float(s2[9])
            self.dictionary['altitude_gps'] = alt

    def read_compass(self):
        #logger
        print("Reading compass")
        angle = self.compass.getBearing()
        self.dictionary['angle_c'] = angle

    def read_imu(self):
        #logger
        print("Reading IMU...")
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
        self.dictionary['magZ'] = s[9]


if __name__ == '__main__':
    data_obj = DataManager()
    data_obj.start()