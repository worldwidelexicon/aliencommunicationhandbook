import math
import string

def cone_to_point_cloud(slices = 10, radials = 36):
    rows = list()
    f = open('cone.csv','wc')
    ang_inc = math.radians(360.0 / radials)
    slice = 0
    while slice <= slices:
        r = int(1000 * (float(slice) / slices))
        ang = 0.0
        while ang <= math.radians(360):
            x = int(r * math.cos(ang)) + 1000
            y = int(r * math.sin(ang)) + 1000
            ang += ang_inc
            row = '((' + str(x) + ')(' + str(y) + ')(' + str(r) + ')) '
            if row not in rows:
                rows.append(row)
                f.write(row)
        slice += 1
    f.close()
    
    print len(rows)
    
cone_to_point_cloud()