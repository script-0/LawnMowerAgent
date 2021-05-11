"""
	Importing some useful libraries
"""
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from typing import Tuple

"""
	Defining Agent clas
"""

class MowerAgent(Agent):
    """ A Mower as an Agent."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        new_position = Tuple[int, int]
        if ( self.pos[0] < (self.model.grid.width-1) and self.pos[0] >0 ) :
            if ( self.model.direction == 'R' ) :
                new_position =  tuple([ self.pos[0]+1 , self.pos[1] ])
            elif ( self.model.direction == 'L' ) :
                new_position = tuple ( [ self.pos[0]-1 , self.pos[1] ])
            else : 
                print(" Not implemented 1")
        elif ( self.pos[0] == (self.model.grid.width - 1 ) ):
            if ( self.model.direction == 'R' ) :
                
                new_position = tuple( [ self.pos[0] , self.pos[1]+1 ] )
                self.model.direction = 'B'
            elif ( self.model.direction == 'B' ) :
                new_position = tuple ( [ self.pos[0]-1 , self.pos[1] ] )
                self.model.direction = 'L'
            else :
                print(" Not implemented 2")
        else :
            if ( self.model.direction == 'L' ) :
                
                new_position = tuple ( [ self.pos[0] , self.pos[1]+1 ] )
                self.model.direction = 'B'
            elif ( self.model.direction == 'B' ) :
                new_position = tuple ( [ self.pos[0]+1 , self.pos[1] ] )
                self.model.direction = 'R'
            elif ( self.model.direction == 'R' ) :
                new_position = tuple ( [ self.pos[0]+1 , self.pos[1] ] )
            else :
                print(" Not implemented 3")
        self.model.grid.move_agent(self, new_position)

    """
    	Defining the function which will be called after each step
    """
    def step(self):
        self.move()


"""
	Defining the model class
"""
class MowerModel(Model):
    """A model with 1 Mower."""
    def __init__(self, N, width, height):
        super().__init__()  # !!IMPORTANT : https://github.com/projectmesa/mesa/issues/627
        self.num_agents = N
        self.direction = 'R'
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            a = MowerAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            self.grid.place_agent(a, tuple([0, 0]) )

    def step(self):
        self.schedule.step()


from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

"""
	Defining how each agent will be represented
"""
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.3}
    return portrayal

"""
	Launching the model
"""
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(MowerModel,
                       [grid],
                       "Lawn Mower Model",
                       {"N":1, "width":10, "height":10})
server.port = 8521 # The default
server.launch()
