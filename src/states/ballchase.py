from src.states.state import State

from rlbot.agents.base_agent import SimpleControllerState
from src.controllers.groundController import groundController

class BallChase(State):
    """BallChase aims to drive the car straight toward the ball
    
    This State has no regard for other cars or the movement of the ball. This is a simple state not meant for use in-game.
    
    Note:
        This state is always available and expires after every tick.
    
    """
    def __init__(self):
        """Creates an unexpired instance of BallChase"""
        super().__init__()
        self.ticks = 0
        
    def getExpired(self, gameInfo):
        """Determines if the state is no longer useful"""
        self.ticks = self.ticks + 1
        if self.ticks > 10:
            self.expired = True
    
    def execute(self, gameInfo):
        """Attempts to drive the car toward the ball.
        
        Overrides the State class's execute function. The ground controller is automatically used and the target 
        location is set to the ball's current location.
        
        Attributes:
            agent (BaseAgent): The bot
            
        Returns:
            target_location: the location to give the bot.
            
        """
        
        target_location = gameInfo.ball.local_location
        return groundController(gameInfo, target_location)
