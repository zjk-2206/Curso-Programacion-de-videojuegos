from gale.timer import Timer
from src.states.entity.BaseEntityState import BaseEntityState

class BossStrongState(BaseEntityState):
    def __init__(self, entity, state_machine):
        self.entity = entity
        self.state_machine = state_machine
        self.timer = None

    def enter(self, **params):
        # Iniciar animación fuerte/idle
        self.entity.change_animation("idle_strong")
        
        # Dispara una bola de fuego cada 1.5 segundos
        self.timer = Timer.every(1.5, self.entity.shoot)

    def update(self, dt):
        pass # Aquí podrías añadir lógica para que el boss siga al jugador (walk)

    def exit(self):
        # Es crucial eliminar el timer cuando entra en el estado débil para que deje de disparar
        if self.timer:
            self.timer.remove()