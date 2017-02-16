
import math

with open("error_collection") as f:
    data = eval(f.read())

def find_erdst(x1, y1, x2, y2):
    return math.sqrt( (x1-x2)**2 + (y1 - y2) ** 2)
error_distance = 0
for i in data:
    error_distance += find_erdst(*i)


print float(error_distance) / len(data)
