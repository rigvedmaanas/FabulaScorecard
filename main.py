import itertools
import time
from customtkinter import *
from PIL import Image
import threading
import hashlib

import json
from screeninfo import get_monitors

monitors = get_monitors()
for i, m in enumerate(monitors):
    print(i, str(m))
#choice = input("Please enter the window to be shown - ")
choice = "0"
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


set_appearance_mode("dark")
set_default_color_theme("fabula.json")
last_hash = ""
last_hash_config = ""
def load_json(json_file):
    with open(json_file, 'r') as file:
        json_data = json.load(file)
    return json_data

def refresh():
    global scores, scoreboard, num
    file = load_json("TestSchoolData/New_list-2024.json")
    print(file)
    print(scores)



    for data in itertools.zip_longest(scores, file):

        if data[0] == None:
            score = CTkFrame(scoreboard, height=75, width=scoreboard_width - 10)
            score.place(y=num, relx=0.5, anchor=CENTER)
            d = data[1]
            print("data[0] == None", d)
            add_data(score, d["Rank"], d["School Name"], d["Score"])
            scores.append(score)
            num += 75 + 10
        else:


            children = data[0].winfo_children()

            #Rank
            children[0].configure(text=data[1]["Rank"])

            # School Name
            children[1].configure(text=data[1]["School Name"])

            # Score
            children[2].configure(text=data[1]["Score"])

    d = load_json("Config.json")
    print(d)
    if d[2]["Show Participants Only"]:
        show_participants(True)

    elif not d[2]["Show Participants Only"]:
        show_participants(False)

def hash_check():
    global last_hash
    f = open("TestSchoolData/New_list-2024.json", "r")

    current_hash = hashlib.sha256(f.read().encode()).hexdigest()
    if last_hash == "":
        last_hash = current_hash
        print("Starting First")
    elif last_hash == current_hash:
        pass
    elif last_hash != current_hash:
        print(last_hash, current_hash)
        print("No Match")
        print(load_json("TestSchoolData/New_list-2024.json"))
        refresh()
        last_hash = current_hash

    f.close()

    time.sleep(2.0)
    try:
        hash_check()
        #print("Ok")
    except RecursionError as e:

        t10 = threading.Thread(target=hash_check)
        t10.start()


t5 = threading.Thread(target=hash_check)
t5.start()

def hash_check_config():
    global last_hash_config
    f = open("Config.json", "r")
    current_hash_config = hashlib.sha256(f.read().encode()).hexdigest()
    if last_hash_config == "":
        last_hash_config = current_hash_config
    elif last_hash_config == current_hash_config:
        pass
    elif last_hash_config != current_hash_config:
        d = load_json("Config.json")
        if d[1]["Winners"]:
            show_winners(True)
        elif not d[1]["Winners"]:
            show_winners(False)
        if d[2]["Show Participants Only"]:
            show_participants(True)

        elif not d[2]["Show Participants Only"]:
            show_participants(False)
        else:
            pass
        last_hash_config = current_hash_config

    f.close()

    time.sleep(2.0)
    try:
        hash_check_config()
        #print("Ok")
    except RecursionError as e:

        t11 = threading.Thread(target=hash_check_config)
        t11.start()



t6 = threading.Thread(target=hash_check_config)
t6.start()

delete_winners_frame = []
def show_winners(Show):
    global delete_winners_frame
    if Show:
        root.update()
        data = load_json("TestSchoolData/New_list-2024.json")

        coverup_frame = CTkFrame(scoreboardMaster, width=scoreboardMaster.winfo_width(),
                                 height=scoreboardMaster.winfo_height(), corner_radius=0)
        coverup_frame.place(x=0, y=0)
        OverAll_Title = CTkLabel(scoreboardMaster, text="Overall Winner", font=("Chakra Petch", 30), bg_color="#291954")
        OverAll_Title.place(relx=0.5, rely=0.15, anchor=CENTER)
        OverAll = CTkLabel(scoreboardMaster, text=data[0]["School Name"], font=("Chakra Petch", 40), wraplength=500, bg_color="#291954")
        OverAll.place(relx=0.5, rely=0.25, anchor=CENTER)

        OverAllRunner_Title = CTkLabel(scoreboardMaster, text="Overall Runner Up", font=("Chakra Petch", 30), bg_color="#291954")
        OverAllRunner_Title.place(relx=0.5, rely=0.55, anchor=CENTER)
        OverAllRunner = CTkLabel(scoreboardMaster, text=data[1]["School Name"], font=("Chakra Petch", 40), wraplength=500, bg_color="#291954")
        OverAllRunner.place(relx=0.5, rely=0.7, anchor=CENTER)

        delete_winners_frame.append(coverup_frame)
        delete_winners_frame.append(OverAll_Title)
        delete_winners_frame.append(OverAll)
        delete_winners_frame.append(OverAllRunner_Title)
        delete_winners_frame.append(OverAllRunner)

    else:
        for widget in delete_winners_frame:
            widget.destroy()




