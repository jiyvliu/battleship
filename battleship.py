# %%
import numpy as np
import random as r
import string

# %%
def coord_to_index(coord):
  coord = coord.strip()
  letter_to_number = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
  return (letter_to_number[coord[0]], int(coord[1:]) - 1)

def index_to_coord(index):
  number_to_letter = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}
  return number_to_letter[index[0]] + str(index[1] + 1)

class battleship:
  def __init__(self):
    self.hits = np.full((10, 10), "-") # -:blank H:hit M:miss
    self.prob = np.full((10, 10), 0)
    self.carrier = "afloat"
    self.battleship = "afloat"
    self.cruiser = "afloat"
    self.sub = "afloat"
    self.destroyer = "afloat"

  def visualize(self):
    print('   1  2  3  4  5  6  7  8  9  10')
    for i in range(0, 10):
      letter = string.ascii_uppercase[i]
      print(letter + '  ' + '  '.join(self.hits[i,:].tolist()))

  def visualize_prob(self):
    print('   1  2  3  4  5  6  7  8  9  10')
    for i in range(0, 10):
      letter = string.ascii_uppercase[i]
      # funky map function for when # of orientations is 2 digit number
      print(letter + '  ' + \
            ''.join(map(lambda x: str(x) + ' ' if x > 9 else str(x) + '  ', \
                        self.prob[i,:].tolist())))

  def add_hit(self, coord):
    index = coord_to_index(coord)
    self.hits[index[0], index[1]] = "H"

  def add_miss(self, coord):
    index = coord_to_index(coord)
    self.hits[index[0], index[1]] = "M"

  def sink(self, ship):
    ship = str(ship).strip().lower()
    if ship == "carrier":
      self.carrier = "sunk"
    if ship == "battleship":
      self.battleship = "sunk"
    if ship == "cruiser":
      self.cruiser = "sunk"
    if ship == "sub":
      self.sub = "sunk"
    if ship == "destroyer":
      self.ship = "sunk"

  def remove(self, coord):
    index = coord_to_index(coord)
    self.hits[index[0], index[1]] = "-"

  def give_max_coord(self):
    max_indices = np.where(self.prob == np.max(self.prob))
    max_indices = list(zip(max_indices[0], max_indices[1]))
    return r.choice(max_indices)

  def clear_prob(self):
    self.prob = np.full((10, 10), 0)

  def calculate_prob(self, boat_len):
    # calculates the # of orientations a boat of 
    # length boat_len can fit at every cell
    for row in range(10):
      for col in range(10):
        if row + boat_len <= 10: #bottom
          boat_loc = self.hits[row:row + boat_len, col]
          boat_proc = self.prob[row:row + boat_len, col]
          if all(cell == '-' for cell in boat_loc):
            for i in range(len(boat_proc)):
              boat_proc[i] += 1

        if col + boat_len <= 10: #right
          boat_loc = self.hits[row, col:col + boat_len]
          boat_proc = self.prob[row, col:col + boat_len]
          if all(cell == '-' for cell in boat_loc):
            for i in range(len(boat_proc)):
              boat_proc[i] += 1
            

# %%
# initialize
board = battleship()

# begin game state tracking
while(True):
  board.clear_prob()
  if board.carrier == "afloat":
    board.calculate_prob(5)
  if board.battleship == "afloat":
    board.calculate_prob(4)
  if board.cruiser == "afloat":
    board.calculate_prob(3)
  if board.sub == "afloat":
    board.calculate_prob(3)
  if board.destroyer == "afloat":
    board.calculate_prob(2)
    
  #board.visualize_prob()
  board.visualize()
  print("Recommended coordinates: " + index_to_coord(board.give_max_coord()))
  print('-------------------------------------------')

  instruct = input("H [coord], M [coord], sunk [ship], remove [coord]: ")
  try:
    instruction = instruct.split(' ')[0]
    parameter = instruct.split(' ')[1]

    if instruction == "H":
      board.add_hit(parameter)
    if instruction == "M":
      board.add_miss(parameter)
    if instruction == "sunk":
      board.sink(parameter)
    if instruction == "remove":
      board.remove(parameter)
  except:
    print('Wrong instruction input!')
