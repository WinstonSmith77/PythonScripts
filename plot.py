import numpy as np
import matplotlib.pyplot as plt 
 
  
# creating the dataset
data = {'C':20, 'C++':15, 'Java':30, 
        'Python':35}
courses = list(data.keys())
values = list(data.values())
  
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(courses, values, color ='maroon', 
        width = .5)
 
plt.xlabel("Pitcher")
plt.ylabel("Umsatz")
plt.title("Alle Haie im Teich")
plt.show()