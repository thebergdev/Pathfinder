import numpy as np
from a_star import bmd

class Map_Obj():
    def __init__(self, width, length, goal_count=1, obs=0.4, water_count=1):
        self.width = width
        self.length = length
        self.goal_count = goal_count
        self.obs = obs
        self.water_count = water_count
        self.goals = []
        self.start = None
        self.water = None
        self.generate_map()
    
    #Generate map
    def generate_map(self):
        print("Generating map")
        map = np.ones((self.width, self.length))

        #Finding min length of width and length
        min_length = self.width
        if self.length < self.width:
            min_length = self.length

        #Generate obsticles
        print("Generating map : Obsticles")
        for i in range(0, int(self.width * self.length * self.obs)):
            cord = (np.random.randint(self.width), np.random.randint(self.length))
            map[cord[0]][cord[1]] = 9    
        
        #Fill single holes in obsticles
        print("Generating map : Filling holes")
        for i in range(0, self.width):
            for t in range(0, self.length):
                if map[i][t] < 9:
                    n = 0
                    for y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                        if i+y[0] < self.width and i+y[0] >= 0 and t+y[1] < self.length and t+y[1] >= 0:
                            if map[i+y[0]][t+y[1]] == 9:
                                n += 1
                        else:
                            n += 1
                    if n == 4:
                        map[i][t] = 9
        
        #Generate water
        print("Generating map : Water")
        water_cost = 7
        water_radius = np.random.randint(int(min_length / 3))
        while self.water is None:
            cord = (np.random.randint(self.width), np.random.randint(self.length))
            if map[cord[0]][cord[1]] < 9:
                self.water = cord
                print("Water center cord: ", cord)
        #Width first search turn every non obsitcle to water with radius water_radius <---
        

        #Generate start location
        print("Generating map : Start Location")
        while self.start is None:
            cord = (np.random.randint(self.width), np.random.randint(self.length))
            if map[cord[0]][cord[1]] < 9:
                self.start = cord
                print("Start cord: ", cord)

        #Generate goal location(s)
        print("Generating map : Goal Locations")
        for i in range(0, self.goal_count):
            while len(self.goals) < i+1:
                cord = (np.random.randint(self.width), np.random.randint(self.length))
                if map[cord[0]][cord[1]] < 9:
                    if bmd(self.start, [cord]) > min_length:
                        self.goals.append(cord)
                    else:
                        min_length -= 1
                        
        self.map = map

        #Sets start and goal(s) to 0 to visualize key locations on map
        map[self.start[0]][self.start[1]] = 0
        #for goal in self.goals:
        #    map[goal[0]][goal[1]] = 0
            

    def get_map(self):
        return self.map

    def get_key_loc(self):
        return self.start, self.goals
