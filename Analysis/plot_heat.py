import time
from matplotlib import pyplot as plt
import numpy as np
import reader
import json

class TemperatureFig():

    def __init__(self, temp_name,fig, rd):
        self.fig = fig
        self.temp_name = temp_name
        self.config = self.get_config()
        self.index = self.get_column_index()
        self.x = np.array([])
        self.y = np.array([])
        self.ax = self.fig.add_subplot(*self.config["dimensions"])
        self.reader = rd 



    def get_config(self):
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['figures'][self.temp_name]


    def set_up(self):
        self.h, = self.ax.plot(self.x, lw=3)
        self.ax.set_ylim(0,100)
        self.ax.set_xlim(0,100)
        self.ax.title.set_text(self.config["title"])
        self.ax.set_xlabel(self.config["x_label"])
        self.ax.set_ylabel(self.config["y_label"])

    def read_data(self,data_array):
        value_type = self.config['value_type']
        curr_value = data_array[self.index]
        
        if curr_value.strip() == 'None': return

        if(value_type == 'float'):
            curr_value = float(curr_value)
        elif(value_type == 'int'):
            curr_value = int(curr_value)

        # TODO: Read time and not log id
        time = int(data_array[0])

        self.x = np.append(self.x,time)
        self.y = np.append(self.y,curr_value)

        if(len(self.x) > self.config["limit"]):
            self.x = np.delete(self.x, 0)
            self.y = np.delete(self.y, 0)
        
        
        if(curr_value >= self.config["danger_value"]):
            self.h.set_color("red")
        else:
            self.h.set_color("blue")

        
        
    def set_data(self):
        if(len(self.x) > 0):
            self.ax.set_xlim(self.x[0] -1 , self.x[-1] +1)
            self.ax.set_ylim(np.amin(self.y) - 10, np.amax(self.y) + 10)

            self.h.set_xdata(self.x)
            self.h.set_ydata(self.y)


    def get_column_index(self):
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['data_manager']['columns'][self.temp_name]



def start():
    fig = plt.figure()
    temp_names = ['temp_A' , 'temp_B' , 'int_temp' , 'inf_temp', 'amp_temp', 'ras_temp']
    #temp_names = ['temp_A','int_temp']
    temp_figs = []

    rd = reader.Reader('elink.data.log','Data Logs' , 10)

    for temp_name in temp_names:
        temp_figs.append(TemperatureFig(temp_name,fig,rd))

    fig.canvas.draw()   # note that the first draw comes before setting data

    for temp_fig in temp_figs:
        temp_fig.set_up()

    while(True):
        data, total_rows = rd.get_unread_logs()
        if total_rows == 0:
            plt.pause(3)
            continue

        for data_row in data:
            data_array = data_row.split(',')

            for temp_fig in temp_figs:
                temp_fig.read_data(data_array)

            fig.canvas.draw()
            fig.canvas.flush_events()

            for temp_fig in temp_figs:
                temp_fig.set_data()

            plt.pause(0.000001)
            #plt.pause calls canvas.draw(), as can be read here:
            #http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
            #however with Qt4 (and TkAgg??) this is needed. It seems,using a different backend,
            #one can avoid plt.pause() and gain even more speed.


if __name__ == '__main__':
    
    start() # 28 fps
    #live_update_demo(False) # 18 fps