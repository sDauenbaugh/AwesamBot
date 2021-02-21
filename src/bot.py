import numpy as np

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

import states as st
from game_object import *
from util import util
from util.boost_pad_tracker import BoostPadTracker
from util.gameinformation import GameInformation
from util.orientation import Orientation, relative_location
from util.sequence import Sequence
from util.vec import Vec3


class MyBot(BaseAgent):
    """MyBot is an extension of the BaseAgent class and handles all of the logic of the bot.

    This is the class used by the rlBot framework to run the bot in-game.

    Attributes:
        controller_state (SimpleControllerState): The current set of commands the bot's controller should receive
        me (Car): The Car GameObject representing the bot
        ball (Ball): The Ball object representing the ball
        state (State): The state governing the bot's current behavior

    """

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.active_sequence: Sequence = None
        self.boost_pad_tracker = BoostPadTracker()

        self.controller_state = SimpleControllerState()
        self.me = Car()
        self.ball = Ball()
        self.kickoff_flag = False

        self.state = st.State()
        self.state_message = "State"

    def initialize_agent(self):
        """The setup function that runs once when the bot is created."""
        self.controller_state = SimpleControllerState()
        self.kickoff_flag = False

        self.state = st.Kickoff()
        self.state_message = "Kickoff"

    def get_output(self, game_packet: GameTickPacket) -> SimpleControllerState:
        """Calculates the next set of commands for the bot.

        This function should run 60 times a second, or once for every game tick. This function also calls a set
        of commands to draw debug information on screen.

        Args:
            game_packet (GameTickPacket): set of current information about the game

        Returns:
            SimpleControllerState: the next set of commands for the bot

        """
        # debugging flags. debug mode tells whether to print messages to console, debug_change flags when a change
        # occurs that should trigger a debug message
        debug_mode = True
        debug_change = False

        # Keep our boost pad info updated with which pads are currently active
        # self.boost_pad_tracker.update_boost_status(game_packet)

        # clear active_sequence when kickoff is starting
        if self.kickoff_flag is False and game_packet.game_info.is_round_active and \
                game_packet.game_info.is_kickoff_pause:
            self.active_sequence = None

        self.preprocess(game_packet)

        game_info = GameInformation(self.me, self.ball)

        # if there is an active sequence then that gets priority and no other state or controller calculations are done
        if self.active_sequence is not None and not self.active_sequence.done:
            self.controller_state = self.active_sequence.tick(game_packet)
        # if there is no active sequence we proceed with normal state calculations
        else:
            # kickoff state get priority
            if self.kickoff_flag:
                self.state = st.Kickoff()
                self.state_message = "Kickoff"
            # get new state if expired
            elif self.state.check_expired(game_info):
                debug_change = True
                if util.sign(self.ball.location.y) == util.sign(self.me.team):
                    self.state = st.Defend()
                    self.state_message = "Defend"
                elif util.sign(self.ball.location.y) != util.sign(self.me.team):
                    self.state = st.Shoot()
                    self.state_message = "Shoot"
                else:
                    self.state = st.BallChase()
                    self.state_message = "BallChase"
            # execute the current state
            self.state.execute(game_info)
            if self.state.has_sequence():
                self.active_sequence = self.state.get_sequence()
                self.controller_state = self.active_sequence.tick(game_packet)
            else:
                self.controller_state = self.state.get_next_controller_state()

        team = util.sign(self.team)
        ball_side = util.sign(self.ball.location.y)

        message = f"{self.state_message} | Team {team} | Ball {ball_side}"
        if debug_change and debug_mode:
            print(message)
        # action_display = message
        # ball_path = util.predict_ball_path(self)
        # turn_loops = get_turn_circle(self.me.velocity, self.me.location)
        self.draw_debug(message, self.state.get_debug()['target'])

        return self.controller_state

    def preprocess(self, game_packet: GameTickPacket):
        """Calculates a set of values that may be useful.

        This function runs every tick, so it should not contain any operations that are slow.
        Additionally, the operations should be limited to what is necessary to have on every tick.

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

        # flag that kickoff is occurring
        self.kickoff_flag = game_packet.game_info.is_round_active and game_packet.game_info.is_kickoff_pause

    def draw_debug(self, action_display=None, target=None):
        """Draws debug information on screen.

        Args:
            action_display: message to display describing the car's current action
            target: location that the bot is targeting

        Returns:
            This function has no returns, but instead draws information directly to the screen.

        """
        # self.renderer.begin_rendering()
        # draw a line from the car to the ball
        self.renderer.draw_line_3d(self.me.location, self.ball.location, self.renderer.white())
        # print the action that the bot is taking
        if action_display:
            self.renderer.draw_string_3d(self.me.location, 2, 2, action_display, self.renderer.cyan())
        # draw line to target location
        if target:
            self.renderer.draw_line_3d(self.me.location, target, self.renderer.black())
        # draw the ball's predicted path
        # renderer.draw_polyline_3d(ball_path, renderer.red())
        # stop rendering to avoid render limit
        # self.renderer.end_rendering()
        # draw turn radius at current velocity
        self.renderer.draw_polyline_3d(get_turn_circle(self.me.velocity, self.me.location), self.renderer.blue())


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
    theta = np.arange(phi, 2 * np.pi - phi, np.pi / 16)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    right_loop = tuple(zip(x + right_center.x, y + right_center.y))
    left_loop = tuple(zip(x + left_center.x, y + left_center.y))
    return right_loop + left_loop


"""
    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.active_sequence: Sequence = None
        self.boost_pad_tracker = BoostPadTracker()

    def initialize_agent(self):
        # Set up information about the boost pads now that the game is active and the info is available
        self.boost_pad_tracker.initialize_boosts(self.get_field_info())

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
"""
# This function will be called by the framework many times per second. This is where you can
# see the motion of the ball, etc. and return controls to drive your car.
"""

        # Keep our boost pad info updated with which pads are currently active
        self.boost_pad_tracker.update_boost_status(packet)

        # This is good to keep at the beginning of get_output. It will allow you to continue
        # any sequences that you may have started during a previous call to get_output.
        if self.active_sequence is not None and not self.active_sequence.done:
            controls = self.active_sequence.tick(packet)
            if controls is not None:
                return controls

        # Gather some information about our car and the ball
        my_car = packet.game_cars[self.index]
        car_location = Vec3(my_car.physics.location)
        car_velocity = Vec3(my_car.physics.velocity)
        ball_location = Vec3(packet.game_ball.physics.location)

        # By default we will chase the ball, but target_location can be changed later
        target_location = ball_location

        if car_location.dist(ball_location) > 1500:
            # We're far away from the ball, let's try to lead it a little bit
            ball_prediction = self.get_ball_prediction_struct()  # This can predict bounces, etc
            ball_in_future = find_slice_at_time(ball_prediction, packet.game_info.seconds_elapsed + 2)

            # ball_in_future might be None if we don't have an adequate ball prediction right now, like during
            # replays, so check it to avoid errors.
            if ball_in_future is not None:
                target_location = Vec3(ball_in_future.physics.location)
                self.renderer.draw_line_3d(ball_location, target_location, self.renderer.cyan())

        # Draw some things to help understand what the bot is thinking
        self.renderer.draw_line_3d(car_location, target_location, self.renderer.white())
        self.renderer.draw_string_3d(car_location, 1, 1, f'Speed: {car_velocity.length():.1f}', self.renderer.white())
        self.renderer.draw_rect_3d(target_location, 8, 8, True, self.renderer.cyan(), centered=True)

        if 750 < car_velocity.length() < 800:
            # We'll do a front flip if the car is moving at a certain speed.
            return self.begin_front_flip(packet)

        controls = SimpleControllerState()
        controls.steer = steer_toward_target(my_car, target_location)
        controls.throttle = 1.0
        # You can set more controls if you want, like controls.boost.

        return controls

    def begin_front_flip(self, packet):
        # Send some quickchat just for fun
        self.send_quick_chat(team_only=False, quick_chat=QuickChatSelection.Information_IGotIt)

        # Do a front flip. We will be committed to this for a few seconds and the bot will ignore other
        # logic during that time because we are setting the active_sequence.
        self.active_sequence = Sequence([
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=True)),
            ControlStep(duration=0.05, controls=SimpleControllerState(jump=False)),
            ControlStep(duration=0.2, controls=SimpleControllerState(jump=True, pitch=-1)),
            ControlStep(duration=0.8, controls=SimpleControllerState()),
        ])

        # Return the controls associated with the beginning of the sequence so we can start right away.
        return self.active_sequence.tick(packet)
"""
