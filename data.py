from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Text, Scrollbar, Frame
from datetime import datetime
from tabulate import tabulate
import subprocess

# Paths to assets
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Piwani\Desktop\school\Final Year\EEE4113_design\GUI_FINAL_DESIGN\Code\New folder\build\assets\frame2")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

file_path = r"C:\Users\Piwani\Desktop\school\Final Year\EEE4113_design\GUI_FINAL_DESIGN\Code\data.txt"  # Path where data file is saved
data = []

# Open and read the file
with open(file_path, 'r') as file:
    for line in file:
        # Split the line by commas and strip whitespace
        elements = [e.strip() for e in line.split(',')]

        # Parse the elements from the line
        date_str = f"{elements[0]} {elements[1]}"
        date = datetime.strptime(date_str, "%A %B %d %Y %H:%M:%S")
        
        temp1 = float(elements[3])
        humd1 = float(elements[5])
        temp2 = float(elements[7])
        humd2 = float(elements[9])
        alarm = elements[11]

        # Append the parsed data to the list (array of arrays)
        data.append([date.strftime("%d/%m/%y %H:%M"), temp1, temp2, humd1, humd2, alarm])

# Create a formatted table using tabulate
headers = ["Date", "Temp1", "Temp2", "Humd1", "Humd2", "Alarm"]
table = tabulate(data, headers=headers, tablefmt="grid")

def open_home():
    # Close current window and open home window
    window.destroy()
    subprocess.run(["python", "home.py"])

def open_settings():
    # Open settings window
    subprocess.run(["python", "settings.py"])

window = Tk()
window.geometry("854x480")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=480,
    width=854,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(427.0, 240.0, image=image_image_1)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_home,
    relief="flat"
)
button_1.place(x=8.0, y=13.0, width=48.0, height=48.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=open_settings,
    relief="flat"
)
button_2.place(x=798.0, y=13.0, width=48.0, height=48.0)

# Create a frame for the table with a scrollbar
frame = Frame(window)
frame.place(x=50, y=80, width=750, height=360)

# Create a Text widget to display the table
text_widget = Text(frame, wrap="none")
text_widget.insert("1.0", table)
text_widget.config(state="disabled")

# Add a scrollbar to the text widget
scrollbar = Scrollbar(frame, command=text_widget.yview)
scrollbar.pack(side="right", fill="y")
text_widget.pack(side="left", fill="both", expand=True)
text_widget.config(yscrollcommand=scrollbar.set)

window.resizable(False, False)
window.mainloop()
