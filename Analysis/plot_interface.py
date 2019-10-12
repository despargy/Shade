from abc import ABC, abstractmethod
import json
import numpy as np
import builtins


class PlotInterface(ABC):

    def __init__(self, fig_cluster, fig_name, fig):
        self.fig = fig
        self.fig_name = fig_name
        self.fig_cluster = fig_cluster
        self.config = self.get_config()
        self.auto_scale = self.get_auto_scale()
        self.index = self.get_column_index()
        self.x = np.array([0])
        self.y = np.array([0])
        if "projection" in self.config:
            self.ax = self.fig.add_subplot(self.config["dimensions"], projection=self.config["projection"])
        else:
            self.ax = self.fig.add_subplot(*self.config["dimensions"])



    def get_auto_scale(self):
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['figures']['general_settings']["auto_scale"]


    def get_config(self):
        """Gets the configuration for this figure
        
        Returns:
            list -- the configuration for this figure
        """
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['figures'][self.fig_cluster][self.fig_name]

    
    def get_column_index(self, fig_name = None):

        if fig_name == None:
            fig_name = self.fig_name
        with open('../settings.json') as json_file:
            settings =  json.load(json_file)
            return settings['data_manager']['columns'][fig_name]

    @staticmethod
    def str_to_command(str_command):
        return getattr(builtins, str_command)


    @abstractmethod
    def set_up(self):
        """Sets title , x and y label,
           initializes the x and y limits
        """
        pass

    @abstractmethod
    def set_fig_color(self,curr_value):
        """Set the color of the figure
        
        Arguments:
            curr_value {int | float | nan}
        """
        pass

    @abstractmethod
    def read_data(self,data_array):
        """Read data and appends em to dataset.
        
        Arguments:
            data_array {list} -- array with data from a row
        """
        pass


    @abstractmethod
    def set_data(self):
        pass


    