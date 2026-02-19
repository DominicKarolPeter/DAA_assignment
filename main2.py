import tkinter as tk

from game_screen import show_game_screen
from intro_screen import show_intro_screen
from graph_controller import grid_generator

root = tk.Tk()
root.withdraw()  # Hide the main window while the intro screen is active

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