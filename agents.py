import mesa

# Agente Robot
class Robot(mesa.Agent):
  def __init__(self, unique_id, pos, model, bgwidth, bgheight):
    super().__init__(unique_id, model)
    self.bgwidth = bgwidth
    self.bgheight = bgheight 
    self.charging = 0 
    self.countdown = 5
    self.new_x = 0 
    self.new_y = 0 
    self.movements = 0 

  def leaveBox(self):
    next_moves = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)

    if self.pos[0] > 0 and self.countdown == 5:
      next_move = (self.pos[0]-1, self.pos[1])
      empty_cell = self.model.grid.is_cell_empty(next_move)
      while empty_cell == False:
        next_move = self.random.choice(next_moves)
        empty_cell = self.model.grid.is_cell_empty(next_move)
      self.model.grid.move_agent(self, next_move)
      self.movements +=1

    elif self.pos[0] == 0 and self.countdown == 5 and self.pos[1] > 1:
      next_move = (self.pos[0], self.pos[1]-1)
      empty_cell = self.model.grid.is_cell_empty(next_move)
      while empty_cell == False:
        next_move = self.random.choice(next_moves)
        empty_cell = self.model.grid.is_cell_empty(next_move)
      self.model.grid.move_agent(self, next_move)
      self.movements +=1

    elif self.pos[0] == 0 and self.pos[1] == 1 and self.countdown == 5:
      for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True, include_center=False):
        if isinstance(neighbor, Shelf) and neighbor.boxes < 5:
          neighbor.boxes += 1
          self.charging = 0
          self.countdown = 5
          self.movements +=1
          break

      if self.charging == 1:
        next_move = (self.pos[0]+1, self.pos[1])
        empty_cell = self.model.grid.is_cell_empty(next_move)
        if empty_cell:
          self.countdown -= 1
          self.model.grid.move_agent(self, next_move)
          self.movements +=1
        else:
          self.countdown -= 1
          return
          
    elif self.countdown < 5:
      for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True, include_center=False):
        if isinstance(neighbor, Shelf) and neighbor.boxes < 5:
          neighbor.boxes += 1
          self.charging = 0
          self.countdown = 5
          self.movements +=1
          break

      if self.charging == 1:
        next_move = (self.pos[0]+1, self.pos[1])
        empty_cell = self.model.grid.is_cell_empty(next_move)
        if empty_cell:
          self.countdown -= 1
          self.model.grid.move_agent(self, next_move)
          self.movements += 1
        else:
          self.countdown -= 1
          return

  def searchBox(self):
    next_moves = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)

    if self.countdown == 5:
      x1 = self.pos[0]
      y1 = self.pos[1]
      next_move = self.random.choice(next_moves)
      empty_cell = self.model.grid.is_cell_empty(next_move)
      while empty_cell == False:
        next_move = self.random.choice(next_moves)
        empty_cell = self.model.grid.is_cell_empty(next_move)
      self.model.grid.move_agent(self, next_move)
      self.movements += 1
      x2 = self.pos[0]
      y2 = self.pos[1]
      self.new_x = x2 - x1
      self.new_y = y2 - y1
      self.countdown -= 1

    elif self.countdown < 5:
      x = self.pos[0]+self.new_x
      y = self.pos[1]+self.new_y
      next_move = (x, y)
      if (x >= 0 and x < self.bgwidth) and (y >= 0 and y < self.bgheight):
        empty_cell = self.model.grid.is_cell_empty(next_move)
        while empty_cell == False:
          self.countdown = 5
          next_move = self.random.choice(next_moves)
          empty_cell = self.model.grid.is_cell_empty(next_move)
        self.model.grid.move_agent(self, next_move)
        self.movements +=1
        if self.countdown < 5 and self.countdown > 0:
          self.countdown -= 1
        if self.countdown == 0:
          self.countdown = 5
      else:
        next_move = self.random.choice(next_moves)
        empty_cell = self.model.grid.is_cell_empty(next_move)
        while empty_cell == False:
          next_move = self.random.choice(next_moves)
          empty_cell = self.model.grid.is_cell_empty(next_move)
        self.model.grid.move_agent(self, next_move)
        self.movements +=1
        self.countdown = 5

    self.chargeBox()

  def chargeBox(self):

    for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True, include_center=False):
      if isinstance(neighbor, Box):
        cont = 0
        for box_neighbor in self.model.grid.iter_neighbors(neighbor.pos, moore=True, include_center=False, radius=1):
          if isinstance(box_neighbor, Robot):
            cont += 1
        if cont == 1:
          self.charging = 1
          self.countdown = 5
          self.model.kill_agents.append(neighbor)
          self.movements +=1
          break
          
        elif cont > 1:
          next_moves = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
          next_move = self.random.choice(next_moves)
          empty_cell = self.model.grid.is_cell_empty(next_move)
          while empty_cell == False:
            next_move = self.random.choice(next_moves)
            empty_cell = self.model.grid.is_cell_empty(next_move)
          self.model.grid.move_agent(self, next_move)
          self.movements +=1
          
  
  def advance(self):
    if self.charging == 0:
      self.searchBox()
    elif self.charging == 1:
      self.leaveBox()
    
# Agente Box
class Box(mesa.Agent):
  def __init__(self, unique_id, pos, model):
    super().__init__(unique_id, model)
    self.pos = pos

# Agente Shelf
class Shelf(mesa.Agent):
  def __init__(self, unique_id, pos, model):
    super().__init__(unique_id, model)
    self.pos = pos
    self.boxes = 0 # Miembro boxes: Es la cantidad actual de cajas en el estante

# Agente Obstaculo
class Obstacle(mesa.Agent):
  def __init__(self, unique_id, pos, model):
    super().__init__(unique_id, model)
    self.pos = pos