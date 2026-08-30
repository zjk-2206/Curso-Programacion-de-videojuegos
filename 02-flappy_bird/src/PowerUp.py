
import pygame
import settings

class PowerUp:
    def __init__(self, x: float, y: float, visible:bool = True ):
        self.x: float = x
        self.y: float = y
        self.visible: bool = visible
        
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), settings.POWER_UP_WIDTH, settings.POWER_UP_HEIGHT)
    
    def collides(self, rect: pygame.Rect) -> bool:
        if self.get_rect().colliderect(rect):
            self.visible = False
        return self.get_rect().colliderect(rect)
    
    def update(self, dt: float) -> None:
        self.x += -settings.MAIN_SCROLL_SPEED * dt
        
    def is_out_of_game(self) -> bool:
        return self.x < -settings.LOG_WIDTH
        
    def render(self, surface: pygame.Surface) -> None:
        if self.visible:
            surface.blit(settings.TEXTURES["powerup"], self.get_rect())