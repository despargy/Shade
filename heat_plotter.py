from pylive import live_line_plotter_xy
import numpy as np
import time
import logger

def get_heat_from_data(data_row):
    return int(data_row.split(',')[-1])


def get_time_from_data(data_row):
    return int(data_row.split(',')[0])


if __name__ == '__main__':

    limit = 100
    x_vec = []
    y_vec = []
    line1 = []
    count = 0

    data_logger = logger.DataLogger()
    while True:
        data,total_rows = data_logger.get_unsend_data()
        if total_rows == 0:
            time.sleep(3)
            continue

        last_id = data[-1].split(',')
        last_id = last_id[0]
        data_logger.set_last_sended_index(last_id)

        for data_row in data:
            heat_value = get_heat_from_data(data_row)
            line_id = get_time_from_data(data_row)
            y_vec.append(heat_value)
            x_vec.append(line_id)

            if len(x_vec) == limit:
                x_vec.pop(0)
                y_vec.pop(0)
            color = 'r' if heat_value > 10 else 'b'
            line1 = live_line_plotter_xy(x_vec,y_vec,line1,title="Heat Temperature",pause_time=0.2,color=color)
            count += 1