import numpy as np
from a_star import bmd

#Class to generate, update* and visualize map*
class MapObj():
    def __init__(self, width, length, goal_count=1, mountain_count=-1, mountain_radius=-1, water_count = 1, water_radius=-1):

        #Set all object variables
        self.width = width
        self.length = length
        self.goal_count = goal_count
        self.water_cost = 7
        self.climb_cost = 8
        self.mountain_cost = 9
        self.water_count = water_count

        if mountain_count < 0:
            self.mountain_count = np.random.randint(int(min([self.width, self.length]) / 2)) + 1
        else:
            self.mountain_count = mountain_count

        if mountain_radius < 0:
            self.mountain_radius = np.random.randint(int(min([self.width, self.length]) / 3)) +3
        else:
            self.mountain_radius = mountain_radius

        if water_radius < 0:
            self.water_radius = np.random.randint(int(min([self.width, self.length]) / 2)) +2
        else:
            self.water_radius = water_radius
        
        #Initialize terrain lists
        self.mountains = []
        self.waters = []

        #Key locations
        self.goals = []
        self.start = None

        #Generating map
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

    #Generate mountains
    def generate_map_mountains(self):
        print("Generating map : Mountains... (" + str(self.mountain_count) + ")")

        #Generates as many mountains as mountain_count
        for i in range(0, self.mountain_count):

            #Loops until a single mountain was successfully generated
            while len(self.mountains) < i+1:

                #Uses numpy.random.randint to get a random cordinate within the map
                cord = (np.random.randint(self.width), np.random.randint(self.length))

                #Checks if cordinate is not mountain
                if self.map[cord[0]][cord[1]] < self.mountain_cost:

                    #Cordinate is added to list of mountain
                    self.mountains.append(cord)
        
        #Add all mountain centers to current_list
        current_list = self.mountains

        #Growing mountains
        #Search with depth = mountain_radius, and set cordinates to mountain
        for i in range(0, self.mountain_radius):

            #List to add children of cordinates in current list
            new_list = []

            #For every cordinate in current_list
            for t in current_list:

                #Set cordinate as mountain
                self.map[t[0]][t[1]] = self.mountain_cost

                #Find every child of cordinate
                for y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:

                    #Check if child is inside map (if it exist)
                    if t[0]+y[0] < self.width and t[0]+y[0] >= 0 and t[1]+y[1] < self.length and t[1]+y[1] >= 0:

                        #Check if child is not mountain
                        if self.map[t[0]+y[0]][t[1]+y[1]] < self.mountain_cost:

                            #Add child to new_list
                            new_list.append((t[0]+y[0],t[1]+y[1]))

            #Finished processing cordinates in current_list, sets new_list as current_list
            current_list = new_list
        
        #Fill cordinates surrounded by mountains
        self.generate_map_fill_surrounded_by_mountains(current_list)
    
    #Fill cordinates surrounded by mountains
    def generate_map_fill_surrounded_by_mountains(self, current_list):
        print("Generating map : Filling gaps...")

        #For every cordinate around mountains
        for i in current_list:

            #Check if cordinate is not mountain
            if self.map[i[0]][i[1]] < self.mountain_cost:

                #Variable to count surrounding mountains and edges
                n = 0

                #For every neighbouring cordinate
                for y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:

                    #Check if inside map
                    if i[0]+y[0] < self.width and i[0]+y[0] >= 0 and i[1]+y[1] < self.length and i[1]+y[1] >= 0:

                        #Check if cordinate is mountain
                        if self.map[i[0]+y[0]][i[1]+y[1]] == self.mountain_cost:

                            #_Mountain_/edge count +1
                            n += 1
                    else:

                        #Mountain/_edge_ count +1
                        n+=1

                #Check if counted 3 or more mountains/edges
                if n > 2:

                    #Sets cordinate to mountain
                    self.map[i[0]][i[1]] = self.mountain_cost
    
    #Generate water
    def generate_map_water(self):
        print("Generating map : Water...")

        #Generates as many waters as water_count
        for i in range(0, self.water_count):

            #Loops until a single water was successfully generated
            while len(self.waters) < i+1:

                #Uses numpy.random.randint to get a random cordinate within the map
                cord = (np.random.randint(self.width), np.random.randint(self.length))

                #Checks if cordinate is less than water in cost
                if self.map[cord[0]][cord[1]] < self.water_cost:

                    #Cordinate is added to list of water centers
                    self.waters.append(cord)

        #Add all mountain centers to current_list
        current_list = self.waters

        #Growing waters
        #Search with depth = water_radius, and set nodes/cordinates to water
        for i in range(0, self.water_radius):

             #List to add children of cordinates in current list
            new_list = []

            #For every cordinate in current_list
            for t in current_list:

                #Set cordinate as water
                self.map[t[0]][t[1]] = self.water_cost

                #Find every child of cordinate
                for y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:

                    #Check if child is inside map (if it exist)
                    if t[0]+y[0] < self.width and t[0]+y[0] >= 0 and t[1]+y[1] < self.length and t[1]+y[1] >= 0:

                        #Checks if cordinate is less than water in cost
                        if self.map[t[0]+y[0]][t[1]+y[1]] < self.water_cost:

                            #Add child to new_list
                            new_list.append((t[0]+y[0],t[1]+y[1]))
            
            #Finished processing cordinates in current_list, sets new_list as current_list
            current_list = new_list
    
    #Set start location
    def generate_start_location(self):
        print("Generating map : Start Location...")

        #Loops until a start cordinate is found
        while self.start is None:

            #Uses numpy.random.randint to get a random cordinate within the map
            cord = (np.random.randint(self.width), np.random.randint(self.length))

            #Check if cordinate is not mountain
            if self.map[cord[0]][cord[1]] < self.mountain_cost:

                #Cordinate is set as start cordinate
                self.start = cord
    
    #Generate goal location(s)
    def generate_goal_locations(self):
        print("Generating map : Goal Location(s)...")

        #Sets a minimum length between start location and goals
        min_length = min([self.width, self.length])

        #Generates as many goals as goal_count
        for i in range(0, self.goal_count):

            #Loops until a single goal was successfully generated
            while len(self.goals) < i+1:

                #Uses numpy.random.randint to get a random cordinate within the map
                cord = (np.random.randint(self.width), np.random.randint(self.length))

                #Checks if cordinate is not mountain
                if self.map[cord[0]][cord[1]] < 9:

                    #Checks if cordinate is far enough from start
                    if bmd(self.start, [cord]) > min_length:
                        #Cordinate is added to list of goals
                        self.goals.append(cord)

                    #Cordinate was to close to start
                    else:
                        #Lowering required distance between start and goal
                        min_length -= 1

    #Returns map as numpy 2d list
    def get_map(self):
        return self.map

    #Returns start cord and list of goal cords
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