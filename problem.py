
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
    def __init__(self, items, priority_function=(lambda x: x)):
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


class ConstrainedRouteProblem :
    def __init__(self, initial_agent_loc , goal_loc, map_edges, map_coords,must_visit):
        self.initial_agent_loc = initial_agent_loc
        self.goal_loc  = goal_loc
        self.map_edges = map_edges
        self.map_coords = map_coords
        self.must_visit = must_visit
        self.initial_state = (initial_agent_loc,False,False)
        
        for i in self.must_visit:
            self.initial_state = self.initial_state + (False,)
            
    def actions(self,state):
        directions = []
        for k,v in self.map_edges.items():
            if k[0] == state[0]:
                directions.append(k[1])
            if k[1] == state[0]:
                directions.append(k[0])
        return directions
    
    def result(self,state,action):
        toadd = 3
        Stateslist = list(state)
        if action in self.must_visit:
            value = self.must_visit.index(action)
        else:
            value = -1

        if value != -1:

            Stateslist[value+toadd] = True

        if action == self.goal_loc:

            if Stateslist[1] == True:

                Stateslist[2] = True
            else:
                Stateslist[1] = True

        Stateslist[0] = action
        transitionstate = tuple(Stateslist)
        return transitionstate
    
    def action_cost(self,state1,action,state2):
        for k,v in self.map_edges.items():
            if (k[0] == state2[0] and k[1] == state1[0]) or (k[0] == state1[0] and k[1] == state2[0]):
                return v
        return False
            
    def is_goal(self,state):
        if ((self.goal_loc == state[0]) and all(state[3:]) and state[1] and  state[2] == False):
            return True
        else:
            return False
    def h(self,node):
        stateValue = self.map_coords.get(node.state[0])

       
        GoalValue = self.map_coords.get(self.goal_loc)
      
        if node.state == self.goal_loc:
            return 0
        else:
            return ((pow((stateValue[0] - GoalValue[0]),2)+pow((stateValue[1]-GoalValue[1]),2))**0.5)
        



class GridProblemWithMonsters:
    def __init__(self, initial_agent_loc ,N, monster_coords, food_coords):
        self.initial_agent_loc = initial_agent_loc
        self.N  = N
        self.monster_coords = monster_coords
        self.food_coords = food_coords
        self.initial_state = (initial_agent_loc[0],initial_agent_loc[1],0)

        for i in self.food_coords:
            self.initial_state = self.initial_state + (False,)
       
    def actions(self,state):
        monstep = (state[2]+1)%4
        MonsterNewCoord = []
        if (monstep == 1):
            for key in self.monster_coords:
                
                if key[1] != 1:
                    MonsterNewCoord.append((key[0],key[1]-1))
                else:
                    MonsterNewCoord.append((key[0],key[1]))
        elif (monstep == 3):
            for key in self.monster_coords:
                
                if key[1] != self.N:
                    MonsterNewCoord.append((key[0],key[1]+1))
                else:
                    MonsterNewCoord.append((key[0],key[1]))
        else:
             for key in self.monster_coords:
                 MonsterNewCoord.append((key[0],key[1]))
                 
            
            
        
        directions = []
    
        if ((state[0]!=self.N) and ((state[0]+1,state[1]) not in MonsterNewCoord)):
            directions.append("up")
        if ((state[0]!=1) and ((state[0]-1,state[1]) not in MonsterNewCoord)):
            directions.append("down")
        if ((state[1]!=self.N) and ((state[0],state[1]+1) not in MonsterNewCoord)):
            directions.append("right")
        if ((state[1]!=1) and ((state[0],state[1]-1) not in MonsterNewCoord)):
            directions.append("left")
        if ((state[0],state[1]) not in MonsterNewCoord):
            directions.append("stay")
        return directions
    def result(self,state,action):
        StateList = list(state)
        
        StateList[2] = (StateList[2]+1)%4
        if (action == "up"):
            StateList[0] = StateList[0] + 1
        if (action == "down"):
            StateList[0] = StateList[0] - 1
        if (action == "right"):
            StateList[1] = StateList[1] + 1
        if (action == "left"):
            StateList[1] = StateList[1] - 1
        value = self.food_coords.index((StateList[0],StateList[1])) if (StateList[0],StateList[1]) in self.food_coords else -1
        if value != -1:

            StateList[value+3] = True
        state = tuple(StateList)

        return state
    
    
    def action_cost(self,state1,action,state2):
        return 1
    
    
    def is_goal(self,state):
        if all(state[3:]):
            return True
        return False
    
    
    def h(self,node):
        hList = []
        
        for i in range (len(node.state[3:])):
            if node.state[i+3] == False:
                hList.append(abs(node.state[0]-self.food_coords[i][0]) + abs(node.state[1]-self.food_coords[i][1]))
            

            
        

        if all(node.state[3:]):
           
            return 0

        return min(hList)  
        
      

  