root = CTk()
root.title("Fabula Scoreboard")
root.overrideredirect(1)
root.overrideredirect(0)
root.geometry(f"{width}x{height}+{posx}+0")
scoreboard_height = 0
root.attributes("-fullscreen", True)
num2 = 50.0
onum = num2
stop = True
def add_data(frame, rank="Rank", school_name="School Name", score="Score", x1=0.075, x2=0.915):
    #Rank School Name Score
    if rank == "Rank" and school_name == "School Name" and score == "Score":
        font = ("Chakra Petch Bold", 30)
    else:
        font = ("Chakra Petch", 20)
    rank_txt = CTkLabel(frame, text=rank, font=font)
    rank_txt.place(relx=x1, rely=0.5, anchor=CENTER)

    SchoolName_txt = CTkLabel(frame, text=school_name, font=font)
    SchoolName_txt.place(relx=0.50, rely=0.5, anchor=CENTER)

    Score_txt = CTkLabel(frame, text=score, font=font)
    Score_txt.place(relx=x2, rely=0.5, anchor=CENTER)

delay_called = False

start_time = 0
end_time = 0


def delay(sec):
    global start_time, end_time, delay_called
    if not delay_called:
        start_time = time.time()
        delay_called = True
    else:
        if time.time() - start_time > 3:
            start_time = 0
            end_time = 0
            delay_called = False
            return True
        else:
            return False

def looping_update():
    while True:
        root.update()

sleeping = False

fullStop = False
def set_stop_false():
    global stop
    stop = False
def auto_scroll():
    global scoreboard_height
    global num2, scores, onum, stop, finish, fullStop, sleeping
    if not fullStop:
        if float(scores[0].place_info()["y"]) > 0 and stop:
            sleeping = True
            time.sleep(3)
            sleeping = False
            stop = False

        if float(scores[-1].place_info()["y"]) < scoreboard_height - 50 and not stop:
            sleeping = True
            time.sleep(3)
            sleeping = False
            d = load_json("Config.json")
            if d[0]["Leading"] == True:
                stop = True
                onum = 50.0
                fullStop = True
                finish = False

                show_leading()
            else:
                stop = True
                onum = 50.0
                fullStop = False
                finish = True


        for score in scores:
            y = float(score.place_info()["y"])
            score.place(relx=0.5, y=num2)
            num2 += 75 + pady
        onum -= 10.5
        #onum -= 50.0
        num2 = onum
        root.update()
    root.after(1, auto_scroll)

anim_leading = 0
anim_school = 0
last_anim_school = anim_school
finish = False

pos = 1
def animate_text(leading_text_animFrame, school_text_animFrame, leading_text, school_text):
    global anim_leading, anim_school, finish, pos, fullStop
    anim_leading -= 2.0
    anim_school += 10.0
    leading_text_animFrame.place(x=0, y=anim_leading)
    school_text_animFrame.place(x=0, y=anim_school)
    if anim_leading < -100 and anim_school > 500:
        anim_school = last_anim_school
        anim_leading = 0
        sleeping = True
        time.sleep(3)
        sleeping = False
        pos += 1
        if pos > 3:
            for widget in delete_frames:
                widget.destroy()
            finish = True
            fullStop = False
            pos = 1
        else:
            if pos == 3:
                leading_text.configure(text=f"Leading in {pos}rd Position", bg_color="#291954")
            else:
                leading_text.configure(text=f"Leading in {pos}nd Position", bg_color="#291954")

            d = load_json("TestSchoolData/New_list-2024.json")
            school_text.configure(text=f"{d[pos-1]['School Name']}\n\n{d[pos-1]['Score']} Points", bg_color="#291954")



    if not finish:
        root.after(10, lambda: animate_text(leading_text_animFrame, school_text_animFrame , leading_text, school_text))
