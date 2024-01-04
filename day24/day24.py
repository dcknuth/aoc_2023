'''AoC Day 24 Part 1 - how many path intersections occur in the test area?
'''
import numpy as np

DEBUG = 4
#filename = "test24-1.txt"
filename = "input24.txt"

with open(filename) as f:
    ls = f.read().strip().split('\n')

hailstones = []
for l in ls:
    pos, vel = l.split(' @ ')
    px, py, pz = map(int, pos.split(', '))
    vx, vy, vz = map(int, vel.split(', '))
    hs = [px, py, pz, vx, vy, vz]
    hailstones.append(hs)

def intersect(x1, y1, vx1, vy1, x2, y2, vx2, vy2):
    m1 = vy1 / vx1 if vx1 != 0 else float('inf')
    m2 = vy2 / vx2 if vx2 != 0 else float('inf')
    a1, b1, c1 = (m1, -1, m1 * x1 - y1) if vx1 != 0 else (1, 0, x1)
    a2, b2, c2 = (m2, -1, m2 * x2 - y2) if vx2 != 0 else (1, 0, x2)
    A = np.array([[a1, b1], [a2, b2]])
    C = np.array([c1, c2])
    try:
        intersection = np.linalg.solve(A, C)
        return(intersection)
    except np.linalg.LinAlgError:
        return(None)

def crossPast(ip, px1, py1, vx1, vy1, px2, py2, vx2, vy2):
    if ip[0] < px1:
        if vx1 > 0:
            return(True)
    if ip[1] < py1:
          if vy1 > 0:
            return(True)
    if ip[0] > px1:
        if vx1 < 0:
            return(True)
    if ip[1] > py1:
        if vy1 < 0:
            return(True)
    if ip[0] < px2:
        if vx2 > 0:
            return(True)
    if ip[1] < py2:
        if vy2 > 0:
            return(True)
    if ip[0] > px2:
        if vx2 < 0:
            return(True)
    if ip[1] > py2:
        if vy2 < 0:
            return(True)
    if ip[0] < px2:
        if vx2 > 0:
            return(True)
    if ip[1] < py2:
        if vy2 > 0:
            return(True)
    return(False)

# MIN = 7
# MAX = 27
MIN = 200000000000000
MAX = 400000000000000
total = 0
for i, h1 in enumerate(hailstones):
    for h2 in hailstones[i+1:]:
        px1, py1, pz1, vx1, vy1, vz1 = h1
        px2, py2, pz2, vx2, vy2, vz2 = h2
        intersect_point = intersect(px1, py1, vx1, vy1,
                                    px2, py2, vx2, vy2)
        if DEBUG > 4:
            print("Intersect of", px1, py1, "and", px2, py2, "is",
                  intersect_point)
        if intersect_point is not None:
            if crossPast(intersect_point,
                        px1, py1, vx1, vy1,
                        px2, py2, vx2, vy2):
                continue
            if intersect_point[0] >= MIN and intersect_point[0] <= MAX and \
                intersect_point[1] >= MIN and intersect_point[1] <= MAX:
                total += 1
        else:
            continue
print(total, "hailstones have an x y cross in the region in the future")


'''Part2 - catch all the hailstones with a single, thrown rock. Add the
coordinates the rock would have to start from'''
# Formulas for where a hailstone will be in standard linear format
# vx1 * t1 - x1 = -px1
# vy1 * t1 - y1 = -py1
# vz1 * t1 - z1 = -pz1
# rock t1
# rvx * t1 - x1 = -rx
# rvy * t1 - y1 = -ry
# rvz * t1 - z1 = -rz
# next hailstone t2
# vx2 * t2 - x2 = -px2
# vy2 * t2 - y2 = -py2
# vz2 * t2 - z2 = -pz2
# rock t2
# rvx * t2 - x2 + rx = 0
# rvy * t2 - y2 + ry = 0
# rvz * t2 - z2 + rz = 0
# Should be enough to calculate catching three hailstones with the rock
#  as we would be at 18 equations and 18 variables

# I ended up borrowing this answer which uses the m3 solver
# https://github.com/fuglede/adventofcode/blob/master/2023/day24