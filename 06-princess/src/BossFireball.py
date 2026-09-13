import pygame
import math
import settings

class BossFireball:
    def __init__(self, x: float, y: float, target_x: float, target_y: float):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.speed = 100 
        self.dead = False
        
        
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        
    def update(self, dt: float):
        self.x += self.dx * dt
        self.y += self.dy * dt
        
        
        if (self.x < 0 or self.x > settings.VIRTUAL_WIDTH or
            self.y < 0 or self.y > settings.VIRTUAL_HEIGHT):
            self.dead = True

    def collides(self, target) -> bool:
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        target_rect = pygame.Rect(target.x, target.y, target.width, target.height)
        return rect.colliderect(target_rect)
        
    def render(self, surface: pygame.Surface):
        surface.blit(settings.TEXTURES["fire-ball"])