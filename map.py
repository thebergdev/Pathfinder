import numpy as np
from a_star import bmd

class Map_Obj():
    def __init__(self, width, length, goal_count=1, obs=0.4, obs_count=-1, obs_radius=-1, water_count=1, water_cost=7, water_radius=-1):
        self.width = width
        self.length = length
        self.goal_count = goal_count
        self.water_cost = water_cost
        self.obs = obs
        self.water_count = water_count

        if obs_count < 0:
            self.count = np.random.randint(3)
        else:
            self.obs_count = obs_count

        if obs_radius < 0:
            self.obs_radius = np.random.randint(int(min([self.width, self.length]) / 3))
        else:
            self.obs_radius = obs_radius

        if water_radius < 0:
            self.water_radius = np.random.randint(int(min([self.width, self.length]) / 2))
        else:
            self.water_radius = water_radius

        self.goals = []
        self.start = None
        self.water = None

        self.generate_map()

    

    #Generate map
    def generate_map(self):
        print("Generating map : Initializing...")

        #Initializing empty map
        self.map = np.ones((self.width, self.length))
        
        #Generate mountains
        self.generate_map_mountains()
        
        #Generate water
        self.generate_map_water()
        
        #Generate start location
        self.generate_start_location()

        #Generate goal location(s)
        self.generate_goal_locations()
     
    #Generate obsticles
    def generate_map_mountains(self):
        print("Generating map : Obsticles...")
        for i in range(0, int(self.width * self.length * self.obs)):
            cord = (np.random.randint(self.width), np.random.randint(self.length))
            self.map[cord[0]][cord[1]] = 9  

        #Fill single holes in obsticles
        print("Generating map : Filling holes...")
        for i in range(0, self.width):
            for t in range(0, self.length):
                if self.map[i][t] < 9:
                    n = 0
                    for y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                        if i+y[0] < self.width and i+y[0] >= 0 and t+y[1] < self.length and t+y[1] >= 0:
                            if self.map[i+y[0]][t+y[1]] == 9:
                                n += 1
                        else:
                            n += 1
                    if n == 4:
                        self.map[i][t] = 9
    
    #Generate water
    def generate_map_water(self):
        print("Generating map : Water...")

        while self.water is None:
            cord = (np.random.randint(self.width), np.random.randint(self.length))
            if self.map[cord[0]][cord[1]] < 9:
                self.water = cord

                print("Generating map : Water center cord", cord)
        print("Generating map : Water radius", self.water_radius)

        current_list = [self.water]
        for i in range(0, self.water_radius):
            new_list = []
            for t in current_list:
                self.map[t[0]][t[1]] = self.water_cost
                for y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                        if t[0]+y[0] < self.width and t[0]+y[0] >= 0 and t[1]+y[1] < self.length and t[1]+y[1] >= 0:
                            if self.map[t[0]+y[0]][t[1]+y[1]] < 8:
                                new_list.append((t[0]+y[0],t[1]+y[1]))
            current_list = new_list
    
    #Set start location
    def generate_start_location(self):
        print("Generating map : Start Location...")
        while self.start is None:
            cord = (np.random.randint(self.width), np.random.randint(self.length))
            if self.map[cord[0]][cord[1]] < 9:
                self.start = cord
                print("Generating map : Start Location cord", cord)
    
    #Generate goal location(s)
    def generate_goal_locations(self):
        print("Generating map : Goal Locations...")

        min_length = min([self.width, self.length])
        for i in range(0, self.goal_count):
            while len(self.goals) < i+1:
                cord = (np.random.randint(self.width), np.random.randint(self.length))
                if self.map[cord[0]][cord[1]] < 9:
                    if bmd(self.start, [cord]) > min_length:
                        self.goals.append(cord)
                    else:
                        min_length -= 1

    def get_map(self):
        return self.map

    def get_key_loc(self):
        return self.start, self.goals
