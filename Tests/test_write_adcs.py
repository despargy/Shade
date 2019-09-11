from logger import InfoLogger, DataLogger, AdcsLogger
from file_read_backwards import FileReadBackwards
import os


adcs_logger = AdcsLogger()
dir = "Logs"
if (not os.path.isdir(dir)):
    os.mkdir(dir)

file_name = "{dir}/{filename}".format(dir=dir, filename='adcs.log')

adcs_logger.write_info(' {}, {} '.format(10,2))
adcs_logger.write_info(' {}, {} '.format(10,2))
adcs_logger.write_info(' {}, {} '.format(10,345))

with FileReadBackwards(file_name, encoding="utf-8") as log_file:
    for line in log_file:
        line_id = line.split(',')[1]
        print(line_id)
        break