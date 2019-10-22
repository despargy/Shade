import plot_line
import numpy as np
import reader
import render_figure

class PlotAltitude(plot_line.LinePlot):

    def __init__(self, fig_cluster, fig_name, fig):
        self.fig = fig
        self.fig_name = fig_name
        self.fig_cluster = fig_cluster
        self.config = self.get_config()
        self.index_alt = self.get_column_index("altitude")
        self.index_gps_alt = self.get_column_index("altitude_gps")
        self.alt_x = self.alt_y =  np.array([])
        self.gps_alt_x = self.gps_alt_y = np.array([])
        self.ax = self.fig.add_subplot(*self.config["dimensions"])


    def set_fig_color(self,curr_value):
        pass
    
    def set_up(self):
        """Sets title , x and y label,
           initializes the x and y limits
        """
        self.h_alt, = self.ax.plot(self.alt_x, lw=3 , label="Altitude")
        self.h_gps_alt, = self.ax.plot(self.gps_alt_x, lw=3 , label="GPS Altitude")
        self.ax.legend(bbox_to_anchor=(1.05, 1), loc='lower center', borderaxespad=0.)
        self.ax.set_ylim(0,100)
        self.ax.set_xlim(0,100)
        self.ax.title.set_text(self.config["title"])
        self.ax.set_xlabel(self.config["x_label"])
        self.ax.set_ylabel(self.config["y_label"])


    def read_data(self,data_array):
        """Read data and appends em to dataset.
        
        Arguments:
            data_array {list} -- array with data from a row
        """
        value_type = self.config['value_type']
        try:
            curr_value_alt = data_array[self.index_alt]
            curr_value_gps_alt = data_array[self.index_gps_alt]
        except:
            curr_value_alt = np.nan
            curr_value_gps_alt = np.nan
        

        value_type = self.str_to_command(value_type)
        
        if str(curr_value_alt).strip() == 'None':
            curr_value_alt = np.nan
        else:
            curr_value_alt  = value_type(curr_value_alt)
        
        if str(curr_value_gps_alt).strip() == 'None':
            curr_value_gps_alt = np.nan
        else:
            curr_value_gps_alt  = value_type(curr_value_gps_alt)
 
        # TODO: Read time and not log id
        time = int(data_array[0])

        self.alt_x = np.append(self.alt_x,time)
        self.alt_y = np.append(self.alt_y,curr_value_alt)

        self.gps_alt_x = np.append(self.gps_alt_x,time)
        self.gps_alt_y = np.append(self.gps_alt_y,curr_value_gps_alt)

        if(len(self.alt_x) > self.config["limit"]):
            #delete old values
            self.alt_x = np.delete(self.alt_x, 0)
            self.alt_y = np.delete(self.alt_y, 0)

            self.gps_alt_x = np.delete(self.gps_alt_x, 0)
            self.gps_alt_y = np.delete(self.gps_alt_y, 0)

    
    def set_data(self):
        if(len(self.alt_x) > 0):
            self.ax.set_xlim(self.alt_x[0] -1 , self.alt_x[-1] +1)
            
            min_y = np.nanmin(np.array([np.nanmin(self.alt_y), np.nanmin(self.gps_alt_y)]))
            
            if not np.isnan(min_y):
                max_y = np.nanmax(np.array([np.nanmax(self.alt_y), np.nanmax(self.gps_alt_y)]))
                self.ax.set_ylim(min_y - 10, max_y + 10)
                
                self.h_alt.set_ydata(self.alt_y)
                self.h_alt.set_xdata(self.alt_x)

                self.h_gps_alt.set_ydata(self.gps_alt_y)
                self.h_gps_alt.set_xdata(self.gps_alt_x)


if __name__ == '__main__':
    render_figure.RenderFigure("altitudes",PlotAltitude).start()

