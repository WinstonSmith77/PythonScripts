from math import atan2, pi

def get_line_angle(a, b):
    
    angle = atan2(b[1] - a[1], b[0] - a[0])

    return (angle / pi) * 180 


a = (0,0)
b = (1,1)

print(get_line_angle(a, b)) 
print(get_line_angle(b, a)) 