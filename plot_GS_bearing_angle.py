GS = [1, 1] #static
gps = get_gondolas_gps() #from gps

# calc GEOMETRY
thresshold = 0.1
dx = abs(GS[0] - gps[0])
dy = abs(gps[1] - GS[1])
if dx < thresshold:
    # in same yy' axis
    if GS[1] < gps[1]:
        GS_todo_theta = 0
    else:
        GS_todo_theta = 180
else:
    if dy < thresshold:
        dy = thresshold
    fi = math.atan(dx / dy) * 180 / math.pi
    if GS[0] < gps[0] and GS[1] < gps[1]:
        GS_todo_theta = fi  # quartile = 1
    elif GS[0] < gps[0] and GS[1] > gps[1]:
        GS_todo_theta = 180 - fi  # quartile = 2
    elif GS[0] > gps[0] and GS[1] > gps[1]:
        GS_todo_theta = 180 + fi  # quartile = 3
    else:
        GS_todo_theta = 360 - fi  # quartile = 4
# end calc GEOMETRY
