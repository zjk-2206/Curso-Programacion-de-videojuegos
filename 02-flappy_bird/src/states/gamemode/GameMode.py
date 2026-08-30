import pygame
import random
from gale.input_handler import InputData

class GameMode:
    def __init__(self):
        pass
    
    #todo esto lo han de sobreescribir los hijos de esta clase que son GameModeNormal y GameModeHard
    #movimiento vertical de los troncos
    def space_log_H(self, dt: float, wordl):
        pass
    #movimiento del pajaro
    def move_bird(self, bird, input_id: str, input_data: InputData):
        pass