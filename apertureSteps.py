

step_aperture = 2  ** (1/6)
start_aperture = 2
range_steps = range(3, 22) 

def format(value):
    
    if value >= 9.5:
        return f"{value:.0f}"
    else:
        return f"{value:.1f}"

for i in range_steps:
    value = start_aperture * (step_aperture ** i)
    print(format(value))