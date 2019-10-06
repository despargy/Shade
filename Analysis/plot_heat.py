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
        """Gets the configuration for this figure
        
        Returns:
            list -- the configuration for this figure
        """
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['figures']['temp_names'][self.temp_name]


    def set_up(self):
        """Sets title , x and y label,
           initializes the x and y limits
        """
        self.h, = self.ax.plot(self.x, lw=3)
        self.ax.set_ylim(0,100)
        self.ax.set_xlim(0,100)
        self.ax.title.set_text(self.config["title"])
        self.ax.set_xlabel(self.config["x_label"])
        self.ax.set_ylabel(self.config["y_label"])


    def set_fig_color(self,curr_value):
        """Set the color of the figure
        
        Arguments:
            curr_value {int | float | nan}
        """
        if np.isnan(curr_value):
            self.h.set_color("orange")
        elif(curr_value >= self.config["danger_value"]):
            self.h.set_color("red")
        else:
            self.h.set_color("blue")


    def read_data(self,data_array):
        """Read data and appends em to dataset.
        
        Arguments:
            data_array {list} -- array with data from a row
        """
        value_type = self.config['value_type']
        curr_value = data_array[self.index]
        
        #if value is none
        if curr_value.strip() == 'None':
            #break line
            curr_value = np.nan
        else:
            if(value_type == 'float'):
                curr_value = float(curr_value)
            elif(value_type == 'int'):
                curr_value = int(curr_value)

        # TODO: Read time and not log id
        time = int(data_array[0])

        self.x = np.append(self.x,time)
        self.y = np.append(self.y,curr_value)

        if(len(self.x) > self.config["limit"]):
            #delete old values
            self.x = np.delete(self.x, 0)
            self.y = np.delete(self.y, 0)

        self.set_fig_color(curr_value)

        
        
    def set_data(self):
        if(len(self.x) > 0):
            self.ax.set_xlim(self.x[0] -1 , self.x[-1] +1)
                
            min_y = np.nanmin(self.y)
            
            if not np.isnan(min_y):
                self.ax.set_ylim(min_y - 10, np.nanmax(self.y) + 10)
                
                self.h.set_ydata(self.y)
                self.h.set_xdata(self.x)


    def get_column_index(self):
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['data_manager']['columns'][self.temp_name]

    @staticmethod
    def get_pause_time():
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['figures']['general_settings']["pause_time"]


def get_figure_settings():
    with open('../settings.json') as json_file:
        settings =  json.load(json_file)
        return settings['figures']

def start():

    #read the configuration settings
    fig_settings = get_figure_settings()
    #get temperature names
    fig_names = fig_settings["temp_names"]
    temp_figs = []

    #init readers
    rd = reader.Reader('elink.data.log','Data Logs' , 10)

    fig = plt.figure()

    #create TemperatureFig Objects
    for fig_name in fig_names:
        temp_figs.append(TemperatureFig(fig_name, fig, rd))

    #init canvas
    fig.canvas.draw()   # note that the first draw comes before setting data

    #set up figs
    for temp_fig in temp_figs:
        temp_fig.set_up()

    #start reading data
    while(True):
        #get unread logs
        data, total_rows = rd.get_unread_logs()

        #if not new data
        if total_rows == 0:
            plt.pause(3)
            continue
        
    
        for data_row in data:
            data_array = data_row.split(',')
            
            for temp_fig in temp_figs:
                #read new data
                temp_fig.read_data(data_array)

            fig.canvas.draw()
            fig.canvas.flush_events()

            for temp_fig in temp_figs:
                #set new data
                temp_fig.set_data()

            #pause
            plt.pause(TemperatureFig.get_pause_time())


if __name__ == '__main__':
    start()