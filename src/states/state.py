class State():
    """State objects dictate the bot's current objective.
    
    These objects are used to control the behavior of the bot at a high level. States are reponsible for determining
    which controller to use as well as what actions the car needs to take. States do not directly determine controller inputs.
    State names should be descriptive and unique.
    
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
    
    def execute(self, agent):
        """Executes the State's behavior.
        
        This function must be overridden by other States.
        
        Attributes:
            agent (BaseAgent): The bot
            
        Returns:
            Nothing.
            When overridden this function should return a SimpleControllerState() containing the commands for the car.
            
        """
        pass
    
    def checkAvailable(self, agent):
        """Checks to see if the state is available. The default state is unavailable
        
        Attributes:
            agent (BaseAgent): the bot
        
        Returns:
            bool: False unless overridden. True means available, false means unavailable.
        
        """
        return False