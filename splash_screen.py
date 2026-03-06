from tkinter import *
from PIL import Image, ImageTk

def show_splash_screen(root: Tk):
    curr = 0
    size = (600, 350)
    def shift():
        nonlocal curr
        if curr < size[0]+115:
            curr += 10
            c.coords(fg_image_obj, curr, 0)
            splash_screen.after(20, shift)
    end_phase = 0
    def ending():
        nonlocal end_phase
        if end_phase == 0:
                c.create_text(size[0]//2, size[1]//2, text="Flood-It!", font=("Luckiest Guy", 98), anchor="center", fill="#ffffff")
                c.create_text(size[0]//2, size[1]//2, text="Flood-It!", font=("Luckiest Guy", 94), anchor="center", fill="#FFFFFF")
                c.create_text(size[0]//2, size[1]//2, text="Flood-It!", font=("Luckiest Guy", 96), anchor="center", fill="#036FA4")
                end_phase += 1
                splash_screen.after(1500, ending)
        elif end_phase == 1:
             end_phase += 1
             c.create_text(size[0]//2+100, size[1]//2+100, text="Loading...", font="calibri 40 bold", anchor="center", fill="#ffffff")
             splash_screen.after(2500, ending)
        else:
             splash_screen.destroy()
    splash_screen = Toplevel(root)
    splash_screen.geometry(f"{size[0]}x{size[1]}+{splash_screen.winfo_screenwidth()//2 - size[0]//2}+{splash_screen.winfo_screenheight()//2 - size[1]//2}")
    splash_screen.attributes("-topmost", True)
    splash_screen.overrideredirect(1)

    c = Canvas(splash_screen, bg="#000044")
    c.pack(fill=BOTH, expand=1)

    bgimg = Image.open("assets/splash_screen_bg.png")
    bgimg = bgimg.resize(size, Image.Resampling.LANCZOS)
    bgimg = ImageTk.PhotoImage(bgimg)
    fgimg = Image.open("assets/splash_screen_fg.png")
    fgimg = fgimg.resize((750, 350), Image.Resampling.LANCZOS)
    fgimg = ImageTk.PhotoImage(fgimg)

    c.create_image(0, 0, image=bgimg, anchor=NW)
    fg_image_obj = c.create_image(0, 0, image=fgimg, anchor=NE)
    c.bgimg = bgimg  # Keep a reference to prevent garbage collection
    c.fgimg = fgimg  # Keep a reference to prevent garbage collection
    shift()
    root.after(2500, ending)
    root.wait_window(splash_screen)


if __name__ == "__main__":
    root = Tk()
    show_splash_screen(root)
    root.mainloop()