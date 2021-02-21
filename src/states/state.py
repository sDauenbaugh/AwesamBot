from rlbot.agents.base_agent import SimpleControllerState

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
        """ Creates a new unexpired state"""
        self.expired = False
        self.debug = {'target': (0, 0, 0)}
        self.sequence = None
        self.next_controller_state = SimpleControllerState()

    def check_expired(self, game_info: GameInformation) -> bool:
        """ Checks to see if the state is still useful under current conditions

        Attributes:
            game_info: information detailing the current status of various game objects

        Returns:
            True if state is expired, otherwise false

        """
        self.expired = True
        return self.expired
    
    def execute(self, game_info: GameInformation):
        """ Executes the State's behavior. This must fill either the sequence or next_controller_state fields.
        
        This function must be overridden by other States. If it is not overridden then the bot will do nothing.
        
        Attributes:
            game_info: information detailing the current status of various game objects
            
        """
        pass

    def get_debug(self):
        """ Returns the debug information stored by the state. The information contained may vary by state

        Returns:
             Dictionary of debug messages

        """
        return self.debug

    def has_sequence(self) -> bool:
        """ Determines if the state has a sequence to return.

        Returns:
            True if there is a sequence
            False if there is no sequence

        """
        return self.sequence is None

    def get_sequence(self):
        """ Returns the sequence stored by the state

        Returns:
            Sequence of SimpleControllerState objects

        """
        return self.sequence

    def get_next_controller_state(self) -> SimpleControllerState:
        """ Returns the next SimpleControllerState to execute.

        Returns:
            SimpleControllerState containing the next move

        """
        return self.next_controller_state
