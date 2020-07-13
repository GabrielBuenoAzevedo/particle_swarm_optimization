import random
import numpy as np

np.random.seed(41)

class Particle:
  #Constructor. Remember to rewrite this 
  def __init__(self, obj):
    if 'coord_max' in obj:
      coord_max = obj['coord_max']
    else:
      coord_max = None
    
    if 'coord_min' in obj:
      coord_min = obj['coord_min']
    else:
      coord_min = None

    if 'coordinates' in obj:
      coordinates = np.array(obj['coordinates'])
      dimensions = len(obj['coordinates'])
    elif 'dimensions' in obj:
      dimensions = obj['dimensions']
      if coord_max is None:
        coordinates = np.random.uniform(size=dimensions)
      elif len(coord_max) == dimensions:
        coordinates = np.array([ random.uniform(limit_min, limit_max) for (limit_min, limit_max) in zip(coord_min,coord_max) ])
      else:
        print("Error: coord_limits size must be the same number of dimensions") ##LEMBRAR DE DAR THROW NO ERROR
        return
    else:
      print("Error: Dimensions or coordinates need to be specified.") ##Lembrar de dar throw no error
      return

    if 'max_vel' in obj:
      if len(obj['max_vel']) == dimensions:
        max_vel = obj['max_vel']
      else:
        print("Velocities limit size must match the number of coordinates")
        return
    else:
      print('Velocities limits must be specified.')
      return

    if 'min_vel' in obj:
      if len(obj['min_vel']) == dimensions:
        min_vel = obj['min_vel']
      else:
        print("Velocities limit size must match the number of coordinates")
        return
    else:
      print('Velocities limits must be specified.')
      return

    if 'initial_velocities' in obj:
      if len(obj['initial_velocities']) == dimensions:
        vel = obj['initial_velocities']
      else:
        print("Velocities limit size must match the number of coordinates")
    else:
      vel = np.array([ random.uniform(min_limit, max_limit) for min_limit, max_limit in zip(min_vel, max_vel) ])

    if 'fitness_func' in obj:
      fitness_func = obj['fitness_func']
    else :
      print('The particle needs a fitness function')
      return

    if 'cog_const' in obj:
      cog_const = obj['cog_const']
    else:
      cog_const = 2.05

    self.coord_min = coord_min
    self.coord_max = coord_max
    self.coordinates = coordinates
    self.dimensions = dimensions
    self.velocities = vel
    self.fitness_func = fitness_func
    self.max_vel = max_vel
    self.min_vel = min_vel
    self.cog_const = cog_const
    self.soc_const = 4.1 - cog_const
    self.best_coord = coordinates
    self.best_fitness = fitness_func(coordinates)

  #Set the neighborhood of the particle
  def setNeighborhood(self, neighborhood):
    self.neighborhood = neighborhood
    best_fitness = float("-Inf")
    best_coord = None
    for neighbor in neighborhood:
      if neighbor.best_fitness > best_fitness:
        best_fitness = neighbor.best_fitness
        best_coord = neighbor.best_coord
    if best_fitness < self.best_fitness:  ## verficiar isso depois
      best_coord = self.coordinates
    self.neighborhood_best_coord = best_coord
    
  #Show all variables contained within the particle
  def showSelf(self):
    selfVariables = vars(self)
    print('\n'.join("%s: %s" % item for item in selfVariables.items()))

  #Show neighbor values
  def showNeighbors(self):
    for index, neighbor in enumerate(self.neighborhood):
      print('-----------------------------------------')
      print('Neighbor {}'.format(index))
      print('Coordinates', neighbor.best_coord)
      print('Best fitness: ', neighbor.best_fitness)
  
  #Update particle velocity
  def updateVelocity(self):
    velocity = self.velocities
    min_vel = self.min_vel
    max_vel = self.max_vel
    best_neighbor_coord = self.neighborhood_best_coord
    soc_dist = self.coordinates - best_neighbor_coord
    cog_dist = self.coordinates - self.best_coord
    random_soc = np.random.uniform(0, self.soc_const)
    random_cog = np.random.uniform(0, self.cog_const)
    new_vel = velocity + (soc_dist * random_soc) + (cog_dist + random_cog)
    new_vel = np.maximum(new_vel, min_vel)
    new_vel = np.minimum(new_vel, max_vel)
    self.velocities = new_vel

  #Update particle coordinates
  def updateCoordinate(self):
    self.updateVelocity()
    coordinate = self.coordinates
    velocities = self.velocities
    new_coord = coordinate + velocities
    new_coord = np.maximum(new_coord, self.coord_min)
    new_coord = np.minimum(new_coord, self.coord_max)
    new_fitness = self.fitness_func(new_coord)
    self.coordinates = new_coord
    if new_fitness > self.best_fitness:
      self.best_fitness = new_fitness
      self.best_coord = coordinate
    


