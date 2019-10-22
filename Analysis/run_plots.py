import os
import sys
import threading


def run_command(version,command):
    os.system('python{version} {command}'.format(version=version, command=command))

if __name__ == '__main__':

    version = "3"
    threading.Thread(target=run_command, args=(version,"plot_altitude.py")).start()
    threading.Thread(target=run_command, args=(version,"plot_angles.py")).start()
    threading.Thread(target=run_command, args=(version,"plot_antenna.py")).start()
    threading.Thread(target=run_command, args=(version,"plot_line.py temperatures")).start()
    threading.Thread(target=run_command, args=(version,"plot_line.py pressures")).start()
    threading.Thread(target=run_command, args=(version,"print_log.py info")).start()