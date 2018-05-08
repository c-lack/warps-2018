import numpy as np

def custom_sort(x):
    if (x.type == 'Queen'):
        return 0
    elif (x.type == 'Worker'):
        return 1
    elif (x.type == 'Juvenile'):
        return 2

class Mole:
    # Age of mole
    age = 1
    fitness = np.random.normal()

    # Status of mole
    alive = True

    # Change state of mole
    def kill(self):
        self.alive = False

class Queen(Mole):
    type = 'Queen'

    # Produce litter of ~11 once a year
    repro_rate = 0.25
    repro_size = [5,16]

    # Amount of resource consumed
    resource_consumption = 5 # TODO

    # probability of death 1/1000 per day
    death_prob = 0.013

    def update(self):
        self.age = self.age + 1
        if (np.random.rand() < self.death_prob):
            self.kill()

    def reproduce(self):
        if (np.random.rand() < self.repro_rate):
            return np.random.randint(self.repro_size[0],self.repro_size[1])
        else:
            return 0

class Juvenile(Mole):
    type = 'Juvenile'

    # Half a year to mature
    maturity_age = 2

    # Amount of resource consumed
    resource_consumption = 1 # TODO

    def update(self):
        self.age = self.age + 1

    def mature(self):
        if (self.age > self.maturity_age):
            worker = Worker()
            worker.fitness = self.fitness
            return worker
        else:
            return self

class Worker(Mole):
    type = 'Worker'

    # probability of death 1/500 per day
    death_prob = 0.026

    # amount of resource consumed
    resource_consumption = 2 # TODO

    # rate of resource production
    resource_production_rate = 27 # TODO

    def update(self):
        self.age = self.age + 1
        if (np.random.rand() < self.death_prob):
            self.kill()

    def become_queen(self):
        queen = Queen()
        queen.age = self.age
        queen.fitness = self.fitness
        return queen

    def generate_resource(self):
        return 1 / (1 + np.exp(-self.fitness)) * np.random.poisson(self.resource_production_rate)

class Colony:
    population = []
    resource_stockpile = 0

    def __str__(self):
        s = ''
        s = s + 'resource: ' + str(self.resource_stockpile) + '\n'
        for idx, mole in enumerate(self.population):
            s = s + str(idx) + ' ' + mole.type + ' ' + str(mole.age) + '\n'
        return s

    def initialise_colony(self,resource_stockpile=100,num_workers=0,num_juveniles=0):
        self.population.append(Queen())
        self.resource_stockpile = resource_stockpile
        for i in range(0,num_workers):
            self.population.append(Worker())
        for i in range(0,num_juveniles):
            self.population.append(Juvenile())

    def update_population(self):
        worker_count = 0
        for idx, mole in enumerate(self.population):
            mole.update()
            if (mole.alive):
                if (mole.type == 'Queen'):
                    self.add_pups(mole.reproduce(),mole.fitness)
                elif (mole.type == 'Juvenile'):
                    self.population[idx] = mole.mature()
                elif (mole.type == 'Worker'):
                    self.add_resource((2**(1-worker_count))*mole.generate_resource())
                    worker_count = worker_count + 1

    def add_pups(self, pups, fitness):
        for i in range(0,pups):
            pup = Juvenile()
            pup.fitness = fitness + np.random.normal()
            self.population.append(pup)

    def add_resource(self,resource):
        self.resource_stockpile = self.resource_stockpile + resource

    def consume_resource(self):
        self.population.sort(key = lambda x : x.age)
        self.population.sort(key = custom_sort)
        for mole in self.population:
            if (self.resource_stockpile > mole.resource_consumption):
                self.resource_stockpile = self.resource_stockpile - mole.resource_consumption
            else:
                mole.kill()

    def ensure_queen(self):
        if (not self.has_queen()):
            if (not self.has_worker()):
                self.kill_colony()
            else:
                idx = self.get_worker_index_by_fitness()
                self.population[idx] = self.population[idx].become_queen()

    def has_queen(self):
        if (len([mole for mole in self.population if mole.type == 'Queen']) == 0):
            return False
        else:
            return True

    def has_worker(self):
        if (len([mole for mole in self.population if mole.type == 'Worker']) > 1):
            return True
        else:
            return False

    def get_random_worker_index(self):
        while(True):
            idx = np.random.randint(len(self.population))
            if (self.population[idx].type == 'Worker'):
                return idx

    def get_worker_index_by_fitness(self):
        fitness_matrix = np.matrix([[mole.type for mole in self.population],[mole.fitness for mole in self.population]])
        idx = np.argmin(fitness_matrix[:,1][fitness_matrix[:,0] == 'Worker'])
        return idx

    def get_number_of_workers(self):
        return len([mole for mole in self.population if mole.type == 'Worker'])

    def kill_colony(self):
        for mole in self.population:
            mole.kill()

    def remove_dead(self):
        self.population = [mole for mole in self.population if mole.alive]
