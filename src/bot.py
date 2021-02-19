import math
import numpy as np

from states.shoot import Shoot
from states.ballchase import BallChase
from states.defendbasic import Defend

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation, relative_location
from util.vec import Vec3
import util.util as util
from util.gameinformation import GameInformation



class GameObject():
    """GameObjects are considered to be all objects that can move on the field.
        
    Attributes:
        location (Vec3): location vector defined by x,y,z coordinates
        velocity (Vec3): velocity vector with x,y,z components
        orientation (Orientation): orientation vector defined by pitch, yaw, and roll
        r_velocity (Vec3): Rotational velocity define by pitch, yaw, and roll components as x, y, z respectively
        local_location (Vec3): location of the GameObject relative to the bot
        
    """
    
    def __init__(self):
        """Creates a new GameObject with zeroed data."""
        self.location = Vec3(0, 0, 0)
        self.velocity = Vec3(0, 0, 0)
        self.orientation = Orientation(0, 0, 0)
        self.r_velocity = Vec3(0, 0, 0)
        
        self.local_location = Vec3(0, 0, 0)


class Car(GameObject):
    """Car is an Extension of the GameObject class that holds data and function specific to the behavior of other cars.
    
    Attributes:
        boost (float): The amount of boost remaining in the car
    
    """
    def __init__(self):
        """Creates a new Car object with zero boost."""
        super().__init__()
        self.boost = 0.0
        self.team = -1
    

class Ball(GameObject):
    """Ball is an extension of the gameObject class that holds data and functions specific to the ball
    
    """
    def __init__(self):
        """Creates a new Ball object."""
        super().__init__()


class MyBot(BaseAgent):
    """MyBot is an extension of the BaseAgent class and handles all of the logic of the bot. 
    
    This is the class used by the rlBot framework to run the bot in-game.
    
    Attributes:
        controller_state (SimpleControllerState): The current set of commands the bot's controller should receive
        me (Car): The Car GameObject representing the bot
        ball (Ball): The Ball object representing the ball
        state (State): The state governing the bot's current behavior
    
    """

    def initialize_agent(self):
        """The setup function that runs once when the bot is created."""
        self.controller_state = SimpleControllerState()
        self.me = Car()
        self.ball = Ball()
        
        self.state = BallChase()
        self.state_message = "Whoops"

    def get_output(self, game_packet: GameTickPacket) -> SimpleControllerState:
        """Calculates the next set of commands for the bot.
        
        This function should run 60 times a second, or once for every game tick. This function also calls a set
        of commands to draw debug information on screen.
        
        Args:
            game_packet (GameTickPacket): set of current information about the game
            
        Returns:
            SimpleControllerState: the next set of commands for the bot
            
        """
        self.preprocess(game_packet)

        game_info = GameInformation(self.me, self.ball)

        self.state = BallChase()
        controller_state = self.state.execute(game_info)
                
        if self.state.get_expired(game_info):
            if util.sign(self.ball.location.y) == util.sign(self.me.team):
                self.state = Defend()
                self.state_message = "Defending"
            elif util.sign(self.ball.location.y) != util.sign(self.me.team):
                self.state = Shoot()
                self.state_message = "Attacking"
            else:
                self.state = BallChase()
                self.state_message = "Chasing"
        
        team = util.sign(self.team)
        ball_side = util.sign(self.ball.location.y)
        
        my_car = game_packet.game_cars[self.index]
        message = f"{self.state_message} | Team {team} | Ball {ball_side} "
        action_display = message
        ball_path = util.predict_ball_path(self)
        turn_loops = get_turn_circle(self.me.velocity, self.me.location)
        draw_debug(self.renderer, my_car, game_packet.game_ball, action_display, ball_path, turn_loops)

        return controller_state
    
    def preprocess(self, game_packet: GameTickPacket):
        """Calculates a set of values that may be useful.
        
        This function runs every tick, so it should not contain any operations that are slow. Additionally, the operations
        should be limited to what is necessary to have on every tick.
        
        Args:
            game_packet (GameTickPacket): set of current information about the game
            
        Returns:
            This function updates the attributes of the class and therefore has no return type. 
            
        """
        # load data about self
        self.me.location = Vec3(game_packet.game_cars[self.index].physics.location)
        self.me.velocity = Vec3(game_packet.game_cars[self.index].physics.velocity)
        self.me.rotation = Orientation(game_packet.game_cars[self.index].physics.rotation)
        self.me.r_velocity = Vec3(game_packet.game_cars[self.index].physics.angular_velocity)
        self.me.boost = game_packet.game_cars[self.index].boost
        self.me.team = self.team
        
        # load data about the ball
        self.ball.location = Vec3(game_packet.game_ball.physics.location)
        self.ball.velocity = Vec3(game_packet.game_ball.physics.velocity)
        self.ball.rotation = Orientation(game_packet.game_ball.physics.rotation)
        self.ball.r_velocity = Vec3(game_packet.game_ball.physics.angular_velocity)
        
        self.ball.local_location = relative_location(self.me.location, self.me.rotation, self.ball.location)


def draw_debug(renderer, car, ball, action_display, ball_path, turns):
    """Draws debug information on screen.
    
    Args:
        renderer: renderer that will draw the information
        car: car object from GameTickPacket representing the bot
        ball: ball object from GameTickPacket
        action_display: message to display describing the car's current action
        ball_path: set of information containing the ball's predicted path
        turns: loops showing the turn radius of the car
        
    Returns:
        This function has no returns, but instead draws information directly to the screen.
    
    """
    renderer.begin_rendering()
    # draw a line from the car to the ball
    renderer.draw_line_3d(car.physics.location, ball.physics.location, renderer.white())
    # print the action that the bot is taking
    renderer.draw_string_3d(car.physics.location, 2, 2, action_display, renderer.white())
    # draw the ball's predicted path
    renderer.draw_polyline_3d(ball_path, renderer.red())
    # stop rendering to avoid render limit
    renderer.end_rendering()
    # draw turn radius at current velocity
    # renderer.begin_rendering()
    # renderer.draw_polyline_3d(turns, renderer.blue())
    # renderer.end_rendering()


def get_turn_circle(velocity, location):
    """Generates a list of tuples containing the coordinates for the smallest turn available to the car"""
    radius = util.turn_radius(velocity.length())
    ground_velocity = velocity.flat()
    ground_location = location.flat()
    # calculate phase offset
    unit_location = ground_velocity.rotate90().normalized()
    phi = np.arctan2(unit_location.y, -unit_location.x)
    # calculate center offset
    right_center = ground_location + (unit_location * radius)
    left_center = ground_location + (ground_velocity.rotate90(-1).normalized() * radius)
    # calculate points
    theta = np.arange(phi, 2*np.pi - phi, np.pi/16)
    x = radius*np.cos(theta)
    y = radius*np.sin(theta)
    right_loop = tuple(zip(x+right_center.x, y+right_center.y))
    left_loop = tuple(zip(x+left_center.x, y+left_center.y))
    return right_loop + left_loop
