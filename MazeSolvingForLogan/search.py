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
import maze
import numpy as np
import operator as op
from time import time

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

class inQ:
    def __init__(self,point,depth,p1,p2):
        self.point = point
        self.depth = depth
        distance = abs(p1[0] - p2[0]) + abs(p1[1] + p2[1])
        self.weight = depth + distance

def astar(maze): 
    obj = tuple(x for y in maze.getObjectives() for x in y)
    start = maze.getStart()
    n_stack = [inQ(start,1,obj,start)]
    path,back_trace = [obj],{}

    visited = np.zeros((maze.getDimensions()[0],maze.getDimensions()[1]),bool)

    while not visited[obj[0]][obj[1]]:
        work_obj = n_stack[0]
        n_stack.pop(0)
        visited[work_obj.point[0]][work_obj.point[1]] = True
        neighbors = maze.getNeighbors(work_obj.point[0],work_obj.point[1])

        for node in neighbors:
            if not (node in n_stack or visited[node[0]][node[1]]):
                sQ = inQ(node,work_obj.depth + 1,obj,node)
                back_trace[sQ.point] = work_obj.point
                if not n_stack:
                    n_stack.append(sQ)
                    continue
                for i,w_comp in enumerate(n_stack):
                    if sQ.weight < w_comp.weight or i == len(n_stack) - 1:
                        n_stack.insert(i,sQ)
                        break   
    while path[0] != start:
        path.insert(0,back_trace[path[0]])
    return path

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here

    pass

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