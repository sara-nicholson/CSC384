# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
    return  [s, s, w, s, w, w, s, w]

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
    
    "*** YOUR CODE HERE ***"
    """
    
    opn = util.Stack()
    startState = problem.getStartState()
    start = [(startState, '',0)]
    #print start
    opn.push(start)

    while opn.isEmpty != True:
	path = opn.pop()
	state = path[-1][0]
	if problem.isGoalState(state):
	    dir = [path[i+1][1] for i in range(len(path)-1)]
	    return dir
	
	succ = problem.getSuccessors(state)
	for i in range(len(succ)):
	    if not succ[i][0] in (path[k][0] for k in range(len(path))):
		nextpath = []
		nextpath.extend(path)
		nextpath.append(succ[i])
	    	opn.push(nextpath)

    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #BFS - queue 
    opn = util.Queue()
    startState = problem.getStartState()
    start = [(startState, '',0)]
    opn.push(start)
    visited = set()
    visited.add(startState)

    while opn.isEmpty != True:
	path = opn.pop()
	state = path[-1][0]
        if problem.isGoalState(state):
	    dir = [path[i+1][1] for i in range(len(path)-1)]
	    return dir
	
	succ = problem.getSuccessors(state)
	for i in range(len(succ)):
	    if not succ[i][0] in visited:
		nextpath = []
		visited.add(succ[i][0])
		nextpath.extend(path)
		nextpath.append(succ[i])
		opn.push(nextpath)

    return []
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    opn = util.PriorityQueue()
    startState = problem.getStartState()
    start = [(startState, '',0)]
    opn.push(start,0)
    visited = {startState: -float("inf")}

    while opn.isEmpty != True:
	path = opn.pop()
	state = path[-1][0]
	if problem.isGoalState(state):
	    dir = [path[i+1][1] for i in range(len(path)-1)]
	    return dir
	
	succ = problem.getSuccessors(state)
	for i in range(len(succ)):
	    if not visited.has_key(succ[i][0]):
		nextpath = []
		nextpath.extend(path)
		nextpath.append(succ[i])
		priority = succ[i][2]
		for j in range(len(path)):
		    priority = priority + path[j][2]
		opn.push(nextpath,priority)
		visited.update({succ[i][0]:priority})
	    else:
		priority = succ[i][2]
		for j in range(len(path)):
		    priority = priority + path[j][2]
		cost = visited.get(succ[i][0])
		if cost > priority:
		    visited[succ[i][0]] = priority
		    nextpath = []
		    nextpath.extend(path)
		    nextpath.append(succ[i])
		    opn.push(nextpath,priority)
	

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    start = [(startState, '',0)]
    opn = util.PriorityQueue()
    visited = {startState: -float("inf")}
    starth = heuristic(startState,problem)
    opn.push(start,starth)
    while opn.isEmpty != True:
	path = opn.pop()
	state = path[-1][0]
	
	if problem.isGoalState(state):
	    dir = [path[k+1][1] for k in range(len(path)-1)]
	    return dir

	succ = problem.getSuccessors(state)
	for i in range(len(succ)):
	    nextpath = []
	    if not visited.has_key(succ[i][0]):
		nextpath.extend(path)
		nextpath.append(succ[i])
		g = succ[i][2]
		for j in range(len(path)):
		    g = g + path[j][2]
		visited.update({succ[i][0]:g})
		h = heuristic(succ[i][0],problem)
		priority = g+h
		opn.push(nextpath,priority)
	    else:
		g = succ[i][2]
		for j in range(len(path)):
		    g = g+path[j][2]
		cost = visited.get(succ[i][0])

		if cost > g:
		    visited[succ[i][0]] = g
		    nextpath.extend(path)
	 	    nextpath.append(succ[i])
		    h = heuristic(succ[i][0],problem)
		    priority = g+h
		    opn.push(nextpath,priority)
		    

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

