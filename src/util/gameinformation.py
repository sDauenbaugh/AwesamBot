#This object will encapsulate game information for the purpose of passing data to states.

class GameInformation():

    def __init__(self, me, ball):
        self.ball = ball
        self.me = me