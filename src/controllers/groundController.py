import math

from rlbot.agents.base_agent import SimpleControllerState

def groundController(agent, target_location):
    """Gives a set of commands to move the car along the ground toward a target location
    
    Attributes:
        target_location (Vec3): The local location the car wants to aim for
        
    Returns:
        SimpleControllerState: the set of commands to achieve the goal
    """
    controllerState = SimpleControllerState()
    ball_direction = target_location
    distance = target_location.flat().length()
    
    angle = -math.atan2(ball_direction.y,ball_direction.x)

    if angle > math.pi:
        angle -= 2*math.pi
    elif angle < -math.pi:
        angle += 2*math.pi
    
    speed = 0.0
    turn_rate = 0.0
    r1 = 250
    r2 = 1000
    if distance <= r1:
        #calculate turn direction
        if(angle > 0):
            turn_rate = -1.0
        elif(angle < 0):
            turn_rate = 1.0
        #if toward ball move forward
        if(abs(angle) < math.pi / 4):
            speed = 1.0
        else: #if not toward ball reverse, flips turn rate to adjust
            turn_rate = turn_rate * -1.0
            speed = -1.0
    #if far away, move at full speed forward
    elif distance >= r2:
        speed = 1.0
        if agent.me.velocity.length() < 2250:
            controllerState.boost = True
        if(angle > math.pi/32):
            turn_rate = -1.0
        elif(angle < -math.pi/32):
            turn_rate = 1.0
    #if mid range, adjust forward
    else:
        #adjust angle
        if(angle > math.pi/32):
            turn_rate = -1.0
        elif(angle < -math.pi/32):
            turn_rate = 1.0
        #adjust speed
        if agent.me.velocity.length() < 2250:
            controllerState.boost = True
        if abs(angle) < math.pi / 2:
            speed = 1.0
        else:
            speed = 0.5
            
            
    controllerState.throttle = speed
    controllerState.steer = turn_rate
    return controllerState
