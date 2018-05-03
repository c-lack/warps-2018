import numpy as np

def custom_sort(x):
    if (type(x).__name__ == 'Queen'):
        return 0
    elif (type(x).__name__ == 'Worker'):
        return 1
    elif (type(x).__name__ == 'Juvenile'):
        return 2

class Mole:
    age = 1
    alive = True

    def update(self):
        self.age = self.age + 1

    def kill(self):
        self.alive = False

class Queen(Mole):
    new_borns = 0

    repro_rate = 1 # TODO
    food_required = 5 # TODO
    life_expectancy = 100 # TODO

    def update(self):
        super(Queen, self).update()
        if (self.age > self.life_expectancy):
            self.kill()
            return
        self.new_borns = np.random.poisson(self.repro_rate)

class Juvenile(Mole):
    maturity_age = 20 # TODO
    food_required = 1 # TODO

    def update(self):
        super(Juvenile, self).update()

    def mature(self):
        if (self.age > self.maturity_age):
            return Worker()
        return self

class Worker(Mole):
    food_required = 2 # TODO
    life_expectancy = 50 # TODO

    def update(self):
        super(Worker, self).update()
        if (self.age > self.life_expectancy):
            self.kill()
            return

    def become_queen(self):
        queen = Queen()
        queen.age = self.age
        return queen

class Colony:
    population = []
    food_stockpile = 0

    pop_capacity = 10 # TODO
    food_capacity = 100 # TODO
    food_collection_rate = 10 # TODO

    def __str__(self):
        s = ''
        s = s + 'food: ' + str(self.food_stockpile) + '\n'
        for idx, mole in enumerate(self.population):
            s = s + str(idx) + ' ' + type(mole).__name__ + ' ' + str(mole.age) + '\n'
        return s

    def initialise_colony(self,food_stockpile=10000,num_workers=0,num_juveniles=0):
        self.population.append(Queen())
        self.food_stockpile = food_stockpile
        for i in range(0,num_workers):
            self.population.append(Worker())
        for i in range(0,num_juveniles):
            self.population.append(Juvenile())

    def update_population(self):
        for idx, mole in enumerate(self.population):
            mole.update()
            if (type(mole).__name__ == 'Queen'):
                self.produce_new_borns(mole.new_borns)
            elif (type(mole).__name__ == 'Juvenile'):
                self.population[idx] = mole.mature()

    def produce_new_borns(self,new_borns):
        while (len(self.population) < self.pop_capacity and \
            new_borns > 0):
            self.population.append(Juvenile())
            new_borns = new_borns - 1

    def supply_food(self,food_collected):
        self.food_stockpile = self.food_stockpile + self.food_collection_rate*self.get_number_of_workers()**0.5

    def consume_food(self):
        self.population.sort(key = lambda x : x.age)
        self.population.sort(key = custom_sort)
        for mole in self.population:
            if (self.food_stockpile > mole.food_required):
                self.food_stockpile = self.food_stockpile - mole.food_required
            else:
                mole.kill()

    def remove_dead(self):
        self.population = [mole for mole in self.population if mole.alive]

    def ensure_queen(self):
        if (not self.has_queen()):
            if (not self.has_worker()):
                self.kill_colony()
            else:
                idx = self.get_random_worker_index()
                self.population[idx] = self.population[idx].become_queen()

    def has_queen(self):
        if (len([mole for mole in self.population if type(mole).__name__ == 'Queen']) == 0):
            return False
        else:
            return True

    def has_worker(self):
        if (len([mole for mole in self.population if type(mole).__name__ == 'Worker']) == 0):
            return False
        else:
            return True

    def get_random_worker_index(self):
        while(True):
            idx = np.random.randint(len(self.population))
            if (type(self.population[idx]).__name__ == 'Worker'):
                return idx

    def get_number_of_workers(self):
        return len([mole for mole in self.population if type(mole).__name__ == 'Worker'])

    def kill_colony(self):
        for mole in self.population:
            mole.kill()
