import tkinter as tk
import pygame

from game_screen import show_game_screen
from intro_screen import show_intro_screen
from splash_screen import show_splash_screen
from graph_controller import grid_generator
from constants import VOLUME

root = tk.Tk()
root.withdraw()

pygame.mixer.init()
pygame.mixer.music.load("assets/bgm2.mp3")
pygame.mixer.music.set_volume(VOLUME / 100)
pygame.mixer.music.play(-1)

win_sound = pygame.mixer.Sound("assets/hooray.mp3")
win_sound.set_volume(1.0)
lose_sound = pygame.mixer.Sound("assets/aww.mp3")
lose_sound.set_volume(1.0)

show_splash_screen(root)
while True:
    result = show_intro_screen(root)
    if result["action"] == 0:
        root.destroy()
        break
    
    SIZE = result["size"]
    MOVES = result["moves"]
    MODE = result["mode"]
    
    graph, color = grid_generator(SIZE)
    
    show_game_screen(root, graph, color, MOVES, MODE, SIZE, win_sound, lose_sound)

root.mainloop()
