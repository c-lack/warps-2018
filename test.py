import mole_sim
from mole_sim import Colony
import numpy as np
import sys

col = Colony()
col.initialise_colony()
N = int(sys.argv[1]) # typically N=20
T = int(sys.argv[2]) # 1 is a quarter
col.pop_capacity = N

cells = np.zeros([N,T])-1
food = np.zeros(T)

for t in range(0,T):
    col.update_population()
    col.remove_dead()
    col.consume_food()
    col.remove_dead()
    col.ensure_queen()
    food[t] = col.food_stockpile
    for i in range(0,len(col.population)):
    	cells[i,t] = mole_sim.custom_sort(col.population[i])

import matplotlib.pylab as plt

plt.imshow(cells,aspect='auto')
plt.show()

plt.plot(range(T),food)
plt.show()

np.savetxt('population_history.txt',cells,fmt='%i')