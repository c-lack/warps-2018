import numpy as np

class Queen:
    alive = True
    age = 1
    repro_rate = 1
    new_borns = 0
    food_required = 5

    def update(self):
        self.age = self.age + 1
        self.new_borns = np.random.poisson(self.repro_rate)

class Juvenile:
    alive = True
    age = 1
    maturity_age = 5
    food_required = 1

    def update(self):
        self.age = self.age + 1

    def mature(self):
        if (self.age > self.maturity_age):
            return Worker()
        return self

class Worker:
    alive = True
    age = 1
    food_collection_rate = 1
    food_collected = 0
    food_required = 2

    def update(self):
        self.age = self.age + 1
        self.food_collected = np.random.poisson(self.food_collection_rate)

    def become_queen(self):
        queen = Queen()
        queen.age = self.age
        return queen

class Colony:
    population = [Queen()]
    capacity = 10
    food_stockpile = 10

    def update_population(self):
        for idx, mole in enumerate(self.population):
            mole.update()
            if (type(mole).__name__ == 'Queen'):
                self.produce_new_borns(mole.new_borns)
            elif (type(mole).__name__ == 'Worker'):
                self.supply_food(mole.food_collected)
            elif (type(mole).__name__ == 'Juvenile'):
                self.population[idx] = mole.mature()

    def produce_new_borns(self, new_borns):
        while (len(self.population) < self.capacity and new_borns > 0):
            self.population.append(Juvenile())
            new_borns = new_borns - 1

    def supply_food(self, food_collected):
        self.food_stockpile += food_collected

    def consume_food(self):
        self.population.sort(key = lambda x : x.age)
        self.population.sort(key = lambda x : type(x).__name__, reverse=True)
        for mole in self.population:
            if (self.food_stockpile > mole.food_required):
                self.food_stockpile = self.food_stockpile - mole.food_required
            else:
