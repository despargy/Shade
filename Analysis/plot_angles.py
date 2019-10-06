import render_figure
import plot_interface
import numpy as np
import math

class AnglePlot(plot_interface.PlotInterface):

    def set_up(self):
        pass

    def set_fig_color(self,curr_value):
        pass

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

            self.theta = math.radians(curr_value)

    
    def set_data(self):
        self.ax.clear()
        self.ax.set_theta_zero_location('N')
        self.ax.title.set_text(self.config["title"])
        self.ax.bar(self.theta, 1, width=self.config["width"], bottom=0.0, alpha=1)


if __name__ == '__main__':
    render_figure.RenderFigure("angle_names",AnglePlot).start()