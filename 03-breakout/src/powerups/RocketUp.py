import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp

class RocketUp(PowerUp):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 7)
        self.ball_factory = Factory(Ball)
    
    def take(self, play_state: TypeVar("PlayState")) -> None:
        paddle = play_state.paddle
        
        a = self.ball_factory.create(paddle.x, paddle.y - 8)
        b = self.ball_factory.create(paddle.x + paddle.width - 8, paddle.y - 8)
        settings.SOUNDS["rockets"].play()
        
        play_state.balls_rocket.append(a)
        play_state.balls_rocket.append(b)
        play_state.balls.append(a)
        play_state.balls.append(b)
        play_state.powerup_active_rocket = True
        
        
        self.active = False
        