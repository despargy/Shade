import matplotlib.pyplot as plt
import numpy as np
import math
import reader
import random
import json

class PlotAntenna():

    def __init__(self,fig_cluster,fig_name):
        self.fig_name = fig_name
        self.fig_cluster = fig_cluster
        self.antenna_theta = 0
        self.config = self.get_config()
        self.arrow_length = self.config['arrow_length']
        self.index_x = self.get_column_index("gps_x")
        self.index_y = self.get_column_index("gps_y")
        self.time_index = self.get_column_index("time_gps")
        self.angle_index = self.get_column_index('angle_index')
        self.gond_x = self.gond_y = 5 
        self.ground_x = self.config["ground_x"]
        self.ground_y = self.config["ground_y"]




    def get_column_index(self, fig_name = None):
        if fig_name == None:
            fig_name = self.fig_name
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['data_manager']['columns'][fig_name]


    def get_config(self):
        """Gets the configuration for this figure
        
        Returns:
            list -- the configuration for this figure
        """
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['figures'][self.fig_cluster][self.fig_name]

    def cart2pol(self,x, y):
        rho = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        return(rho, math.degrees(phi))

    def pol2cart(self, rho, phi):
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return(x, y)


    def format_time(self,time):
        try:
            time =  time.strip().split('.')[0]
            t = iter(time)
            return ":".join(a+b for a,b in zip(t,t))
        except:
            return "Unavailable"
        
    def run(self):
        ax = plt.axes()

        rd = reader.Reader('elink.data.log','Data Logs')
        
        while(True):
            
            data, total_rows = rd.get_unread_logs()

            #if not new data
            if total_rows == 0:
                plt.pause(3)
                continue
            
            for data_row in data:
                data_array = data_row.split(',')
                
                try:
                    time = data_array[self.time_index]
                    self.gond_x = float(data_array[self.index_x])
                    self.gond_y = float(data_array[self.index_y])
                    self.antenna_theta = float(data_array[self.angle_index])
                except:
                    continue



                #pause
                plt.pause(0.000001)
        
                r_s , theta_s = self.cart2pol(0,self.arrow_length)
            
                theta_s = math.radians(self.antenna_theta)
                
                x_s , y_s = self.pol2cart(r_s, theta_s)
                ax.clear()

                min_x = min(self.gond_x , self.ground_x)
                max_x = max(self.gond_x , self.ground_x)

                min_y = min(self.gond_y, self.ground_y)
                max_y = max(self.gond_y, self.ground_y)
                
                ax.set_xlim(min_x - 15 , max_x + 15)
                ax.set_ylim(min_y - 15 , max_y + 15)  



                ax.grid(True)
                ax.title.set_text('Antenna at {time}'.format(time=self.format_time(time)))
                ax.arrow(self.gond_x, self.gond_y, x_s, y_s, head_width=0.3, head_length=0.7, fc='lightblue', ec='red')
                ax.plot(self.ground_x , self.ground_y, 'o', color='black')
        
        
        plt.show()
           
if __name__ == "__main__":
    PlotAntenna("antennas", "antenna_position").run()

