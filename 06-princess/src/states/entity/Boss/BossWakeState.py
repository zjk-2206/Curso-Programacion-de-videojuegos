from gale.timer import Timer
from src.states.entity.BaseEntityState import BaseEntityState

class BossWakeState(BaseEntityState):
    def __init__(self, entity, state_machine):
        self.entity = entity
        self.state_machine = state_machine
        self.stun_timer = None

    def enter(self, **params):
        # Iniciar animación donde parezca cansado o aturdido
        self.entity.change_animation("wake")
        
        # Se queda débil durante 3 segundos, luego vuelve a 'strong'
        self.stun_timer = Timer.after(3, lambda: self.state_machine.change("strong"))

    def exit(self):
        if self.stun_timer:
            self.stun_timer.remove()