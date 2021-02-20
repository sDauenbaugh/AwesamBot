from util.orientation import Orientation
from util.vec import Vec3


class GameObject:
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
        self.orientation = Orientation()
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