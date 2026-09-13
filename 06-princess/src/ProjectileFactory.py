from Projectile_2 import Projectile
import settings
import pygame

# Clase básica para representar el aspecto visual e hitbox de la flecha
class ArrowObject:
    def __init__(self, x: float, y: float, direction: str):
        self.x = x
        self.y = y
        self.direction = direction
        self.texture = settings.TEXTURES["arrow"]
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        
        if direction == "up":
            self.image = pygame.transform.rotate(self.texture, 90)
        elif direction == "down":
            self.image = pygame.transform.rotate(self.texture, -90)
        elif direction == "left":
            self.image = pygame.transform.flip(self.texture, True, False)
        else: # right
            self.image = self.texture

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0) -> None:
        surface.blit(self.image, (self.x - offset_x, self.y - offset_y))


class ProjectileFactory:
    @staticmethod
    def create_projectile(proj_type: str, x: float, y: float, direction: str) -> Projectile:
        if proj_type == "arrow":
            # 1. Creamos el objeto visual de la flecha
            arrow_obj = ArrowObject(x, y, direction)
            # 2. Lo envolvemos en la clase Projectile que ya arreglamos antes
            return Projectile(arrow_obj, direction, "arrow")
        
        # Aquí puedes agregar el "pot" (jarrón) más adelante
        return None