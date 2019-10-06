import json
from matplotlib import pyplot as plt
import reader

class RenderFigure():

    def __init__(self, name , obj_class):
        self.name = name
        self.obj_class = obj_class


    def get_pause_time(self):
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['figures']['general_settings']["pause_time"]


    def get_figure_settings(self):
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['figures']

    def start(self):

        #read the configuration settings
        fig_settings = self.get_figure_settings()
        #get temperature names
        fig_names = fig_settings[self.name]
        fig_objects = []

        fig = plt.figure()

        #create TemperatureFig Objects
        for fig_name in fig_names:
            fig_objects.append(self.obj_class(fig_name, fig))

        #init canvas
        fig.canvas.draw()   # note that the first draw comes before setting data

        #set up figs
        for fig_obj in fig_objects:
            fig_obj.set_up()

        #init readers
        rd = reader.Reader('elink.data.log','Data Logs')

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
                
                for fig_obj in fig_objects:
                    #read new data
                    fig_obj.read_data(data_array)

                fig.canvas.draw()
                fig.canvas.flush_events()

                for fig_obj in fig_objects:
                    #set new data
                    fig_obj.set_data()

                #pause
                plt.pause(self.get_pause_time())
