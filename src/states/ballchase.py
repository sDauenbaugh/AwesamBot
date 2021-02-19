from util.gameinformation import GameInformation
from states.state import State

from rlbot.agents.base_agent import SimpleControllerState
from controllers.groundController import ground_controller


class BallChase(State):
    """BallChase aims to drive the car straight toward the ball
    
    This State has no regard for other cars or the movement of the ball. This is a simple state not meant for use in-game.
    
    Note:
        This state is always available and expires after every tick.
    
    """
    def __init__(self):
        """Creates an unexpired instance of BallChase"""
        super().__init__()
        
    def get_expired(self, game_info: GameInformation):
        """Determines if the state is no longer useful"""
        return True
    
    def execute(self, game_info: GameInformation):
        """Attempts to drive the car toward the ball.
        
        Overrides the State class's execute function. The ground controller is automatically used and the target 
        location is set to the ball's current location.
        
        Attributes:
            game_info: information detailing the current status of various game objects
            
        Returns:
            target_location: the location to give the bot.
            
        """
        
        target_location = game_info.ball.local_location
        return ground_controller(game_info, target_location)
