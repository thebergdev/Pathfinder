import numpy as np
from a_star import bmd

class MapObj():
    def __init__(self, width, length, goal_count=1,  water_count=1, obs_count=-1, obs_radius=-1, water_cost=7, water_radius=-1):
        self.width = width
        self.length = length
        self.goal_count = goal_count
        self.water_cost = water_cost
        self.obs_cost = 9
        self.climb_cost = 8
        self.water_count = water_count

        if obs_count < 0:
            self.obs_count = np.random.randint(int(min([self.width, self.length]) / 2)) + 1
        else:
            self.obs_count = obs_count

        if obs_radius < 0:
            self.obs_radius = np.random.randint(int(min([self.width, self.length]) / 3)) +3
        else:
            self.obs_radius = obs_radius

        if water_radius < 0:
            self.water_radius = np.random.randint(int(min([self.width, self.length]) / 2)) +2
        else:
            self.water_radius = water_radius

        self.obs = []
        self.goals = []
        self.start = None
        self.water = []

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
        print("Generating map : Obsticles... (" + str(self.obs_count) + ")")

        #Generate obsticle center locations
        for i in range(0, self.obs_count):
            while len(self.obs) < i+1:
                cord = (np.random.randint(self.width), np.random.randint(self.length))
                if self.map[cord[0]][cord[1]] < self.obs_cost:
                    self.obs.append(cord)

                print("Generating map : Obsticle " + str(i) + " center cord", cord)
        
        print("Generating map : Obsticle radius", self.obs_radius)

        #Growing obsicles
        current_list = self.obs
        print(current_list)
        for i in range(0, self.obs_radius):
            new_list = []
            for t in current_list:
                self.map[t[0]][t[1]] = self.obs_cost
                for y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                        if t[0]+y[0] < self.width and t[0]+y[0] >= 0 and t[1]+y[1] < self.length and t[1]+y[1] >= 0:
                            if self.map[t[0]+y[0]][t[1]+y[1]] < 8 and self.map[t[0]+y[0]][t[1]+y[1]] != self.obs_cost:
                                new_list.append((t[0]+y[0],t[1]+y[1]))
            current_list = new_list
        
        #Fill single holes in obsticles
        print("Generating map : Filling holes...")
        for i in current_list:
            if self.map[i[0]][i[1]] < self.obs_cost:
                    nt = [0, 0, 0, 0]
                    n = 0
                    for y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                        if i[0]+y[0] < self.width and i[0]+y[0] >= 0 and i[1]+y[1] < self.length and i[1]+y[1] >= 0:
                            if self.map[i[0]+y[0]][i[1]+y[1]] == self.obs_cost:
                                nt[n] = n +1
                        else:
                            nt[n] = 10
                        n += 1
                    ns = sum(nt)
                    #print(nt, ns, np.count_nonzero(nt))
                    if np.count_nonzero(nt) > 3:
                        print("Filled", i)
                        self.map[i[0]][i[1]] = self.obs_cost
                    else:
                        if ns % 2 == 0 and np.count_nonzero(nt) == 2 and ns <= 10:
                            print("Mountain pass at", i)
                            print(nt, ns)
                            self.map[i[0]][i[1]] = self.climb_cost
    
    #Generate water
    def generate_map_water(self):
        print("Generating map : Water...")

        for i in range(0, self.water_count):
            while len(self.water) < i+1:
                cord = (np.random.randint(self.width), np.random.randint(self.length))
                if self.map[cord[0]][cord[1]] < self.water_cost:
                    self.water.append(cord)

                print("Generating map : Water " + str(i) + "center cord", cord)
                
        print("Generating map : Water radius", self.water_radius)

        for w in self.water:
            current_list = [w]
            for i in range(0, self.water_radius):
                new_list = []
                for t in current_list:
                    self.map[t[0]][t[1]] = self.water_cost
                    for y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                            if t[0]+y[0] < self.width and t[0]+y[0] >= 0 and t[1]+y[1] < self.length and t[1]+y[1] >= 0:
                                if self.map[t[0]+y[0]][t[1]+y[1]] < 8 and self.map[t[0]+y[0]][t[1]+y[1]] != self.water_cost:
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

class MapSearchObjOrder():
    def __init__(self, map, node_list, node_path):
        self.map = map
        self.node_list = node_list
        self.node_path = node_path
        
        self.generate_map()
    
    def generate_map(self):
        i = 0
        for node in self.node_list:
            self.map[node.cord[0]][node.cord[1]] = i
            i += 1

    def get_map(self):
        return self.map

class MapSearchObjG():
    def __init__(self, map, node_list, node_path):
        self.map = map
        self.node_list = node_list
        self.node_path = node_path
        
        self.generate_map()
    
    def generate_map(self):
        for node in self.node_list:
            self.map[node.cord[0]][node.cord[1]] = node.g
            
    def get_map(self):
        return self.map