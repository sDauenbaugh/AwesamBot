from util.gameinformation import GameInformation


class State:
    """State objects dictate the bot's current objective.
    
    State objects are intended to be immutable, as they do not have any instance variables that need to be canged. The only reason these are implemented as a class
    rather than a module is for easier tracking of active states. States are used to determine the behavior and commands necessary for a bot. The state itself does
    not determine which state should be used if itself is no longer useful.
    
    Currently Implemented States:
        BallChase
        
    States in Development:
        CalcShot
        DefendBasic
        GetBoost
        GetBack
        
    Attributes: expired (bool)
    
    """
    def __init__(self):
        """Creates a new unexpired state"""
        self.expired = False

    def get_expired(self, game_info: GameInformation):
        """Checks to see if the state is still useful under current conditions"""
        self.expired = True
    
    def execute(self, game_info: GameInformation):
        """Executes the State's behavior.
        
        This function must be overridden by other States. If it is not overriden then the bot will do nothing.
        
        Attributes:
            game_info: information detailing the current status of various game objects
            
        Returns:
            Nothing.
            When overridden this function should return a SimpleControllerState() containing the commands for the car.
            
        """
        pass
