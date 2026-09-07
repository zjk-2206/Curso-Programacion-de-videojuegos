"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any, List

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer
from src.TileFactory import TileFactory

import settings



class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.board = enter_params["board"]
        self.score = enter_params["score"]

        # Position in the grid which we are highlighting
        #self.board_highlight_i1 = -1
        #self.board_highlight_j1 = -1
        #self.board_highlight_i2 = -1
        #self.board_highlight_j2 = -1

        #variables para el arrastre
        self.dragging = False
        self.dragged_tile = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.mouse_start_x = 0
        self.mouse_start_y = 0
        self.drag_i = -1
        self.drag_j = -1
        self.shuffle_message = False
        
        self.highlighted_tile = False

        self.active = True

        self.timer = settings.LEVEL_TIME

        self.goal_score = self.level * 1.25 * 1000

        # A surface that supports alpha to highlight a selected tile
        self.tile_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.tile_alpha_surface,
            (255, 255, 255, 96),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )

        # A surface that supports alpha to draw behind the text.
        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
        )

        def decrement_timer():
            self.timer -= 1

            # Play warning sound on timer if we get low
            if self.timer <= 5:
                settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)
        
        self.check_no_moves_left()

    def update(self, _: float) -> None:
        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            self.state_machine.change("begin", level=self.level + 1, score=self.score)
            
        if getattr(self, 'dragging', False) and self.dragged_tile:
            mx, my = pygame.mouse.get_pos()
            mx = mx * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            my = my * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
            
            delta_X = mx - self.mouse_start_x
            delta_Y = my - self.mouse_start_y
            
            if abs(delta_X) > abs(delta_Y):
                delta_Y = 0
                delta_X = max(-settings.TILE_SIZE,  min(delta_X, settings.TILE_SIZE))
            else:
                delta_X = 0
                delta_Y = max(-settings.TILE_SIZE, min(delta_Y, settings.TILE_SIZE))
                
            if self.drag_j == 0 and delta_X < 0: delta_X = 0
            if self.drag_j == settings.BOARD_WIDTH - 1 and delta_X > 0: delta_X = 0
            if self.drag_i == 0 and delta_Y < 0: delta_Y = 0
            if self.drag_i == settings.BOARD_HEIGHT - 1 and delta_Y > 0: delta_Y = 0
            
            self.dragged_tile.x = self.drag_start_x + delta_X
            self.dragged_tile.y = self.drag_start_y + delta_Y

    def check_no_moves_left(self) -> None:
        if not self.board.has_valid_moves():
            self.active = False
            self.shuffle_message = True
        
            def perform_shuffle():
                self.board.ensure_valid_moves()
                self.shuffle_message = False
                self.active = True
                settings.SOUNDS["re-org"].stop()
                settings.SOUNDS["re-org"].play()
                
            Timer.tween(
                1.5, 
                [],
                on_finish=perform_shuffle
            )

    def render(self, surface: pygame.Surface) -> None:
        self.board.render(surface, getattr(self, 'dragged_tile', None))

        if getattr(self, 'shuffle_message', False):
            render_text(
                surface,
                "Sin movimientos!",
                settings.FONTS['medium'],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT // 2 - 30,
                (255, 255, 255)
            )
            render_text(
                surface,
                "Reordenando tablero...",
                settings.FONTS['small'],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT // 2 + 20,
                (200, 200, 200)
            )

        if self.highlighted_tile:
            x = self.highlighted_j1 * settings.TILE_SIZE + self.board.x
            y = self.highlighted_i1 * settings.TILE_SIZE + self.board.y
            surface.blit(self.tile_alpha_surface, (x, y))

        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active:
            return

        if input_id == "click" and input_data.pressed:
            pos_x, pos_y = input_data.position
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT

            if not getattr(self, 'dragging', False):
                i = (pos_y - self.board.y) // settings.TILE_SIZE
                j = (pos_x - self.board.x) // settings.TILE_SIZE
                
                if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:
                    clicked_tile = self.board.tiles[i][j]
                    if getattr(clicked_tile, 'is_powerup', False):
                        self.active = False
                        tiles_destroyed = clicked_tile.activate(self.board)
                        self.score += len(tiles_destroyed) * 50
                        
                        self.board.matches.append(tiles_destroyed)
                        self.board.remove_matches()
                        falling_tiles = self.board.get_falling_tiles()
                        
                        Timer.tween(
                            0.25,
                            falling_tiles,
                            on_finish=lambda: self._calculate_matches(
                                [item[0] for item in falling_tiles]
                            )
                        )
                        return
                    
                    self.dragging = True
                    self.dragged_tile = self.board.tiles[i][j]
                    
                    self.drag_start_x = self.dragged_tile.x
                    self.drag_start_y = self.dragged_tile.y
                    
                    self.mouse_start_x = pos_x
                    self.mouse_start_y = pos_y
                    self.drag_i = i
                    self.drag_j = j
                    
        elif input_data.released and getattr(self, 'dragging', False) and getattr(self, 'dragged_tile', None) is not None:
                    self.dragging = False
                    
                    dx = self.dragged_tile.x - self.drag_start_x
                    dy = self.dragged_tile.y - self.drag_start_y
                    threshold = settings.TILE_SIZE // 2
                    
                    target_i = self.drag_i
                    target_j = self.drag_j
                    
                    if abs(dx) > threshold:
                        target_j += 1 if dx > 0 else -1
                    if abs(dy) > threshold:
                        target_i += 1 if dy > 0 else -1
                        
                    di = abs(target_i - self.drag_i)
                    dj = abs(target_j - self.drag_j)
                    
                    if (di == 1 and dj == 0) or (di == 0 and dj == 1):
                        self.active = False
                        tile1 = self.dragged_tile
                        tile2 = self.board.tiles[target_i][target_j]
                        
                        def arrive():
                            tile1 = self.dragged_tile
                            tile2 = self.board.tiles[target_i][target_j]
                            (
                                self.board.tiles[tile1.i][tile1.j],
                                self.board.tiles[tile2.i][tile2.j],
                            ) = (
                                self.board.tiles[tile2.i][tile2.j],
                                self.board.tiles[tile1.i][tile1.j],
                            )
                            tile1.i, tile1.j, tile2.i, tile2.j = (
                                tile2.i,
                                tile2.j,
                                tile1.i,
                                tile1.j,
                            )
                            
                            matches = self.board.calculate_matches_for([tile1, tile2])
                            
                            if matches:
                                self.dragged_tile = None
                                self._calculate_matches([tile1, tile2])
                            else:
                                
                                (
                                    self.board.tiles[tile1.i][tile1.j],
                                    self.board.tiles[tile2.i][tile2.j]
                                ) = (
                                    self.board.tiles[tile2.i][tile2.j],
                                    self.board.tiles[tile1.i][tile1.j]
                                )
                                tile1.i, tile1.j, tile2.i, tile2.j = (
                                    tile2.i, 
                                    tile2.j, 
                                    tile1.i,
                                    tile1.j,
                                )
                                
                                def revert_finish():
                                    self.dragged_tile = None
                                    self.active = True
                                    
                                Timer.tween(
                                    0.15,
                                    [
                                      (tile1, {"x": self.drag_start_x, "y": self.drag_start_y}),
                                      (tile2, {"x": target_j * settings.TILE_SIZE, "y": target_i * settings.TILE_SIZE}),  
                                    ],
                                    on_finish=revert_finish,
                                )
                        # Swap tiles
                        Timer.tween(
                            0.2,
                            [
                                (tile1, {"x": target_j * settings.TILE_SIZE, "y": target_i * settings.TILE_SIZE}),
                                (tile2, {"x": self.drag_start_x, "y": self.drag_start_y}),
                            ],
                            on_finish=arrive,
                        )
                    else:
                        self.active = False
                        
                        def bound_finish():
                            self.dragged_tile = None
                            self.active = True
                        
                        Timer.tween(
                            0.15,
                            [(self.dragged_tile, {"x": self.drag_start_x, "y": self.drag_start_y})],
                            on_finish=bound_finish
                        )

                    self.highlighted_tile = False

    def check_board_state(self):
        if not self.board.has_valid_moves():
            self.board.ensure_valid_moves()
    
    def _calculate_matches(self, tiles: List) -> None:
        matches = self.board.calculate_matches_for(tiles)

        if matches is None:
            self.check_no_moves_left()
            self.active = True
            self.check_board_state()
            return

        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()
        
        powerups_to_spawn = []
        processed_matches = []
        all_destroyed_tiles = set()
        
        for match in matches:
            match_tiles = set(match)
            
            for tile in match:
                if getattr(tile, 'is_powerup', False):
                    extra_tiles = tile.activate(self.board)
                    for et in extra_tiles:
                        match_tiles.add(et)
            
            processed_matches.append(list(match_tiles))
            for t in match_tiles:
                all_destroyed_tiles.add(t)
                
            if len(match) >= 4:
                spawn_tile = match[0]
                for tile in match:
                    if tile in tiles:
                        spawn_tile = tile
                        break
                powerups_to_spawn.append({
                    "i": spawn_tile.i,
                    "j": spawn_tile.j,
                    "color": spawn_tile.color,
                    "variety": spawn_tile.variety,
                    "length": len(match)
                })
                
        self.score += len(all_destroyed_tiles) * 50
        self.board.matches = processed_matches
        self.board.remove_matches()
        
        for p_data in powerups_to_spawn:
            if p_data["length"] == 4:
                new_powerup = TileFactory.create_line_clear(
                    p_data["i"], p_data["j"], p_data["color"], p_data["variety"]
                )
                settings.SOUNDS["clear_line"].stop()
                settings.SOUNDS["clear_line"].play()
            elif p_data["length"] >= 5:
                new_powerup = TileFactory.create_color_bomb(
                    p_data["i"], p_data["j"], p_data["color"], p_data["variety"]
                )
                settings.SOUNDS["color_bomb"].stop()
                settings.SOUNDS["color_bomb"].play()
            self.board.tiles[p_data["i"]][p_data["j"]] = new_powerup

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self._calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )
