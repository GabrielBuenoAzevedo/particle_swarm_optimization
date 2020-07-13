import random
import numpy as np

np.random.seed(41)

class Particle:
  #Constructor. Remember to rewrite this 
  def __init__(self, coord_max = [], coord_min = [], 
                min_vel = [], max_vel = [], fitness_func = None,
                initial_vel = [], coordinates = [],
                cog_const = 2.05, soc_const = 2.05):
    self.coord_max = coord_max
    self.coord_min = coord_min
    self.min_vel = min_vel
    self.max_vel = max_vel
    self.fitness_func = fitness_func
    self.velocities = initial_vel
    self.coordinates = coordinates
    self.cog_const = 4.1 - soc_const
    self.soc_const = 4.1 - cog_const
    #Checks if given values are alright.
    if len(self.coord_max) < 1:
      raise ValueError('coord_max must be defined.')
    if len(self.coord_min) < 1:
      raise ValueError('coord_min must be defined.')
    if len(self.coord_max) != len(self.coord_min):
      raise ValueError('coord_max and coord_min must have the same length.')
    if len(self.min_vel) < 1:
      raise ValueError('min_vel must be defined.')
    if len(self.max_vel) < 1:
      raise ValueError('max_vel must be defined.')
    if len(self.min_vel) != len(self.max_vel):
      raise ValueError('min_vel and max_vel must have the same length.')
    if len(self.min_vel) != len(self.coord_min):
      raise ValueError('min_vel and coord_min must have the same length.')
    if fitness_func is None or not hasattr(fitness_func, '__call__'):
      raise ValueError('fitness_func must be callable.')
    if len(self.velocities) > 0 and len(self.velocities) != len(self.min_vel):
      raise ValueError('velocities and min_vel must have the same length.')
    if len(self.coordinates) > 0 and len(self.coordinates) != len(self.coord_min):
      raise ValueError('coordinates and coord_min must have the same length.')
    #If some values weren't declared by the user, declares them
    if len(self.velocities) == 0:
      self.velocities = np.array([ random.uniform(min_v, max_v) for min_v, max_v in zip(self.min_vel, self.max_vel) ])
    if len(self.coordinates) == 0:
      self.coordinates = np.array([ random.uniform(min_c, max_c) for min_c, max_c in zip(self.coord_min, self.coord_max) ])
    #Best coordinate and best fitness up until now are the current ones
    self.best_coord = self.coordinates
    self.best_fitness = self.fitness_func(self.coordinates)

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
    soc_dist = best_neighbor_coord - self.coordinates
    cog_dist = self.best_coord - self.coordinates
    random_soc = np.random.uniform(0, self.soc_const)
    random_cog = np.random.uniform(0, self.cog_const)
    new_vel = velocity + (soc_dist * random_soc) + (cog_dist * random_cog)
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
    self.fitness = new_fitness
    if new_fitness > self.best_fitness:
      self.best_fitness = new_fitness
      self.best_coord = new_coord

    
  #Update neighborhood best
  def updateNeighborhoodValues(self):
    best_coord = self.best_coord
    best_fitness = self.best_fitness
    for neighbor in self.neighborhood:
      if neighbor.best_fitness > best_fitness:
        best_fitness = neighbor.best_fitness
        best_coord = neighbor.best_coord
    self.neighborhood_best_coord = best_coord


