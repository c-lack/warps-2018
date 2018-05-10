import mole_sim
from mole_sim import Colony
import numpy as np
import sys
import time

t0 = time.time()

col = Colony()
col.initialise_colony()
N = 100
T = int(sys.argv[1]) # time steps per realisation
R = int(sys.argv[2]) # number of realisations

col.pop_capacity = N

pop_mean = np.zeros(T)
food_mean = np.zeros(T)

for i in range(0,R):
    for t in range(0,T):
        col.update_population()
        col.remove_dead()
        col.consume_resource()
        col.remove_dead()
        col.ensure_queen()
        pop_mean[t] += len(col.population)/R
        food_mean[t] += col.resource_stockpile/R

t1 = time.time()
print(t1-t0)

import matplotlib.pylab as plt

plt.plot(range(T),pop_mean)
plt.show()

plt.plot(range(T),food_mean)
plt.show()

np.savetxt('mole_statistics.txt',np.vstack((pop_mean,food_mean)))

# np.savetxt('population_history.txt',cells,fmt='%i')
# np.savetxt('resource_history.txt',food,fmt='%i')