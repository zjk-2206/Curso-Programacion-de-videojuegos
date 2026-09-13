from src.states.entity.BaseEntityState import BaseEntityState
from src.states.entity.movement import move_and_bump

class BossWalkState(BaseEntityState):
    def enter(self, *args, **kwargs) -> None:
        self.entity.change_animation(f"walk-{self.entity.direction}")

    def process_ai(self, room, dt: float) -> None:
        if not room.player:
            return
        dx = room.player.x - self.entity.x
        dy = room.player.y - self.entity.y

        new_direction = self.entity.direction


        if abs(dx) > abs(dy):
            new_direction = "right" if dx > 0 else "left"
        else:
            new_direction = "down" if dy > 0 else "up"

        if new_direction != self.entity.direction:
            self.entity.direction = new_direction
            self.entity.change_animation(f"walk-{self.entity.direction}")

    def update(self, dt: float) -> None:
        move_and_bump(self.entity, dt)