delete_frames = []
def show_leading():
    global delete_frames
    global anim_school, last_anim_school
    delete_frames = []
    root.update()
    coverup_frame = CTkFrame(scoreboardMaster, width=scoreboardMaster.winfo_width(), height=scoreboardMaster.winfo_height(), corner_radius=0)
    coverup_frame.place(x=0, y=0)
    print("Covering")
    leading_text = CTkLabel(scoreboardMaster, text="Leading in 1st position", font=("Chakra Petch", 50), bg_color="#291954")
    leading_text.place(relx=0.5, rely=0.3, anchor=CENTER)
    d = load_json("TestSchoolData/New_list-2024.json")

    School_text = CTkLabel(scoreboardMaster, text=f"{d[0]['School Name']}\n\n{d[0]['Score']} Points", font=("Chakra Petch", 35), wraplength=600 , bg_color="#291954")
    School_text.place(relx=0.5, rely=0.55, anchor=CENTER)
    leading_text_animFrame = CTkFrame(scoreboardMaster, width=scoreboardMaster.winfo_width(), height=scoreboardMaster.winfo_height()//2-100, bg_color="#291954")
    leading_text_animFrame.place(x=0, y=0)
    school_text_animFrame = CTkFrame(scoreboardMaster, width=scoreboardMaster.winfo_width(),
                                      height=scoreboardMaster.winfo_height() // 2, bg_color="#291954")
    school_text_animFrame.place(x=0, y=scoreboardMaster.winfo_height() // 2-100)
    anim_school = scoreboardMaster.winfo_height() // 2-100
    last_anim_school = anim_school
    delete_frames.append(coverup_frame)
    delete_frames.append(leading_text)
    delete_frames.append(School_text)
    delete_frames.append(leading_text_animFrame)
    delete_frames.append(school_text_animFrame)



    t2 = threading.Thread(target=animate_text, args=(leading_text_animFrame, school_text_animFrame, leading_text, School_text))
    t2.start()

    root.update()





frame = CTkFrame(root, width=900)
frame.pack(padx=20, pady=(20, 50), expand=True, fill="both")
frame.pack_propagate()
root.img = CTkImage(light_image=Image.open("ScoreCard2k24-01.png"), dark_image=Image.open("ScoreCard2k24-01.png"), size=(756, 104))

score_img = CTkLabel(frame, text="", image=root.img)
score_img.pack(pady=10, padx=10)

scoreboardMaster = CTkFrame(frame)
scoreboardMaster.pack(padx=20, pady=(0, 20), expand=True, fill="both")

score_title = CTkFrame(scoreboardMaster, height=75)
score_title.pack(padx=10, pady=(10, 0), fill="x")
add_data(score_title, x1=0.08, x2=0.91)

border_replica = CTkFrame(scoreboardMaster)
border_replica.pack(padx=10, pady=10, expand=True, fill="both")
scoreboard = CTkFrame(border_replica, fg_color=border_replica.cget("fg_color"))
scoreboard.pack(padx=5, pady=5, expand=True, fill="both")
root.update()
scoreboard_height = scoreboard.winfo_height()
scoreboard_width = scoreboard.winfo_width()
scores = []
num = 50
padx = 10
pady = 10
file = load_json("TestSchoolData/New_list-2024.json")
for x in range(file[-1]["Rank"]):
    score = CTkFrame(scoreboard, height=75, width=scoreboard_width-10)
    score.place(y=num, relx=0.5, anchor=CENTER)
    d = file[x]
    add_data(score, d["Rank"], d["School Name"], d["Score"])
    scores.append(score)
    num += 75 + pady

def show_participants(yn):
    if yn:
        for y in score_title.winfo_children():
            if y.cget("text") in ["Rank", "Score"]:
                y.configure(text_color="#291954")
            else:
                y.configure(text="Participants")
        for x in scoreboard.winfo_children():
            for items in x.winfo_children():

                try:
                    m = int(items.cget("text"))

                    items.configure(text_color="#444d9f")
                except ValueError as e:
                    pass

    else:
        for y in score_title.winfo_children():
            if y.cget("text") in ["Rank", "Score"]:
                y.configure(text_color="#ffca05")
            else:
                y.configure(text="School Name")
        for x in scoreboard.winfo_children():
            for items in x.winfo_children():

                try:
                    m = int(items.cget("text"))

                    items.configure(text_color="#ffca05")
                except ValueError as e:
                    pass


#t100 = threading.Thread(target=move_txt, args=())
#t100.start()
t1 = threading.Thread(target=auto_scroll, args=())
t1.start()
d = load_json("Config.json")
print(d)
if d[1]["Winners"]:
    show_winners(True)
elif not d[1]["Winners"]:
    show_winners(False)
if d[2]["Show Participants Only"]:
    show_participants(True)

elif not d[2]["Show Participants Only"]:
    show_participants(False)
#show_leading()
root.mainloop()


