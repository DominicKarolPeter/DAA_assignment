from tkinter import *

from graph_controller import grid_update
from greedy import greedy_color_selector
from div_n_conq import div_n_conq
from backtracking import backtracking_color_selector
from dp import dp_color_selector
from constants import COMPUTER_DELAY, COLOR_NAMES, COLORS, VOLUME

# FOR DNC

priority_list = dict()
for i in COLORS:
    priority_list[i] = 0


def dnc_pick_color(color, new=True, priority_list=priority_list):
    def get_max(priority_list):
        # max = list(priority_list.keys())[0]
        max = next(iter(priority_list))
        for i in priority_list:
            if priority_list[i] > priority_list[max]:
                max = i
        del priority_list[max]
        return max

    if new:
        # priority_list = div_n_conq(color)
        priority_list.clear()
        priority_list.update(div_n_conq(color))
    return get_max(priority_list)



gameover = False

def show_game_screen(root, graph, color, MOVES, MODE, SIZE, win_sound, lose_sound):
    global gameover
    gameover = False
    """
    Docstring for show_game_screen

    :param root: The main Tkinter window.
    :param graph: The current graph state. It is a dictionary representing the adjacency list.
    :param color: The current color of each node. It is a list.
    :param moves_left: The number of moves left for the player.
    :param mode: The game mode, one of the following: "human", "alternate", "greedy", "divide_conquer", "dp".
    
    This function should create and display the game screen using Tkinter. It should show the grid based on the current graph and color state, display the number of moves left, and provide an interface for the player to select colors (if in human mode) or show the computer's move (if in computer mode). The game screen should update dynamically based on user interactions or computer decisions.
    """
    game_window = Toplevel(root)
    game_window.geometry("1300x650")
    game_window.title("Flood It!")
    game_window.config(bg="#000044")
    game_frame = Frame(game_window, bd=1, relief="solid")
    game_frame.place(relx=0.01, rely=0.95, width=550, height=550, anchor="sw")

    canvas = Canvas(game_frame, highlightthickness=0)
    canvas.place(relwidth=1, relheight=1)

    cell_size = 550 / SIZE

    current_turn = "You"


    def apply_move(selected_color: int, source: str):
        nonlocal MOVES, current_turn
        global gameover

        # if MOVES <= 0:
        #     return False

        # Ignore same-color selection
        if selected_color == color[0]:
            return False

        change = grid_update(selected_color, color, graph)

        if change == 1:
            MOVES -= 1
            text.insert(END, f"{source}", "blue")
            text.insert(END, f" selected color {COLOR_NAMES[selected_color]}. ")
            text.insert(END, f"Remaining moves: {MOVES}\n", "yellow")
            text.see(END)

        draw_grid(color)

        # GAME OVER LOGIC
        gameover = all(c == color[0] for c in color)
        if gameover:
            win_sound.play()
            text.insert(END, "The board has been completed!\n\n               YOU WIN!\n", "green")
            canvas.unbind("<ButtonRelease-1>")
            return False

        if change == -1: # Greedy failed- no expansion
            text.insert(END, f"{source} ", "blue")
            text.insert(END, f"selected color {COLOR_NAMES[selected_color]}, but it did not expand the region. Remaining moves: {MOVES}\n", "grey")
            text.see(END)
            return False

        if MOVES <= 0:
            gameover = True
            lose_sound.play()
            text.insert(END, "Game Over! No more moves left.\n", "red")
            canvas.unbind("<ButtonRelease-1>")
            return False

        # Alternate mode: switch turns
        if MODE == "alternate":
            current_turn = "Computer" if current_turn == "You" else "You"
            if current_turn == "Computer":
                game_window.after(800, computer_move)

        return True


    # ---------------- HUMAN INPUT ---------------- #

    def on_click(event):
        if MODE in ("greedy", "divide_conquer", "dp", "backtracking"):
            return

        if MODE == "alternate" and current_turn != "You":
            return

        col = int(event.x // cell_size)
        row = int(event.y // cell_size)

        if 0 <= row < SIZE and 0 <= col < SIZE:
            node = row * SIZE + col
            apply_move(color[node], "You")
        


    # ---------------- COMPUTER MOVE ---------------- #

    def computer_move(greedy_fail=False):
        if MOVES <= 0:
            return

        if MODE == "greedy" or MODE == "alternate" :
            selected_color = greedy_color_selector(graph, color)
            temp = apply_move(selected_color, "Computer")
        
        elif MODE == "dp":
            selected_color = dp_color_selector(graph, color)
            temp = apply_move(selected_color, "Computer")

        elif MODE == "backtracking":
            selected_color = dp_color_selector(graph, color)
            temp = apply_move(selected_color, "Computer")

        elif MODE == "divide_conquer":
            temp = False
            first_run = True
            while not temp and not gameover:
                selected_color = dnc_pick_color(color, new=first_run)
                # print(f"New List: {first_run}\nSelected color: {selected_color}\nPrio List: {priority_list}\n\n")
                first_run = False
                temp = apply_move(selected_color, "Computer")

        else:
            return

        if MODE in ("greedy", "divide_conquer", "dp", "backtracking") and temp:
            game_window.after(COMPUTER_DELAY, computer_move)


    # ---------------- DRAW GRID ---------------- #

    def draw_grid(color):
        canvas.delete("all")

        for node in range(SIZE * SIZE):
            row = node // SIZE
            col = node % SIZE

            x0 = col * cell_size
            y0 = row * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=COLORS[color[node]],
                outline=""
            )


    draw_grid(color)


    Label(
        game_window,
        text=f"{MODE.title()} Mode",
        bg="#000044",
        fg="white",
        font=("Arial", 24, "bold")
    ).place(relx=0.5, y=0.05, anchor="n")

    text_frame = Frame(game_window)
    text_frame.place(relx=0.99, rely=0.95, width=700, height=550, anchor="se")

    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text = Text(text_frame, yscrollcommand=scrollbar.set, bg="#00003a", fg="#ffffff", font="calibri 13")
    text.pack(side="left", fill="both", expand=True)
    text.tag_config("green", foreground="#39ff39", font=("calibri", 16))
    text.tag_config("red", foreground="#f58a8a", font=("calibri", 16))
    text.tag_config("blue", foreground="#47ecfe")
    text.tag_config("yellow", foreground="#f8f671")
    text.tag_config("grey", foreground="#929292")

    scrollbar.config(command=text.yview)


    # ---------------- MODE INITIALIZATION ---------------- #

    if MODE == "human":
        canvas.bind("<ButtonRelease-1>", on_click)

    elif MODE in ("greedy", "divide_conquer", "dp", "backtracking"):
        game_window.after(COMPUTER_DELAY, computer_move)

    elif MODE == "alternate":
        canvas.bind("<ButtonRelease-1>", on_click)
        text.insert(END, "Alternate Mode: You start.\n")

    game_window.wait_window()