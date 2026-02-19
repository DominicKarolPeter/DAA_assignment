from tkinter import *
from graph_controller import grid_update
from greedy import greedy_color_selector
from div_n_conq import div_n_conq
from dp import dp_color_selector

COMPUTER_DELAY = 2000

# def computer_color_selector(MODE):
#     if MODE == "greedy":
#         return greedy_color_selector
#     elif MODE == "divide_conquer":
#         return div_n_conq
#     else:
#         return greedy_color_selector # Default to greedy if mode is unrecognized

COLOR_NAMES = {
    1: "RED",  # RED
    2: "BLUE",  # BLUE
    3: "GREEN",  # GREEN
    4: "PURPLE",  # PURPLE
    5: "PINK",  # PINK
    6: "YELLOW"   # YELLOW
}
COLORS = {
    1: "#FF5555",  # RED
    2: "#8BE9FD",  # BLUE
    3: "#50FA7B",  # GREEN
    4: "#BD93F9",  # PURPLE
    5: "#FF79C6",  # PINK
    6: "#F1FA8C"   # YELLOW
}

# FOR DNC

priority_list = dict()
for i in COLORS:
    priority_list[i] = 0


def dnc_pick_color(color, new=True, priority_list= priority_list):
    def get_max(priority_list):
        # max = list(priority_list.keys())[0]
        max = next(iter(priority_list))
        for i in priority_list:
            if priority_list[i] > priority_list[max]:
                max = i
        del priority_list[max]
        return max

    if new:
        priority_list = div_n_conq(color)
    return get_max(priority_list)




def show_game_screen(root, graph, color, MOVES, MODE, SIZE):
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
    game_window.geometry("1300x600")
    game_window.title("Flood It!")
    game_window.config(bg="#000044")
    game_frame = Frame(game_window, bd=1, relief="solid")
    game_frame.place(x=10, rely=0.5, width=550, height=550, anchor="w")

    canvas = Canvas(game_frame, highlightthickness=0)
    canvas.place(relwidth=1, relheight=1)

    cell_size = 550 / SIZE

    current_turn = "Human"


    def apply_move(selected_color: int, source: str):
        nonlocal MOVES, current_turn

        if MOVES <= 0:
            return False

        # Ignore same-color selection
        if selected_color == color[0]:
            return False

        change = grid_update(selected_color, color, graph)
        if change == 1:
            MOVES -= 1
        draw_grid(color)

        if change == -1: # Greedy failed- no expansion
            text.insert(END, f"{source} selected color {COLOR_NAMES[selected_color]}, but it did not expand the region. Remaining moves: {MOVES}\n")
            text.see(END)
            return False

        text.insert(
            END,
            f"{source} selected color {COLOR_NAMES[selected_color]}. Remaining moves: {MOVES}\n"
        )
        text.see(END)

        # GAME OVER LOGIC
        gameover = all(c == color[0] for c in color)
        if gameover:
            text.insert(END, "The board has been completed!\n\n               YOU WIN!\n")
            canvas.unbind("<ButtonRelease-1>")
            return False



        if MOVES <= 0:
            text.insert(END, "Game Over! No more moves left.\n")
            canvas.unbind("<ButtonRelease-1>")
            return False

        # Alternate mode: switch turns
        if MODE == "alternate":
            current_turn = "Computer" if current_turn == "Human" else "Human"
            if current_turn == "Computer":
                game_window.after(800, computer_move)
        return True


    # ---------------- HUMAN INPUT ---------------- #

    def on_click(event):
        if MODE in ("greedy", "divide_conquer", "dp"):
            return

        if MODE == "alternate" and current_turn != "Human":
            return

        col = int(event.x // cell_size)
        row = int(event.y // cell_size)

        if 0 <= row < SIZE and 0 <= col < SIZE:
            node = row * SIZE + col
            apply_move(color[node], "Human")
        


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

        elif MODE == "divide_conquer":
            temp = False
            while not temp:
                selected_color = dnc_pick_color(color)
                temp = apply_move(selected_color, "Computer")
        elif MODE == "dp":
            # selected_color = dp_pick_color(color)
            return
        else:
            return

        if MODE in ("greedy", "divide_conquer", "dp") and temp:
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


    # ---------------- UI SIDE PANEL ---------------- #

    Label(
        game_window,
        text=f"{MODE} Mode",
        bg="#282A36",
        fg="white",
        font=("Arial", 24, "bold")
    ).place(x=930, y=20, anchor="center")

    text_frame = Frame(game_window)
    text_frame.place(x=930, y=70, width=700, height=500, anchor="n")

    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text = Text(text_frame, yscrollcommand=scrollbar.set)
    text.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=text.yview)


    # ---------------- MODE INITIALIZATION ---------------- #

    if MODE == "human":
        canvas.bind("<ButtonRelease-1>", on_click)

    elif MODE in ("greedy", "divide_conquer", "dp"):
        game_window.after(COMPUTER_DELAY, computer_move)

    elif MODE == "alternate":
        canvas.bind("<ButtonRelease-1>", on_click)
        text.insert(END, "Alternate Mode: Human starts.\n")

    icon2 = PhotoImage(file="ingame_icon.png")
    iconlabel2 = Label(game_window, image=icon2, bg="#282A36")
    iconlabel2.image = icon2
    iconlabel2.place(x=700, y=70, anchor="sw")


    game_window.wait_window()