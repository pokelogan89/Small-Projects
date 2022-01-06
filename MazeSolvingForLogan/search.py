# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

#import queue
import math
#from queue import PriorityQueue
import heapq

from numpy.core.shape_base import stack
import maze
import numpy as np
import operator as op
import time

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)

def sanity_check(maze, path):
    """
    Runs check functions for part 0 of the assignment.

    @param maze: The maze to execute the search on.
    @param path: a list of tuples containing the coordinates of each state in the computed path

    @return bool: whether or not the path pass the sanity check
    """
    # TODO: Write your code here

    #print("sanity check called")
    
    return False

def bfs(maze):
    obj = tuple(x for y in maze.getObjectives() for x in y)
    start = maze.getStart()
    next_stack,path,back_trace = [start],[obj],{}

    visited = np.zeros((len(maze.mazeRaw),len(maze.mazeRaw[0])),bool)

    while not visited[obj[0]][obj[1]]:
        work_stack,next_stack = next_stack,[]
        for point in work_stack:
            neighbors = maze.getNeighbors(point[0],point[1])
            for node in neighbors:
                if not (node in next_stack or visited[node[0]][node[1]]):
                    next_stack.append(node)
                    back_trace[node] = point
            visited[point[0]][point[1]] = True
    
    while path[0] != start:
        path.insert(0,back_trace[path[0]])
    return path

#Used for astar
class inQ:
    def __init__(self,point,depth,objs,p2):
        distance = -1
        self.point = point
        self.depth = depth #Distance travelled
        for obj in objs:
            if distance < 0:
                distance = abs(obj[0] - p2[0]) + abs(obj[1] - p2[1])
                self.obj = (obj[0],obj[1])
                continue
            if distance > abs(obj[0] - p2[0]) + abs(obj[1] - p2[1]):
                distance = abs(obj[0] - p2[0]) + abs(obj[1] - p2[1])
                self.obj = (obj[0],obj[1])
        self.distance = distance
        self.weight = depth + distance #Distance travelled + theoretical distance to finish

def astar(maze):
    objective_l = maze.getObjectives()
    objective = objective_l[0]
    start = maze.getStart()
    search_Q = [inQ(start,1,objective_l,start)]

    #Defining list of nodes in queue, path list, and dictionary to store path to path relations
    node_list,path,back_trace = [],[objective],{}

    visited = np.zeros((maze.getDimensions()[0],maze.getDimensions()[1]),bool)

    while not visited[objective[0]][objective[1]]:
        work_obj = search_Q.pop(0)
        visited[work_obj.point[0]][work_obj.point[1]] = True
        if node_list:
            node_list.remove(work_obj.point)

        #Finding all the possible neighbor coordinates in the maze that can be travelled to
        neighbors = maze.getNeighbors(work_obj.point[0],work_obj.point[1])

        for node in neighbors:
            if not (node in node_list or visited[node[0]][node[1]]):
                node_obj = inQ(node,work_obj.depth + 1,objective_l,node)
                back_trace[node_obj.point] = work_obj.point
                node_list.append(node)

                if not search_Q:
                    search_Q.append(node_obj)
                    continue

                for i,weight_comp in enumerate(search_Q):
                    if node_obj.weight < weight_comp.weight:
                        search_Q.insert(i,node_obj)
                        break

                if node_obj not in search_Q:
                    search_Q.append(node_obj)
    while path[0] != start:
        path.insert(0,back_trace[path[0]])
    return path

def astar_corner(maze):
    objective = maze.getObjectives()
    start = maze.getStart()
    search_Q = [inQ(start,1,objective,start)]

    #Defining list of nodes in queue, path list, and dictionary to store path to path relations
    path,objectives_visited,node_list,back_trace = [],[start],[],{}

    visited = np.zeros((maze.getDimensions()[0],maze.getDimensions()[1]),bool)
    visited_mut = np.copy(visited)

    while objective:
        work_obj = search_Q.pop(0)
        visited_mut[work_obj.point[0]][work_obj.point[1]] = True
        
        if node_list:
            node_list.remove(work_obj.point)

        #Finding all the possible neighbor coordinates in the maze that can be travelled to
        neighbors = maze.getNeighbors(work_obj.point[0],work_obj.point[1])
        
        for node in neighbors:
            if not (node in node_list or visited_mut[node[0]][node[1]]):
                node_obj = inQ(node,work_obj.depth + 1,objective,node)

                back_trace[node_obj.point] = work_obj.point

                if node_obj.distance == 0:
                    objectives_visited.insert(0,node_obj.obj)
                    objective.remove(node_obj.obj)
                    visited[node_obj.obj[0]][node_obj.obj[1]] = True
                    visited_mut = np.copy(visited)
                    node_list,search_Q = [],[inQ(node_obj.obj,1,objective,node_obj.obj)]
                    
                    path_mut = [objectives_visited[0]]
                        
                    while path_mut[0] != objectives_visited[1]:
                        path_mut.insert(0,back_trace[path_mut[0]])

                    back_trace = {}
                    path_mut.pop(0)

                    for point in path_mut:
                        path.append(point)
                    break

                node_list.append(node)

                if not search_Q:
                    search_Q.append(node_obj)
                    continue
                
                for i,weight_comp in enumerate(search_Q):
                    if node_obj.weight < weight_comp.weight:
                        search_Q.insert(i,node_obj)
                        break

                if node_obj not in search_Q:
                    search_Q.append(node_obj)
    path.insert(0,start)
    return path 

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    pass

def extra(maze):
    """ 
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    """Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path"""
    
    # TODO: Write your code here

    pass