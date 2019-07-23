import MotorADC as motor


def test_action():

    motor.act(10, 1)
    print("18 degrees clockwise: DONE")
    motor.act(10, 0)
    print("18 degrees anti-clockwise: DONE")
    motor.act(100, 1)
    print("180 degrees clockwise: DONE")
    motor.act(100, 0)
    print("180 degrees anti-clockwise: DONE")
    motor.act(200, 0)
    print("360 degrees anti-clockwise: DONE")
    motor.act(200, 1)
    print("360 degrees clockwise: DONE")


def test_unit():

    motor.act(True, 1)
    print("test true")
    motor.act(None, 1)
    print("test negative")
    motor.act(-3, 1)
    print("test ")


motor = motor.MotorADC()
test_unit()


