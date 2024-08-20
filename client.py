from customtkinter import *
from tkinter import messagebox
import csv
import json
from screeninfo import get_monitors

FlashMessageShown = False
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

def sort_json(json_data):
    sorted_data = sorted(json_data, key=lambda x: (-int(x['Score']), x['School Name']))
    return sorted_data


schools = []


def get_schools():
    global schools
    schools = []
    for school in data:
        schools.append(school["School Name"])

def find_dict_by_school_name(list_of_dicts, school_name):
    for i, dictionary in enumerate(list_of_dicts):
        if dictionary.get('School Name') == school_name:
            return (i, dictionary)
    return None

def change_score(school_name, score):
    global data
    #if messagebox.askyesno("Warning", "Are you sure you want to do this action?"):
    if True:
        print(school_name, score)
        index, info = find_dict_by_school_name(data, school_name)
        data[index]["Score"] = str(int(info["Score"]) + int(score))
        data = sort_json(data)
        for i, x in enumerate(range(1, len(data) + 1)):
            data[i]["Rank"] = int(x)
        print(data)
        save_json(data, "TestSchoolData/New_list-2024.json")

def register_school(school_name):
    global data
    #if messagebox.askyesno("Warning", "Are you sure you want to do this action?"):
    if True:
        data.append({"Rank": int(int(data[-1]["Rank"]) + 1), "School Name": school_name, "Score": "0"})
        data = sort_json(data)
        for i, x in enumerate(range(1, len(data) + 1)):
            data[i]["Rank"] = int(x)
        print(data)
        save_json(data, "TestSchoolData/New_list-2024.json")
        get_schools()
        School_dropdown.configure(values=schools)



def save_json(json_data, file_path):
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)


def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        print(rows)

    for val in rows:
        print(val)
        val["Rank"] = int(float(val["Rank"]))
        val["Score"] = int(float(val["Score"]))
        val["School Name"] = val["School Name"].upper()


    # Convert CSV data to JSON
    json_data = json.dumps(rows, indent=4)

    # Write the JSON data to a file
    with open(json_file, 'w') as file:
        file.write(json_data)


# Provide the paths for the CSV and JSON files
csv_file_path = 'TestSchoolData/list_of_schools_2024.csv'
json_file_path = 'TestSchoolData/New_list-2024.json'
csv_to_json(csv_file_path, json_file_path)

def load_json(json_file):
    with open(json_file, 'r') as file:
        json_data = json.load(file)
    return json_data


data = load_json("TestSchoolData/New_list-2024.json")
print(data)

set_appearance_mode("dark")
set_default_color_theme("fabula.json")

root = CTk()

root.title("Fabula Scoreboard Client")
root.geometry("900x900+950+50")
root.overrideredirect(1)
root.overrideredirect(0)
root.geometry(f"{width}x{height}+{posx}+0")
#root.attributes("-fullscreen", True)

class Spinbox(CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size=1,
                 command=None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        #self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = CTkButton(self, text="–", width=height - 6, height=height - 6,
                                         command=self.subtract_button_callback, font=("Chakra Petch", 30))
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = CTkEntry(self, width=width - (2 * height), height=height-6, border_width=0, justify='center', font=("Chakra Petch", 30))
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = CTkButton(self, text="+", width=height - 6, height=height - 6,
                                    command=self.add_button_callback, font=("Chakra Petch", 30))
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "5")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self):
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))


tabview = CTkTabview(root)
tabview.pack(padx=20, pady=20, expand=True, fill=BOTH)

tabview.add("General")
tabview.add("Change Flash Message")  # add tab at the end
tabview.add("Change Scoreboard")  # add tab at the end
tabview.add("Register New School")  # set currently visible tab
tabview.set("General")

def switch_event():
    global last_winner, last_leading
    config = load_json("Config.json")
    #print(leading_var.get())
    # When Winners are shown Make leading False
    if show_winners_var.get() and leading_var.get():

        if last_winner != show_winners_var.get():

            leading_var.set(not leading_var.get())
            last_winner = show_winners_var.get()

        if last_leading != leading_var.get():
            show_winners_var.set(not show_winners_var.get())
            last_leading = leading_var.get()



    if last_winner != show_winners_var.get():
        leading_var.set(not leading_var.get())
        last_winner = show_winners_var.get()

    if last_leading != leading_var.get():
        show_winners_var.set(not show_winners_var.get())
        last_leading = leading_var.get()
    config[0]["Leading"] = leading_var.get()
    config[1]["Winners"] = show_winners_var.get()
    save_json(config, "Config.json")
    print("Leading Schools Show is ", leading_var.get())
    print("Winners Toggle is ", show_winners_var.get())


def toggle_winners():
    if show_winners_var.get() == True and leading_var.get() == True:
        leading_var.set(False)

    save_general()

def save_general():
    config = load_json("Config.json")
    config[0]["Leading"] = leading_var.get()
    config[1]["Winners"] = show_winners_var.get()
    config[2]["Show Participants Only"] = show_participants_var.get()
    save_json(config, "Config.json")

def toggle_leading():

    if leading_var.get() == True and show_winners_var.get() == True:
        show_winners_var.set(False)

    save_general()

def toggle_participants():

    save_general()

"""
    General Tab
"""

general = CTkFrame(tabview.tab("General"), width=500, height=300)
general.place(relx=0.5, rely=0.5, anchor=CENTER)
general.pack_propagate(False)
d = load_json("Config.json")
last_leading = d[0]["Leading"]
last_winner = d[1]["Winners"]
show_participants = d[2]["Show Participants Only"]

