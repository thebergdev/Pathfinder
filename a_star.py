import heapq

#Manhattan Distance
def md(loc1, loc2):
    return abs(loc1[0]-loc2[0]) + abs(loc1[1]-loc2[1])

#Manhattan Distance to Nearest Goal
def bmd(cord, goals):
    bmdv = float("inf")
    for goal in goals:
        mdv = md(cord, goal)
        if(mdv < bmdv):
            bmdv = mdv
    return bmdv

#Node Class to Represent Squares on the Map
class Node:
    def __init__(self, cord, goals, parent, moevement_cost):
        self.cord = cord
        self.parent = parent
        self.movement_cost = moevement_cost
        if moevement_cost > -1 and parent is not None:
            self.g = parent.g + moevement_cost
            self.h = bmd(cord, goals)
            self.f = self.g + self.h
        else:
            self.g = -1
            self.h = -1
            self.f = -1
    
    def __eq__(self, other):
        if self.cord == other.cord:
            return True
        else:
            return False

    def __repr__(self):
        return self.f

    def __lt__(self, other):
        return self.f < other.f

    def in_list(self, list):
        for other in list:
            if self.cord[0] == other.cord[0] and self.cord[1] == other.cord[1]:
                return True
        return False

    def is_goal(self, goals):
        for goal in goals:
            if self.cord[0] == goal[0] and self.cord[1] == goal[1]:
                return True
        return False

#A* algrotithm
def a_star(map, start, goals):
    start = Node(start, goals, None, map[start[0]][start[1]])
    current_node = start
    open_list = []
    closed_list = []

    while current_node.is_goal(goals) is False:
        #print('Current node: ', current_node.cord)
        closed_list.append(current_node)
        children = []
        for i in [(1,0), (0,1), (-1,0), (0,-1)]:
            cord = current_node.cord[0] + i[0], current_node.cord[1] + i[1]
            if(cord[0] < len(map) and cord[0] >= 0 and cord[1] < len(map[0]) and cord[1] >= 0):
                children.append(Node(cord, goals, current_node, map[cord[0]][cord[1]]))
        for child in children:
            if child.movement_cost < 9 and not child.in_list(closed_list):
                heapq.heappush(open_list, child)
        if(len(open_list) > 0):
            current_node = heapq.heappop(open_list)
        else:
            return -1, [], [], map

    cost = current_node.g
    path = []
    node_path = []


    while not (current_node == start):
        path.append(current_node.cord)
        node_path.append(current_node)
        map[current_node.cord[0]][current_node.cord[1]] = 0
        current_node = current_node.parent

    path.append(start.cord)
    node_path.append(start)

    return cost, path[::-1], node_path, map