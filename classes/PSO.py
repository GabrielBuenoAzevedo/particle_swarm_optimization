from Particle import Particle

class PSO:
  #Constructor
  def __init__(self, pop_size = 0, search_space = [], 
               vel_range = [], fitness_func = None):
    self.population_size = pop_size
    self.search_space = search_space
    self.vel_range = vel_range
    self.fitness_func = fitness_func
    #Check if the given values are right
    if self.population_size < 1:
      raise ValueError('Population size must be at least 1.')
    if len(self.search_space) < 1:
      raise ValueError('Search Space must be defined.')
    for coordinate in self.search_space:
      if len(coordinate) != 2:
        raise ValueError('Each search space dimension must have a minimun and a maximum.')
    if len(self.vel_range) < 1:
      raise ValueError('Velocities range must be especified.')
    for v_range in self.vel_range:
      if len(v_range) != 2:
        raise ValueError('Each velocity range must have a minimun and a maximum.')
    if len(self.search_space) != len(self.vel_range):
      raise ValueError('Velocities and coordinates sizes must be the same.')
    if self.fitness_func is None or not hasattr(self.fitness_func, '__call__'):
      raise ValueError('fitness_func must be callable.')

  #Create particles and set their neighborhood as the closest positions in a circular list.
  def createPopulation(self):
    population = []
    max_coords = []
    min_coords = []
    max_velocities = []
    min_velocities = []
    for velocity in self.vel_range:
      min_velocities.append(velocity[0])
      max_velocities.append(velocity[1])
    for coord in self.search_space:
      min_coords.append(coord[0])
      max_coords.append(coord[1])
    for i in range(0,self.population_size):
      population.append(
        Particle(coord_max = max_coords, coord_min = min_coords, 
                min_vel = min_velocities, max_vel = max_velocities, 
                fitness_func = self.fitness_func)
      )
    for index, particle in enumerate(population):
      pos_before = index - 1
      pos_after = (index + 1)%self.population_size
      particle.setNeighborhood( [ population[pos_before] , population[pos_after] ])
    self.population = population
    
  #Show every particle in the population
  def showPopulation(self):
    for particle in self.population:
      print('--------------------------------')
      particle.showSelf()
      print('--------------------------------')
  
  def runAlgorithm(self, num_iterations):
    for i in range(0, num_iterations):
      for index, particle in enumerate(self.population):
        particle.updateCoordinate()
      for particle in self.population:
        particle.updateNeighborhoodValues()
      self.population[0].showSelf()
      # print(self.population[0].velocities, self.population[0].coordinates, self.population[0].neighborhood_best_coord)
      print('\n')


#Testing code

def fitness(coord):
  return coord.sum()

pso = PSO(pop_size=4, 
          search_space=[
            [1, 5],
            [1, 5],
            [1, 5],
            [1, 5],
            [1, 5]
          ], vel_range=[
            [0, 0.4],
            [0, 0.4],
            [-1, 0.25],
            [0, 0.4],
            [0, 0.2],
          ], fitness_func=fitness)

pso.createPopulation()
pso.showPopulation()
print('\n\n\n')
pso.runAlgorithm(30)