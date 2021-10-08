import numpy as np
from a_star import a_star, bmd, Node

#Class to generate and visualize map*
class MapObj():
    def __init__(self, width, length, goal_count=1, mountain_count=-1, mountain_radius=-1, water_count = 1, water_radius=-1):

        #Set all object variables
        self.width = width
        self.length = length
        self.goal_count = goal_count
        self.path_value = 10
        self.no_path_value = 11
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
        self.map = None
        self.generate_map()

        #Initializing map layers
        self.map_with_path = []
        self.map_with_order = []
        self.map_with_f = []

        #Initializing A_star information array
        #cost, path, node_path, node_list, , node_discover_list
        self.a_star = []



    

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
    
    #Returns map with path
    def get_map_with_path(self):

        #Check if map_with_path is not set
        if self.map_with_path == []:

            #Fill A_star information array
            for i in a_star(self.map, self.start, self.goals):
                self.a_star.append(i)
            
            #Copy map
            temp = np.copy(self.map)

            #Check if path was found
            if self.a_star[0] > -1:

                #For every cordinate that is a part of the path
                for i in self.a_star[1]:

                    #Set value to path_value
                    temp[i[0]][i[1]] = self.path_value
            
            else:
                #Mark start
                temp[self.start[0]][self.start[1]] = self.no_path_value
            
            #Set temp as map_with_path
            self.map_with_path = temp

        #Return map with path
        return self.map_with_path

    #Returns map with node order
    def get_map_with_order(self, index=0):

        #Make sure index is max 1
        if index > 1:
            index = 1
                
        #Check if map_with_order is not set
        if self.map_with_order == []:

            #Initialize 2d array with zeroes
            temp = np.zeros((self.width, self.length))

            #Node order counter
            i = 1

            #For every node in node_history
            for n in self.a_star[3+index]:

                #Check that node is not yet visited/discorvered
                if temp[n.cord[0]][n.cord[1]] == 0:
    
                    #Node's cordinate is set to i
                    temp[n.cord[0]][n.cord[1]] = i

                    #i is incremented
                    i += 1

            #Set temp as map_with_order
            self.map_with_order = temp
        
        #Return map with order
        return self.map_with_order
    
    #Returns map with node f
    def get_map_with_f(self, index=0):

        #Make sure index is max 1
        if index > 1:
            index = 1

        #Check if f is not set
        if self.map_with_f == []:

            #Initialize 2d array with zeroes
            temp = np.zeros((self.width, self.length))

            #For every node in node_history
            for n in self.a_star[3+index]:

                #Check if f is not set, or n.f is better than current f
                if temp[n.cord[0]][n.cord[1]] > 0 and n.f < temp[n.cord[0]][n.cord[1]] or temp[n.cord[0]][n.cord[1]] == 0:

                    #Node's cordinate is set to node's f
                    temp[n.cord[0]][n.cord[1]] = n.f

            #Set temp as map_with_f
            self.map_with_f = temp
        
        #Return map with f
        return self.map_with_f