from src.Tile import Tile
import pygame
import settings

class LineClearUp(Tile):
    def __init__(self, i, j, color, variety):
        super().__init__(i, j, color, variety)
        self.is_powerup = True
        self.powerup_type = "line_clear"
        
    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int):
        super().render(surface, offset_x, offset_y)
        
        pygame.draw.rect(
            surface, 
            (255, 215, 0),
            pygame.Rect(self.x + offset_x, self.y + offset_y, settings.TILE_SIZE, settings.TILE_SIZE),
            width=3,
            border_radius=7
        )
        
    def activate(self, board) -> list:
        tiles_to_destroy = []
        
        #para filas
        for col in range(settings.BOARD_WIDTH):
            tiles_to_destroy.append(board.tiles[self.i][col])
            
        #para columnas
        for row in range(settings.BOARD_HEIGHT):
            if board.tiles[row][self.j] not in tiles_to_destroy:
                tiles_to_destroy.append(board.tiles[row][self.j])
        return tiles_to_destroy

class ColorBombUp(Tile):
    def __init__(self, i, j, color, variety):
        super().__init__(i, j, color, variety)
        self.is_powerup = True
        self.powerup_type = "color_bomb"
    
    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int):
        super().render(surface, offset_x, offset_y)
        
        pygame.draw.rect(
            surface, 
            (255, 255, 255),
            pygame.Rect(self.x + offset_x, self.y + offset_y, settings.TILE_SIZE, settings.TILE_SIZE),
            width=3,
            border_radius=7
        )
    
    def activate(self, board) -> list:
        tile_to_destroy = []
        
        for row in range(settings.BOARD_HEIGHT):
            for col in range(settings.BOARD_WIDTH):
                if board.tiles[row][col].color == self.color:
                    tile_to_destroy.append(board.tiles[row][col])
        return tile_to_destroy

class TileFactory:
    @staticmethod
    def create_normal(i, j, color, variety):
        return Tile(i, j, color, variety)

    @staticmethod
    def create_line_clear(i, j, color, variety):
        return LineClearUp(i, j, color, variety)
    
    @staticmethod
    def create_color_bomb(i, j, color, variety):
        return ColorBombUp(i, j, color, variety)