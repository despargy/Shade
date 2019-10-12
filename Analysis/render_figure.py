import json
from matplotlib import pyplot as plt
import reader

class RenderFigure():

    def __init__(self, fig_cluster , obj_class):
        self.fig_cluster = fig_cluster
        self.obj_class = obj_class
        self.fig_settings = self.get_figure_settings()
        self.fig = plt.figure()


    def get_pause_time(self):
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['figures']['general_settings']["pause_time"]


    def get_figure_settings(self):
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['figures']


    def init_objs(self):
        self.fig_objects = []
        fig_names = self.fig_settings[self.fig_cluster]
        for fig_name in fig_names:
            self.fig_objects.append(self.obj_class(self.fig_cluster, fig_name, self.fig))

    def setup_objs(self):
        #set up figs
        for fig_obj in self.fig_objects:
            fig_obj.set_up()

    def read_data_objs(self,data_array):
        for fig_obj in self.fig_objects:
            #read new data
            fig_obj.read_data(data_array)      
    
    def set_data_objs(self):
        for fig_obj in self.fig_objects:
            #set new data
            fig_obj.set_data()

    def start(self):

        self.init_objs()
        #init canvas
        self.fig.canvas.draw()   # note that the first draw comes before setting data

        self.setup_objs()

        #init reader
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
                
                self.read_data_objs(data_array)

                self.fig.canvas.draw()
                self.fig.canvas.flush_events()

                self.set_data_objs()

                #pause
                plt.pause(self.get_pause_time())
