import render_figure
import plot_interface
import numpy as np
import math

class AnglePlot(plot_interface.PlotInterface):

    def set_up(self):
        self.theta = np.nan

    def set_fig_color(self,curr_value):
        pass

    def read_data(self,data_array):
        value_type = self.config['value_type']
        
        try:
            curr_value = data_array[self.index]
        except:
            curr_value = np.nan
            self.time = 'Unavailable'
        else:
            self.time = int(data_array[0])

        #if value is none
        if str(curr_value).strip() == 'None':
            #break line
            curr_value = np.nan
        else:
            value_type = self.str_to_command(value_type)
            curr_value = value_type(curr_value)

            self.theta = math.radians(curr_value)

    
    def set_data(self):
        self.ax.clear()
        self.ax.set_theta_zero_location('N')
        title = "{title}\nAngle : {theta}\nat {time}".format(title=self.config["title"], 
                                                                theta= round(math.degrees(self.theta),2),
                                                                time= self.time)
        self.ax.title.set_text(title)
        self.ax.bar(self.theta, 1, width=self.config["width"], bottom=0.0, alpha=1)


if __name__ == '__main__':
    render_figure.RenderFigure("angles",AnglePlot).start()