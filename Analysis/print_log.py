import reader as reader
import sys
import time



def log_starts_with(log, str_filter, reversed = False):

    try:
        log = log.split(',')[2]
        prefix = log.split()[2]
        return True if str_filter == 'all' or prefix.startswith(str_filter) else False
    except:
        return False 

    
def get_logs(logs,str_filter):
    filtered_logs = []
    for log in logs:
        if log_starts_with(log,str_filter):
            filtered_logs.append(log)

    return filtered_logs


def get_search_strs():
    return [
        'TX',
        'DMC',
        'ADC',
        'DataManager'
    ]

def log_is_rest(log):
     try:
        log = log.split(',')[2]
        prefix = log.split()[2]
        return False if prefix in get_search_strs() else True
     except:
         return True


def get_rest_logs(logs):
    filtered_logs = []
    for log in logs:
        if log_is_rest(log):
           filtered_logs.append(log)

    return filtered_logs



if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("""
            [+] Invalid args 
            [+] e.g. python3 print_logs.py info DMC: or
            [+]      python3 print_logs.py info REST or
            [+]      python3 print_logs.py data all
            """)
        sys.exit(0)

    is_data_reader = False
    if(sys.argv[1] == 'data'):
        rd = reader.Reader('elink.data.log','name')
        is_data_reader = True

    elif(sys.argv[1] == 'info'):
        rd = reader.Reader('elink.info.log','name')
    else:
        print("""
            [+] Invalid args 
            [+] e.g. python3 print_logs.py info DMC: or
            [+]      python3 print_logs.py info REST or
            [+]      python3 print_logs.py data all
            """)
        sys.exit(0)

    str_filters = sys.argv[2]
    while True:
        data, total_rows = rd.get_unread_logs()

        if total_rows == 0:
            time.sleep(3)
            continue
        
        if is_data_reader:
            for log in data:
                print(log)
        elif str_filters == 'REST':
            for log in get_rest_logs(data):
                print(log)
        else:
            for log in get_logs(data,str_filters):
                print(log)


