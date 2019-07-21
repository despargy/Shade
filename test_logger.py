from logger import AdcsLogger , InfoLogger , DataLogger
import sys

def test_logger(logger_type):
    """
       @logger_type: the type of logger.
       Test function to create dummy data, log them and then
       retrieve the unsend ones.
    """
    __instance = None

    if logger_type == 'adcs':
        __instance = AdcsLogger.get_instance()
    elif logger_type == 'data':
        __instance = DataLogger.get_instance()
    elif logger_type == 'info':
        __instance = InfoLogger.get_instance()
    else:
        print_prompt()

    for i in range(10):
        __instance.write_info('{loger_type} log from line {line}'.format(loger_type = logger_type , line=i))

    unsend_data,rows = __instance.get_unsend_data()
    print_unsend_data(unsend_data, logger_type)

    for i in range(5):
        __instance.write_warning('{loger_type} log from line {line}'.format(loger_type = logger_type , line=i))

    unsend_data,rows = __instance.get_unsend_data()
    print_unsend_data(unsend_data, logger_type)


def print_unsend_data(unsend_data,logger_type):
    #Prints the unsend data
    print('Unsend data from logger {logger_type}'.format(logger_type=logger_type))
    for data in unsend_data:
        print('\t'+data)


def print_prompt():
    print("""
          [+] Run test_logger program with one argument.
          [+] The argument indicates the unit
          [+] e.g python logger.py adcs
          [+] or  python logger.py info
          [+] or  python logger.py data
          """)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_prompt()
    else:
        test_logger(sys.argv[1])
