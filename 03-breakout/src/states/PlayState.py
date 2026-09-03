"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class to define the Play state.
"""

import random

import pygame
from typing import Any

from gale.factory import AbstractFactory
from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import render_text

import settings
import src.powerups



class PlayState(BaseState):
    def enter(self, **params: dict):
        self.level = params["level"]
        self.score = params["score"]
        self.lives = params["lives"]
        self.paddle = params["paddle"]
        self.balls = params["balls"]
        self.brickset = params["brickset"]
        self.live_factor = params["live_factor"]
        self.points_to_next_live = params["points_to_next_live"]
        self.points_to_next_grow_up = (
            self.score
            + settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
        )
        self.powerups = params.get("powerups", [])

        if not params.get("resume", False):
            self.balls[0].vx = random.randint(-80, 80)
            self.balls[0].vy = random.randint(-170, -100)
            settings.SOUNDS["paddle_hit"].play()

        self.powerups_abstract_factory = AbstractFactory("src.powerups")
        self.powerup_active: bool = False 
        self.powerup_active_rocket = False
        self.timer_powerup: float = 0.0
        self.balls_rocket = []
        self.balls_page = []
        self.launch_balls: bool = False
        self.balls_rocket_launch = False
        self.bomb_active = False

    def update(self, dt: float) -> None:
        self.paddle.update(dt)
               
        
        for ball in self.balls:
            ball.update(dt)
            ball.solve_world_boundaries()

            # Check collision with the paddle
            if not self.powerup_active:
                if ball.collides(self.paddle):
                    settings.SOUNDS["paddle_hit"].stop()
                    settings.SOUNDS["paddle_hit"].play()
                    ball.rebound(self.paddle)
                    ball.push(self.paddle)
            
            else:
                if ball.collides(self.paddle):
                    self.timer_powerup += dt 
                    self.balls_page.append(ball)
                    #self.balls.remove(ball)
                    if self.timer_powerup < 5:
                        for ball_page in self.balls_page:
                            ball_page.vx = self.paddle.vx
                            ball_page.vy = 0
                    elif self.launch_balls:
                        print("se salio del powerup")
                    elif self.timer_powerup >= 5:
                        settings.SOUNDS["launch_rocket"].play()
                        self.launch_balls = True
                        
            
            if self.launch_balls:
                for ball_page in self.balls_page:
                    ball_page.vx = random.randint(-80, 80)
                    ball_page.vy = random.randint(-170, -100)
                    #self.balls.append(ball_page)
                self.powerup_active = False
                self.launch_balls = False
                self.timer_powerup = 0.0
                self.balls_page.clear()
                    
                    
            if self.powerup_active_rocket:
                for ball_rocket in self.balls_rocket:
                    ball_rocket.vx = self.paddle.vx
                
            if self.balls_rocket_launch:
                for ball_rocket in self.balls_rocket:
                    ball_rocket.vx = random.randint(-10, 10)
                    ball_rocket.vy = random.randint(-170, -100)
                self.balls_rocket.clear()
                self.balls_rocket_launch = False
                self.powerup_active_rocket = False
                

            # Check collision with brickset
            if not ball.collides(self.brickset):
                continue

            brick = self.brickset.get_colliding_brick(ball.get_collision_rect())

            if brick is None:
                continue

            brick.hit()
            self.score += brick.score()
            ball.rebound(brick)

            # Check earn life
            if self.score >= self.points_to_next_live:
                settings.SOUNDS["life"].play()
                self.lives = min(3, self.lives + 1)
                self.live_factor += 0.5
                self.points_to_next_live += settings.LIVE_POINTS_BASE * self.live_factor

            # Check growing up of the paddle
            if self.score >= self.points_to_next_grow_up:
                settings.SOUNDS["grow_up"].play()
                self.points_to_next_grow_up += (
                    settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
                )
                self.paddle.inc_size()

            # Chance to generate two more balls
            random_num = random.random()
            if random_num <= 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("TwoMoreBall").create(
                        r.centerx - 8, r.centery - 8
                    )
                )
            
            if random_num > 0.1 and random_num <= 0.2:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("CaptureBalls").create(
                        r.centerx - 8, r.centery - 8
                    )
                )
            if random_num > 0.2 and random_num <= 0.3:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("RocketUp").create(
                        r.centerx - 8, r.centery - 8
                    )
                )
            if random_num > 0.3 and random_num <= 0.35:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("BombUp").create(
                        r.centerx - 8, r.centery - 8
                    )
                )
                

        # Removing all balls that are not in play
        self.balls = [ball for ball in self.balls if ball.active]

        self.brickset.update(dt)

        if not self.balls:
            self.lives -= 1
            if self.lives == 0:
                self.state_machine.change("game_over", score=self.score)
            else:
                self.paddle.dec_size()
                self.state_machine.change(
                    "serve",
                    level=self.level,
                    score=self.score,
                    lives=self.lives,
                    paddle=self.paddle,
                    brickset=self.brickset,
                    points_to_next_live=self.points_to_next_live,
                    live_factor=self.live_factor,
                )

        # Update powerups
        for powerup in self.powerups:
            powerup.update(dt)

            if powerup.collides(self.paddle):
                powerup.take(self)

        # Remove powerups that are not in play
        self.powerups = [p for p in self.powerups if p.active]

        # Check victory
        if self.brickset.size == 1 and next(
            (True for _, b in self.brickset.bricks.items() if b.broken), False
        ):
            settings.SOUNDS["winner2"].play()
            settings.SOUNDS["winner2"].set_volume(0.6)
            self.state_machine.change(
                "victory",
                lives=self.lives,
                level=self.level,
                score=self.score,
                paddle=self.paddle,
                balls=self.balls,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
            )
        
        if self.brickset.size == 0:
            settings.SOUNDS["winner1"].play()
            settings.SOUNDS["winner1"].set_volume(0.8)
            self.state_machine.change(
                "victory",
                lives=self.lives,
                level=self.level,
                score=self.score,
                paddle=self.paddle,
                balls=self.balls,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
            )

    def render(self, surface: pygame.Surface) -> None:
        heart_x = settings.VIRTUAL_WIDTH - 120

        i = 0
        # Draw filled hearts
        while i < self.lives:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][0]
            )
            heart_x += 11
            i += 1

        # Draw empty hearts
        while i < 3:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][1]
            )
            heart_x += 11
            i += 1

        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["tiny"],
            settings.VIRTUAL_WIDTH - 80,
            5,
            (255, 255, 255),
        )

        self.brickset.render(surface)

        self.paddle.render(surface)

        for ball in self.balls:
            ball.render(surface)

        for powerup in self.powerups:
            powerup.render(surface)
            

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_left":
            if input_data.pressed:
                self.paddle.vx = -settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx < 0:
                self.paddle.vx = 0
        elif input_id == "move_right":
            if input_data.pressed:
                self.paddle.vx = settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx > 0:
                self.paddle.vx = 0
        elif input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "pause",
                level=self.level,
                score=self.score,
                lives=self.lives,
                paddle=self.paddle,
                balls=self.balls,
                brickset=self.brickset,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
                powerups=self.powerups,
            )
        elif input_id == "launch_ball" and input_data.pressed:
            if self.powerup_active:
                self.launch_balls = True

        elif input_id == "rocket_ball" and input_data.pressed:
            if self.powerup_active_rocket:
                settings.SOUNDS["launch_rocket"].play()
                settings.SOUNDS["launch_rocket"].set_volume(1.0)
                self.balls_rocket_launch = True
                
                
            
