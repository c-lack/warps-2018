from mole_sim import Colony

col = Colony()
col.initialise_colony()
for t in range(0,7000):
    col.update_population()
    col.remove_dead()
    col.consume_food()
    col.remove_dead()
    col.ensure_queen()

print(col)
