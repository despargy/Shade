tempC= int(open('/sys/class/thermal/thermal_zone0/temp').read())/1e3
print('rasb temperature now = {}'.format(tempC))