import json
import Paths as paths

if __name__ == '__main__':
    path = paths.Paths()
    status_vector =  {"TEMP_A": 1,"TEMP_B": 1, "HEAT_B_ON": 0, "HEAT_A_ON": 0, "IMU": 1, "GPS": 1, "DEP_READY": 0, "KILL": 0, "DMC_SLEEP": 0, "TX_ON": 0, "ADC_MAN": 0, "DEP_CONF": 0, "COMPASS": 1, "DEP_SUCS": 0, "RET_AB": 0, "RET_READY": 0, "RET_CONF": 0, "HEAT_SLEEP": 0, "RET_SUCS": 0, "ALTIMETER": 1, "AMP_TEMP": 1, "INFRARED": 1}
    command_vector = {"ADC_MAN": 0, "ADC_AUTO": 0, "SET": 0, "SCAN": 0, "INIT": 0, "HEAT_SLEEP": 0, "HEAT_AWAKE": 0, "DMC_AWAKE": 0, "DEP": 0, "DEP_CONF": 0, "DEP_AB": 0, "DEP_SUCS": 0, "DEP_RETRY": 0, "RET_CONF": 0, "RET_AB": 0, "RET": 0, "RET_SUCS": 0, "RET_RETRY": 0, "TX_SLEEP": 0, "TX_AWAKE": 0, "SIN": 0, "SPON": 0,"REBOOT_SLAVE": 0, "KILL": 0}
    json.dump(status_vector, open(path.file_status_vector, 'w'))
    json.dump(command_vector, open(path.file_command_vector, 'w'))

