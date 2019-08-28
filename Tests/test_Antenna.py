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
    print("1:", antenna.check_isinoverlap(1,1))
    print("1:", antenna.check_isinoverlap(390,1))
    print("2:", antenna.check_isinoverlap(2,True))
    print("3:", antenna.check_isinoverlap(True,-1))
    print("4:", antenna.check_isinoverlap("lala",-1))
    if None:
        print("none")



antenna = antenna.Antenna()
test_check_isinoverlap()