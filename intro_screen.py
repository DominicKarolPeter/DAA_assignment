from tkinter import *
from PIL import Image, ImageTk

blue1 = "#000044"
blue2 = "#00b0f0"

SIZE = 10
MAX_MOVES = 25

SIZE_MIN, SIZE_MAX = 5, 200
MOVES_MIN, MOVES_MAX = 1, 200

def show_intro_screen(root):

    ###############################
    # CREATING INTRO WINDOW

    intro_window = Toplevel(root)
    intro_window.geometry(f"800x650+{intro_window.winfo_screenwidth()//2 - 400}+{intro_window.winfo_screenheight()//2 - 325}")
    intro_window.attributes("-topmost", True)
    #intro_window.attributes("-transparentcolor", "#00ff00")
    intro_window.overrideredirect(1)

    ###############################
    # BACKGROUND

    c = Canvas(intro_window, bg="#000044")
    c.pack(fill=BOTH, expand=1)

    bgimg = Image.open("assets/start_screen_new.png")
    bgimg = bgimg.resize((800, 650), Image.Resampling.LANCZOS)
    bgimg = ImageTk.PhotoImage(bgimg)

    c.create_image(0, 0, image=bgimg, anchor=NW)
    c.bgimg = bgimg  # Keep a reference to prevent garbage collection

    ###############################
    # VARIABLES
    
    result = {"action": 0, "size": SIZE, "moves": MAX_MOVES, "mode": "human"}

    size_var = IntVar(value=SIZE)
    moves_var = IntVar(value=MAX_MOVES)
    mode_var = StringVar(value="human")


    ######################################
    # SELECT SIZE AND MOVES

    size = Entry(intro_window, font="Arial 20", bg=blue2, fg="#ffffff", insertbackground="#ffffff", borderwidth=0, highlightthickness=0, textvariable=size_var, justify="center")
    size.place(x=470, y=195, width=210, height=55)
    moves = Entry(intro_window, font="Arial 20", bg=blue2, fg="#ffffff", insertbackground="#ffffff", borderwidth=0, highlightthickness=0, textvariable=moves_var, justify="center")
    moves.place(x=470, y=288, width=210, height=55)

    size_down = [(418, 207), (454, 207), (436, 235)]
    size_up = [(713, 203), (695, 232), (731, 232)]
    moves_down = [(418, 300), (454, 300), (436, 328)]
    moves_up = [(713, 300), (695, 330), (731, 330)]

    #######################################
    # SELECT MODE
    MODES = ["human", "backtracking", "greedy", "divide_conquer", "dp"]

    MODE_RECTS = [
        ((215, 385), (312, 510)),
        ((321, 385), (418, 510)),
        ((427, 385), (524, 510)),
        ((533, 385), (630, 510)),
        ((639, 385), (736, 510)),
    ]

    highlight_rect = None

    def highlight_mode(i):
        nonlocal highlight_rect
        if highlight_rect:
            c.delete(highlight_rect)

        (x1, y1), (x2, y2) = MODE_RECTS[i]
        highlight_rect = c.create_rectangle(
            x1, y1, x2, y2,
            outline=blue1, width=3
        )

    highlight_mode(0)  # Highlight the default mode

    ############################################
    # BINDING CLICK EVENTS

    def point_in_rect(px, py, x1, y1, x2, y2):
        return x1 <= px <= x2 and y1 <= py <= y2

    def point_in_triangle(px, py, a, b, c):
        def sign(p1, p2, p3):
            return (p1[0]-p3[0])*(p2[1]-p3[1]) - (p2[0]-p3[0])*(p1[1]-p3[1])

        b1 = sign((px, py), a, b) < 0
        b2 = sign((px, py), b, c) < 0
        b3 = sign((px, py), c, a) < 0

        return (b1 == b2) and (b2 == b3)

    def point_in_circle(px, py, cx, cy, r):
        return (px - cx)**2 + (py - cy)**2 <= r*r



    def on_canvas_click(event):
        x, y = event.x, event.y

        # -------- SIZE --------
        if point_in_triangle(x, y, *size_down):
            size_var.set(max(SIZE_MIN, size_var.get() - 1))
            return

        if point_in_triangle(x, y, *size_up):
            size_var.set(min(SIZE_MAX, size_var.get() + 1))
            return

        # -------- MOVES --------
        if point_in_triangle(x, y, *moves_down):
            moves_var.set(max(MOVES_MIN, moves_var.get() - 1))
            return

        if point_in_triangle(x, y, *moves_up):
            moves_var.set(min(MOVES_MAX, moves_var.get() + 1))
            return

        # -------- MODE --------
        for i, ((x1, y1), (x2, y2)) in enumerate(MODE_RECTS):
            if point_in_rect(x, y, x1, y1, x2, y2):
                mode_var.set(MODES[i])
                highlight_mode(i)
                return

            
        # -------- CLOSE --------
        if point_in_circle(x, y, 756, 43, 30):
            result["action"] = 0
            intro_window.destroy()
            return
        
        # -------- START GAME --------
        if point_in_rect(x, y, 160, 546, 646, 612) or point_in_circle(x, y, 158, 579, 33) or point_in_circle(x, y, 641, 579, 33):
            result["action"] = 1
            result["size"] = size_var.get()
            result["moves"] = moves_var.get()
            result["mode"] = mode_var.get()
            intro_window.destroy()
            return

    c.bind("<ButtonRelease-1>", on_canvas_click)
    intro_window.wait_window()
    return result

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Hide the main window while the intro screen is active
    result = show_intro_screen(root)
    print(result)