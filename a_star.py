import heapq

#Manhattan Distance
def md(loc1, loc2):
    return abs(loc1[0]-loc2[0]) + abs(loc1[1]-loc2[1])

#Manhattan Distance to Nearest Goal
def bmd(cord, goals):
    #Sets best Manhattan distance value to infinite
    bmdv = float("inf")

    #Finds Manhattan distance for each goal and compares with current best Manhattan distance value
    #If the Manhattan distance value is lower, the best Manhattan distance is updated
    for goal in goals:
        mdv = md(cord, goal)
        if(mdv < bmdv):
            bmdv = mdv
    
    #Returns best Manhattan distance value
    return bmdv

#Node Class to Represent Squares on the Map
class Node:
    #Initialize method
    #cord = cordinates of node
    #goals = a list of goal cordinates
    #parent = node that discovered this node
    #movement_cost = cost to move to this node
    def __init__(self, cord, goals, parent, moevement_cost):
        self.cord = cord
        self.parent = parent
        self.movement_cost = moevement_cost

        #If node is not start node, set g, h and f values
        if moevement_cost > -1 and parent is not None:
            self.g = parent.g + moevement_cost
            self.h = bmd(cord, goals)
            self.f = self.g + self.h
        #Node is start node
        else:
            self.g = -1
            self.h = -1
            self.f = -1
    
    #OVERRIDE equals
    def __eq__(self, other):
        if self.cord == other.cord:
            return True
        else:
            return False
        
    #Sets what variable represents the nodes value
    def __repr__(self):
        return self.f

    #OVERRIDE less than
    def __lt__(self, other):
        return self.f < other.f

    #Method to check if node has same location as any node in list
    def in_list(self, list):
        for other in list:
            if self.cord[0] == other.cord[0] and self.cord[1] == other.cord[1]:
                return True
        return False

    #Method to check if the node cord is the same as cord in list
    def is_goal(self, cords):
        for cord in cords:
            if self.cord[0] == cord[0] and self.cord[1] == cord[1]:
                return True
        return False

#A* algrotithm
def a_star(map, start, goals, cost_cap=9):
    #Makes node of start cordinate
    start = Node(start, goals, None, map[start[0]][start[1]])

    #Sets current node to start node before loop
    current_node = start

    #Initializing lists for handeling nodes
    open_list = []
    closed_list = []
    node_history_list = []

    #Loop until goal is found
    while current_node.is_goal(goals) is False:
        #add current node to closed list
        closed_list.append(current_node)

        #add current node to node-history list
        node_history_list.append(current_node)
        
        #Initializing list for children of current node
        children = []

        #Makes node of each neighboring cord if inside the map
        for i in [(1,0), (0,1), (-1,0), (0,-1)]:
            cord = current_node.cord[0] + i[0], current_node.cord[1] + i[1]
            if(cord[0] < len(map) and cord[0] >= 0 and cord[1] < len(map[0]) and cord[1] >= 0):
                children.append(Node(cord, goals, current_node, map[cord[0]][cord[1]]))

        #Adds child nodes to open_list if it is not already used and is not an obsticle
        for child in children:
            if child.movement_cost < cost_cap and not child.in_list(closed_list):
                heapq.heappush(open_list, child)
        
        #If open_list has entries, choose node with smallest f as current node
        if(len(open_list) > 0):
            current_node = heapq.heappop(open_list)
        #Else return with no path from start to any goal
        else:
            return -1, [], [], map, node_history_list

    #Extract cost from current node, which is a goal
    cost = current_node.g

    #Initializing lists for presenting found path
    path = []
    node_path = []

    #Backtracks path from goal to start node and adds nodes to path
    while not (current_node == start):
        path.append(current_node.cord)
        node_path.append(current_node)
        current_node = current_node.parent

    #Adds start node to lists
    path.append(start.cord)
    node_path.append(start)
    
    #return path cost, path as lists of cords, path as list of nodes, map, list of nodes as used
    return cost, path[::-1], node_path.reverse(), map, node_history_list