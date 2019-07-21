import Antenna as antenna

def test_update_position():
    print("pose before:", antenna.position)
    antenna.update_position(10,1)
    print("pose after:", antenna.position)
    print("pose before:", antenna.position)
    antenna.update_position(True,1)
    print("pose after:", antenna.position)
    print("pose before:", antenna.position)
    antenna.update_position(40,2)
    print("pose after:", antenna.position)

#TODO modify testing
def test_check_isinoverlap():
    print("pose before:", antenna.position)
    antenna.update_position(10,1)
    print("pose after:", antenna.position)
    print("pose before:", antenna.position)
    antenna.update_position(True,1)
    print("pose after:", antenna.position)
    print("pose before:", antenna.position)
    antenna.update_position(40,2)
    print("pose after:", antenna.position)


antenna = antenna.Antenna()
test_update_position()