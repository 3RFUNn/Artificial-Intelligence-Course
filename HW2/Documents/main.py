import numpy as np
lines = np.loadtxt("database.cnf",dtype=int, delimiter="  ", unpack=False)
temp = ""


#to access each variable use this line :
for i in np.nditer(lines):
    print(i)

#good luck sir





