import numpy as np
import reader
import render_figure
import plot_interface
import sys

class LinePlot(plot_interface.PlotInterface):

    
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



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("""
              [+] Run line_plot program with one argument.
              [+] The argument indicates the cluster figure
              [+] e.g python plot_line.py temperature or
                      python plot_line.py pressure
              """)
    else:
        cluster = sys.argv[1]
        render_figure.RenderFigure(cluster,LinePlot).start()
    