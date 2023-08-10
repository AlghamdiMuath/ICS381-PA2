import heapq
from problem import *


class Node :
    def __init__(self,state,parent_node = None , action_from_parent = None , path_cost =0):
        self.state = state
        self.parent_node  = parent_node
        self.action_from_parent = action_from_parent
        self.path_cost = path_cost
        self.depth = 0
        if parent_node: 
            self.depth = parent_node.depth + 1
            
    def __lt__(self, other):
        return self.state < other.state

class PriorityQueue:
    def __init__(self, items=(), priority_function=(lambda x: x)):
        self.priority_function = priority_function
        self.pqueue = []
        # add the items to the PQ
        for item in items:
            self.add(item)

    def add(self, item):
        pair = (self.priority_function(item), item)
        heapq.heappush(self.pqueue, pair)

    def pop(self):
        return heapq.heappop(self.pqueue)[1]
    
    def __len__(self):
        return len(self. pqueue)

#Copied from the book
def expand(problem , node):
    s = node.state
    for action in problem.actions(s):
        snew = problem.result(s,action)
        cost = node.path_cost + problem.action_cost(s,action,snew)
        yield Node(snew,node,action,cost)



def get_path_actions(node):
    if node == None:
        return []
    if node.parent_node == None:
        return []
    Nodespath = [node.action_from_parent]
    parentnode = node.parent_node
    while  parentnode.parent_node:
        
        Nodespath.append(parentnode.action_from_parent)
        parentnode = parentnode.parent_node
        
    Nodespath.reverse() # Hint: follow the parent pointers to the root. Be sure to return in the correct order (not reverse order)
    return Nodespath
# Almost same as get_path_actions
def get_path_states(node):
    if node == None:
        return []
    Nodestates = []
    Nodestates.append(node.state)
    parentnode = node.parent_node
    
    while  parentnode != None:
        Nodestates.append(parentnode.state)
        parentnode = parentnode.parent_node
        
    Nodestates.reverse()
    return Nodestates

#from slides graph-like
def best_first_search(problem,f):
    
    node = Node(problem.initial_state)
    frontier = PriorityQueue((node,),f)
    reached = {problem.initial_state:node}
    while  len(frontier): #len(frontier) != 0
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        
        for child in expand(problem , node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return None #failure


def best_first_search_treelike(problem,f):
    node = Node(problem.initial_state)
    frontier = PriorityQueue((node,),f)

    while  len(frontier):#len(frontier) != 0
        node = frontier.pop()
        
        if problem.is_goal(node.state):
            return node
        for child in expand(problem , node):
            frontier.add(child)      
    return None #failure

def breadth_first_search(problem , treelike = False):
    
    f = (lambda n: n.depth)
    if not treelike: # if treelike = False will execute
        return best_first_search(problem,f)
    return best_first_search_treelike(problem,f)

def depth_first_search(problem , treelike = False):
    f = (lambda n: -n.depth)
    if not treelike:
        return best_first_search(problem,f)
    return best_first_search_treelike(problem,f)
def uniform_cost_search(problem , treelike = False):
    f = (lambda n: n.path_cost)
    if not treelike:
        return best_first_search(problem,f)
    return best_first_search_treelike(problem,f)
def greedy_search(problem ,h, treelike = False):
    f = (lambda n: h(n))
    if not treelike:
        return best_first_search(problem,f)
    return best_first_search_treelike(problem,f)
def astar_search(problem ,h, treelike = False):
    f=( lambda n: n.path_cost + h(n) )
    if not treelike:
        return best_first_search(problem,f)
    return best_first_search_treelike(problem,f)

