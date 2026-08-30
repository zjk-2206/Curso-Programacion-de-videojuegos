import pygame

from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import render_text
from src.World import World
from src.states.gamemode.GameMode import GameMode
from src.Bird import Bird
import settings

class PauseState(BaseState):
    def enter(self, gamemode: GameMode, bird : Bird ,world : World,**params: dict) -> None:
        self.score = params["score"]
        settings.SOUNDS["pause"].play()
        settings.SOUNDS["pause"].set_volume(0.5)
        self.gamemode: GameMode = gamemode
        self.world: World = world
        self.bird: Bird = bird
 
        
        
    
    def render(self, surface: pygame.Surface) -> None:
        render_text(
            surface,
            f"Score : {self.score}",
            settings.FONTS["huge"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 3,
            (255, 255, 255),
            center=True,
        )
        
        render_text(
            surface,
            "Pause",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2,
            (255, 255, 255),
            center=True,
        )
        
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause_tab" and input_data.pressed:
            self.state_machine.change(
                "playing", self.gamemode, self.bird, self.world 
            )
        