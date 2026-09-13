from typing import Any, Dict
from src.Entity import Entity
from src.BossFireball import BossFireball
import settings

class Boss(Entity):
    def __init__(self, x: float, y: float, width: float, height: float, walk_speed: float, health: int, animation_defs: Dict[str, Dict[str, Any]], states: Dict[str, Any]) -> None:
        super().__init__(x, y, width, height, walk_speed, health, animation_defs, states)
        self.room = None 
    

    def damage(self, amount: int) -> None:
        if self.state_machine.current_state_name == "strong":
            settings.SOUNDS["hit-enemy"].play()
            self.change_state("wake")
            
        elif self.state_machine.current_state_name in ["wake", "walk"]:
            self.health -= amount
            if self.health <= 0:
                self.dead = True
    
    def shoot(self):
        if self.room and self.room.player:
            fireball = BossFireball(self.x, self.y, self.room.player.x, self.room.player.y)
            self.room.boss_projectiles.append(fireball)