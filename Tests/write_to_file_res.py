from threading import Thread
import time


def start_test(heat_inst):
    print("Start HEAT process")
    thread_data = Thread(target=heat_inst.threaded_function_data)
    thread_data.start()
    max_size = 100
    counter = 0
    while counter < max_size:
        #title = 'Results of heating test\n'
        path = '/home/despina/Dropbox/BEAM/Software/Shade/test_heat.txt'
        test_file = open(path, 'a+')
        #test_file.write(title)
        heat_inst.need_heating = heat_inst.consider_data()
        test_file.write("\tmean: %d\n" % heat_inst.mean_temp)
        if heat_inst.need_heating and not heat_inst.ison:
            test_file.write("\tin counter: ON\n")
            heat_inst.open_heat()
            heat_inst.ison = True
        elif not heat_inst.need_heating and heat_inst.ison:
            test_file.write("\tCLOSE HEAT")
            heat_inst.pause_heat()
            heat_inst.ison = False
        counter += 1
        time.sleep(1)
    test_file.close()
