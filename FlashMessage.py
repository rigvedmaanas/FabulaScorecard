import tkinter as tk
from overlay import Window
import hashlib
import threading
from screeninfo import get_monitors
import time
import json


def load_json(json_file):
    with open(json_file, 'r') as file:
        json_data = json.load(file)
    return json_data


monitors = get_monitors()
for i, m in enumerate(monitors):
    print(i, str(m))
choice = input("Please enter the window to be shown - ")
width = 500
height = 500
posx = 0
posy = 0
FLASH = "Welcome To Fabula"
last_hash_config = ""



def hash_check_config():
    global last_hash_config, FLASH
    f = open("FlashMessage.json", "r")

    current_hash_config = hashlib.sha256(f.read().encode()).hexdigest()
    f.close()
    if last_hash_config == "":
        last_hash_config = current_hash_config
    elif last_hash_config == current_hash_config:
        pass
    elif last_hash_config != current_hash_config:
        d = load_json("FlashMessage.json")
        FLASH = d[0]["Flash"]
        flash_message.itemconfigure(msg, text=FLASH)

        x1, y1, x2, y2 = flash_message.bbox(msg)
        #flash_message.move(msg, flash_message.winfo_width() + (x2 - x1), 0)
        flash_message.coords(msg, 0, 40 // 2 - 5)
        last_hash_config = current_hash_config

    time.sleep(2.0)
    try:
        hash_check_config()
        # print("Ok")
    except RecursionError as e:

        t11 = threading.Thread(target=hash_check_config)
        t11.start()


t1 = threading.Thread(target=hash_check_config)
t1.start()

try:
    width = monitors[int(choice)].width
    height = monitors[int(choice)].height
    posx = monitors[int(choice)].x
    posy = monitors[int(choice)].y

except Exception as e:
    print(e)
    print("An error occured. Changing to default 500x500")
print(f"{width}x{height}+{posx}+{posy}")
win = Window()
win.root.geometry(f"{width}x{60}+{posx}+{height - 60}")


def move_txt():
    global msg, canvas, msg2
    flash_message.move(msg, -1, 0)
    x1, y1, x2, y2 = flash_message.bbox(msg)
    if x1 < 0 - (x2 - x1):
        flash_message.move(msg, flash_message.winfo_width() + (x2 - x1), 0)
        win.root.update()

    win.after(10, move_txt)


flash_message = tk.Canvas(win.root, height=60, bg="#291954", highlightthickness=0)
flash_message.pack(side=tk.BOTTOM, fill="x")
d = load_json("FlashMessage.json")
FLASH = d[0]["Flash"]

msg = flash_message.create_text(flash_message.winfo_width() - 10, 70 // 2 - 5,
                                text=FLASH, fill="#ffca05",
                                font=('Chakra Petch', 40), anchor=tk.W)
move_txt()
Window.launch()