leading_var = BooleanVar(value=d[0]["Leading"])
info = CTkLabel(general, text="'Show Leading Schools' and 'Show Winners' cannot be ON together. Either one of them should be off. If one is turned on then the other will turned off. Both can be kept off.", wraplength=450)
info.pack(pady=(30, 10))
leading_switch = CTkSwitch(general, text="Show Leading Schools", command=toggle_leading,
                                 variable=leading_var, onvalue=True, offvalue=False, font=("Chakra Petch", 30), switch_width=70, switch_height=35)
leading_switch.pack(padx=10, pady=(0, 10))

show_winners_var = BooleanVar(value=d[1]["Winners"])
show_winners = CTkSwitch(general, text="Show Winners", command=toggle_winners,
                                 variable=show_winners_var, onvalue=True, offvalue=False, font=("Chakra Petch", 30), switch_width=70, switch_height=35)
show_winners.pack(padx=10, pady=(0, 10))

show_participants_var = BooleanVar(value=d[2]["Show Participants Only"])
show_participants = CTkSwitch(general, text="Show Participants Only", command=toggle_participants,
                                 variable=show_participants_var, onvalue=True, offvalue=False, font=("Chakra Petch", 30), switch_width=70, switch_height=35)
show_participants.pack(padx=10, pady=(0, 10))

"""
    Change Flash Message Tab
"""
window_opened = False
def create_new_flash(flash):
    #if messagebox.askyesno("Warning", "Are you sure you want to do this action?"):
    if True:
        f = load_json("FlashMessage.json")
        f[0]["Flash"] = flash
        save_json(f, "FlashMessage.json")

window_opened = False
view = ""
def on_closing():
    global window_opened, view
    window_opened = False
    view.destroy()

def view_flash():
    global window_opened, view
    f = load_json("FlashMessage.json")

    #messagebox.showinfo("Flash text", f[0]["Flash"])
    if not window_opened:
        f = load_json("FlashMessage.json")
        view = CTkToplevel(root)
        view.attributes("-topmost", True)
        view.title("Current Flash Message")
        #view.geometry(f"{width}x{height}+{posx}+{height - (height//2)}")
        view.protocol("WM_DELETE_WINDOW", on_closing)
        lbl = CTkLabel(view, text=f[0]["Flash"], wraplength=500)
        lbl.pack(padx=10, pady=10)
        view.update()
        view.geometry(f"{view.winfo_width()}x{view.winfo_height()}+{posx+(width//2-(view.winfo_width()//2))}+{height//2-(view.winfo_height()//2)}")
        window_opened = True


flash_message_tab = CTkFrame(tabview.tab("Change Flash Message"), width=500, height=190)
flash_message_tab.place(relx=0.5, rely=0.5, anchor=CENTER)
flash_message_tab.pack_propagate(False)

Show_Current_Flash_MessageBTN = CTkButton(flash_message_tab, text="View Current Flash Message", height=50, font=("Chakra Petch", 30), command=view_flash)
Show_Current_Flash_MessageBTN.pack(padx=10, pady=10, fill="x")

New_Flash = CTkEntry(flash_message_tab, placeholder_text="Enter New Flash Message", font=("Chakra Petch", 30), height=50)
New_Flash.pack(pady=(0, 10), fill="x", padx=10)

Set_Flash_Message = CTkButton(flash_message_tab, text="Set Flash Message", height=50, font=("Chakra Petch", 30), command=lambda: create_new_flash(New_Flash.get()))
Set_Flash_Message.pack(padx=10, pady=(0, 10), fill="x")

"""
    Register New School Tab
"""

register = CTkFrame(tabview.tab("Register New School"), width=500, height=200)
register.place(relx=0.5, rely=0.5, anchor=CENTER)
register.pack_propagate(False)
school_text = CTkLabel(register, text="School Name", height=50, font=("Chakra Petch", 30))
school_text.pack(padx=10, pady=(10, 0), fill="x")
School_name = CTkEntry(register, placeholder_text="Enter School Name", height=50, font=("Chakra Petch", 30))
School_name.pack(padx=10, pady=10, fill="x")
Register_btn = CTkButton(register, text="Register", height=50, command=lambda: register_school(School_name.get()), font=("Chakra Petch", 30))
Register_btn.pack(padx=10, pady=(0, 10), fill="x")

"""
    Change Scoreboard Tab
"""

change_scoreboard_frame = CTkFrame(tabview.tab("Change Scoreboard"), width=500, height=330)
change_scoreboard_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
change_scoreboard_frame.pack_propagate(False)
school_text = CTkLabel(change_scoreboard_frame, text="Choose School", height=50, font=("Chakra Petch", 30))
school_text.pack(padx=10, pady=(10, 0), fill="x")
get_schools()
School_dropdown = CTkOptionMenu(change_scoreboard_frame, values=schools, height=50, font=("Chakra Petch", 30))
School_dropdown.pack(padx=10, pady=10, fill="x")
info_text = CTkLabel(change_scoreboard_frame, text="Negative values for subtracting score \nPositive values for adding score", height=50, font=("Chakra Petch", 20))
info_text.pack(padx=10, pady=10, fill="x")
score = Spinbox(change_scoreboard_frame, height=50)
score.pack(padx=10, pady=(0, 10), fill="x")
Register_btn = CTkButton(change_scoreboard_frame, text="Update Scoreboard", height=50, font=("Chakra Petch", 30), command=lambda : change_score(School_dropdown.get(), score.get()))
Register_btn.pack(padx=10, pady=(0, 10), fill="x")

root.mainloop()
