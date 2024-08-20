from customtkinter import *

set_default_color_theme("fabula.json")
from screeninfo import get_monitors

monitors = get_monitors()
for i, m in enumerate(monitors):
    print(i, str(m))
#choice = input("Please enter the window to be shown - ")
choice = "1"
width = 500
height = 500
posx = 0
posy = 0

try:
    width = monitors[int(choice)].width
    height = monitors[int(choice)].height
    posx = monitors[int(choice)].x
    posy = monitors[int(choice)].y

except Exception as e:
    print(e)
    print("An error occured. Changing to default 500x500")
print(f"{width}x{height}+{posx}+{posy}")

root = CTk()
root.title("Fabula Scoreboard")
root.overrideredirect(1)
root.overrideredirect(0)
root.geometry(f"{width}x{height}+{posx}+0")
scoreboard_height = 0
root.attributes("-fullscreen", True)

frame = CTkFrame(root)
frame.pack(expand=True)

root.mainloop()