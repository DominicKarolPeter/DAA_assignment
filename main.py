import tkinter as tk
import pygame

from game_screen import show_game_screen
from intro_screen import show_intro_screen
from graph_controller import grid_generator
from constants import VOLUME

root = tk.Tk()
root.withdraw()

pygame.mixer.init()
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(VOLUME / 100)
pygame.mixer.music.play(-1)

while True:
    result = show_intro_screen(root)
    if result["action"] == 0:
        root.destroy()
        break
    
    SIZE = result["size"]
    MOVES = result["moves"]
    MODE = result["mode"]
    
    graph, color = grid_generator(SIZE)
    
    show_game_screen(root, graph, color, MOVES, MODE, SIZE)

root.mainloop()
