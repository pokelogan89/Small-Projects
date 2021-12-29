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

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)

def neighborCheck(maze,point):
    neighbors = maze.getNeighbors(point[0],point[1])
    return neighbors

def pathGenerator(inp):
    for j in range(len(inp)):
        for k,l in enumerate(inp[j]):
            yield j,k,l


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
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    obj = tuple(x for y in maze.getObjectives() for x in y)
    start,depth,nQ,xQ,path = maze.getStart(),1,[],[],[obj]
    objx,objy,sx,sy = obj[0],obj[1],start[0],start[1]

    visited = np.zeros((len(maze.mazeRaw),len(maze.mazeRaw[0])),int)
    while not visited[objx][objy]:
        nQ,xQ = xQ,[]
        if not visited[sx][sy]:
            nQ.append((sx,sy))

        for point in nQ:
            px, py = point[0],point[1]
            neighbors = neighborCheck(maze,point)
            for p in neighbors:
                if not (visited[p[0]][p[1]] or p in xQ):
                    xQ.append(p)
            visited[px][py] = depth
        depth += 1 
   
    i = 2

    while i < depth - 1:
        px,py = path[0][0],path[0][1]
        for j,k,l in pathGenerator(visited):
            if l == depth - i and abs(px + py - j - k) == 1 and (abs(px - j) == 0 or abs(py - k) == 0):
                path.insert(0,(j,k))
                break
        i += 1

    path.insert(0,start)
    return path


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    
    pass


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