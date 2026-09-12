from typing import Dict, Any
import pygame
from gale.timer import Timer
from gale.state import BaseState
import settings


class FadeOutState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.next_level = enter_params.get("level")
        
        pygame.mixer.music.stop()
        
        # Referencias visuales necesarias del PlayState para mantener la escena visible
        self.game_level = enter_params.get("game_level")
        self.player = enter_params.get("player")
        self.camera = enter_params.get("camera")
        
        # Configuración del tiempo y opacidad (alpha de 0 a 255
        self.alpha = 255
        
        # Superficie para dibujar el rectángulo negro de desvanecimiento
        self.fade_surface = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT), pygame.SRCALPHA).convert_alpha()
        
        Timer.tween(
            7,
            [(self, {"alpha": 0})],
            on_finish=self.on_finish,
        )

    def on_finish(self): 
        print(self.next_level)
        if self.next_level > settings.NUM_LEVELS:
            self.state_machine.change("start")
            return
        
        self.state_machine.change("play", level=self.next_level)

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.game_level.render(self.fade_surface, self.camera)
        self.player.render(self.fade_surface, self.camera)
            
        self.fade_surface.set_alpha(self.alpha)
        surface.blit(self.fade_surface, (0, 0))

    def on_input(self, input_id: str, input_data: Any) -> None:
        # Bloquear la entrada del usuario durante la transición de salida
        pass