import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from time import sleep

#Constants
CLEAN_UP = -1
IDLE = 0
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

CLEAN = 0
DIRTY = 1
WALL = -1

class Room:
    def __init__(self, rows = 12, columns = 12, walls = True):
        self._rows = rows
        self._columns = columns
        self._size = (rows-1)*(columns-1)
        self._floor = np.zeros((rows, columns))
        self._wallsum = 0
        self._utility = 0
        if walls:
            self.create_walls()
            self._wallsum = rows*2 + (columns - 2) * 2
        self._model_room = self._floor.copy()
        self.make_model_room()
        
        
    def create_walls(self):
        self._floor[0,:] = WALL
        self._floor[-1,:] = WALL
        self._floor[:,0] = WALL
        self._floor[:,-1] = WALL

    def randomize_dirt(self):
        for i in range(1, self._rows - 1):
            for j in range(1, self._columns - 1):
                if np.random.random() < 0.5:
                    self._floor[i,j] = DIRTY

    def make_model_room(self):
        self._model_room = self._floor.copy()
        self._model_room[self._rows - 2, 1:self._columns-2] = RIGHT
        for i in range(1, self._columns - 1):
            if i % 2 == 1:
                self._model_room[2:self._rows - 2, i] = DOWN
                self._model_room[self._rows - 2, i] = RIGHT
            if i % 2 == 0:
                self._model_room[3:self._rows - 2, i] = UP
                self._model_room[2, i-2] = RIGHT
        for i in range(1, self._rows - 1):
            if i % 2 == 1:
                self._model_room[2, i] = DOWN
            if i % 2 == 0:
                self._model_room[self._rows - 2, i] = UP
        self._model_room[2, self._columns -2] = UP
        self._model_room[self._rows - 2, self._columns - 2] = UP
        self._model_room[1,1] = DOWN
        self._model_room[1,2:self._columns - 1] = LEFT
        
    @property
    def floor(self):
        return self._floor
    
    @property
    def percent_dirty(self):
        return (np.sum(self._floor) + self._wallsum)/(self._size - self._wallsum)
    
class Vacuum:
    def __init__(self, room, starting_location = (1,1), agent_type = 'reflex'):
        self._room = room
        self._x = starting_location[0]
        self._y = starting_location[1]
        self._path = [[self._y, self._x]]
        self._utility = 0
        self._time = 0
        self._charge = 100
        self._agent_type = agent_type
        self._last10 = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]


    @property
    def utility(self):
        return self._utility
    @utility.setter
    def utility(self, value):
        self._utility += value

    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, value):
        self._time += value

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, location):
        self._path.append(location)
    
    @property
    def charge(self):
        return self._charge
    @charge.setter
    def charge(self, amount):
        self._charge += amount


    def clean(self):
        if self._agent_type == 'reflex':
            self.reflex_clean()
        if self._agent_type == 'model':
            self.model_clean()
        if self._agent_type == 'goal':
            self.goal_clean()
        if self._agent_type == 'util':
            self.util_clean()

    def scan_dirt(self):
        x = self._x
        y = self._y
        adjacent = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        moves = [UP, DOWN, LEFT, RIGHT]
        dirty_spots = []
        for i in range(4):
            if self._room.floor[adjacent[i]] == DIRTY:
                dirty_spots.append(moves[i])
        return dirty_spots
    def reflex_clean(self):
        if self._room.floor[self._x, self._y] == DIRTY:
            move = CLEAN_UP
            
        else:
            move = self.get_move()
        
        if move == CLEAN_UP:
            self._room.floor[self._x, self._y] = CLEAN
            self.utility = 10
        elif move == UP:
            self._x -= 1
            self.utility = -1
        elif move == DOWN:
            self._x += 1
            self.utility = -1
        elif move == LEFT:
            self._y -= 1
            self.utility = -1
        elif move == RIGHT:
            self._y += 1
            self.utility = -1
        self._path.append([self._y, self._x])
        self.charge = -1
        
    def model_clean(self):
        if self._room.floor[self._x, self._y] == DIRTY:
            move = CLEAN_UP
        else:
            move = self._room._model_room[self._x, self._y]
        if move == CLEAN_UP:
            self._room.floor[self._x, self._y] = CLEAN
            self.utility = 10
        elif move == UP:
            self._x -= 1
            self.utility = -1
        elif move == DOWN:
            self._x += 1
            self.utility = -1
        elif move == LEFT:
            self._y -= 1
            self.utility = -1
        elif move == RIGHT:
            self._y += 1
            self.utility = -1
        self._path.append([self._y, self._x])
        self._last10.append(move)
        self._last10.pop(0)
        self.charge = -1   

    def goal_clean(self):
        if self._room.floor[self._x, self._y] == DIRTY:
            move = CLEAN_UP
        else:
            adjacent_dirt = self.scan_dirt()
            if len(adjacent_dirt) == 0:
                move = self.get_move()
            else:
                move = adjacent_dirt.pop()
        if move == CLEAN_UP:
            self._room.floor[self._x, self._y] = CLEAN
            self.utility = 10
        elif move == UP:
            self._x -= 1
            self.utility = -1
        elif move == DOWN:
            self._x += 1
            self.utility = -1
        elif move == LEFT:
            self._y -= 1
            self.utility = -1
        elif move == RIGHT:
            self._y += 1
            self.utility = -1
        self._path.append([self._y, self._x])
        self._last10.append(move)
        self._last10.pop(0)
        self.charge = -1

    

    def util_clean(self):
        #To be implemented
        return

    def get_move(self):
        possible_moves = [UP, DOWN, LEFT, RIGHT, IDLE]
        if self._x == 1:
            possible_moves.remove(UP)
        if self._x == self._room._rows - 2:
            possible_moves.remove(DOWN)
        if self._y == 1:
            possible_moves.remove(LEFT)
        if self._y == self._room._columns - 2:
            possible_moves.remove(RIGHT)
        return np.random.choice(possible_moves)
    

def update(frame):
    vacuum.clean()
    ax.clear()
    ax.imshow(room.floor, cmap = ListedColormap(['black', 'white', 'brown']), interpolation='nearest')
    ax.plot(*zip(*vacuum.path), marker = None, linestyle = '-', color = 'red', label = 'Vacuum path')
    ax.plot(*zip(vacuum.path[-1]), marker = 'o', linestyle = None, color = 'red', label = 'Vacuum path')
    ax.set_title(f"{kind.capitalize()} Vacuum, Utility: {vacuum.utility} Charge: {vacuum.charge}")
    



kind = input("What kind of vacuum do you want to use? (reflex, model, goal)")
kind = kind.lower()
room = Room()
room.randomize_dirt()
vacuum = Vacuum(room, (1,1), kind)


fig, ax = plt.subplots()
ax.imshow(room.floor, cmap=ListedColormap(['black', 'white', 'brown']), interpolation='nearest')
ax.plot(*zip(*[(y,x) for x,y in vacuum.path]), marker='o', linestyle = '-', color='red', label='Vacuum path')
ax.set_title(f"{kind.capitalize()} Vacuum, Utility: {vacuum.utility} Charge: {vacuum.charge}")
ax.legend()

animation = FuncAnimation(fig, update, frames=range(1, 100), interval=1000)


plt.show()
