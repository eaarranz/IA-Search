# -*- coding: utf-8 -*-
#
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def expand(frontera, closed, current_node, problem, heuristic):
    """
    It expands the node and handles its successors
    Returns the 'frontera' and 'closed' data strucutres updated with the childs
    """
    closed.add(current_node[0])
    childs = problem.getSuccessors(current_node[0])
    for child in childs:
        if isinstance(frontera, util.PriorityQueue):
            # In order to save memory we can recalculate the accum cost, this works well if the heuristic is O(1)
            accumulated_cost = current_node[2] + child[2] if current_node[2] == 0 else (
                current_node[2] - heuristic(current_node[0], problem)) + child[2]
            node_cost = accumulated_cost + heuristic(child[0], problem)
            #(Node, path, accumulated_cost)
            frontera.push((child[0], current_node[1] +
                           [child[1]], node_cost), node_cost)
        else:
            #(Node, path)
            frontera.push((child[0], current_node[1] + [child[1]]))


def commonSearch(frontera, problem, heuristic=lambda x, y: 0):
    """
    Interchangable implementation of the search algorithm, based on the 
    type of "frontera" it returns different results.
    """
    if isinstance(frontera, util.PriorityQueue):
        #(Node, path, accumulated_cost)
        frontera.push(((problem.getStartState()), [], 0), 0)
    else:
        #(Node, path)
        frontera.push(((problem.getStartState()), []))

    closed = set()
    while frontera:
        current_node = frontera.pop()
        if problem.isGoalState(current_node[0]):
            return current_node[1]
        if current_node[0] not in closed:
            expand(frontera, closed, current_node, problem, heuristic)

    return []


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    frontera = util.Stack()
    return commonSearch(frontera, problem)


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """

    frontera = util.Queue()
    return commonSearch(frontera, problem)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    frontera = util.PriorityQueue()
    return commonSearch(frontera, problem)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    frontera = util.PriorityQueue()
    return commonSearch(frontera, problem, heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
