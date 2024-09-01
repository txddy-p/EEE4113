from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, filedialog
import subprocess
import shutil

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Piwani\Desktop\school\Final Year\EEE4113_design\GUI_FINAL_DESIGN\Code\New folder\build\assets\frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_settings():
    subprocess.Popen(["python", "settings.py"])

def open_stats():
    subprocess.Popen(["python", "stats.py"])

def open_data():
    subprocess.Popen(["python", "data.py"])

def save_data():
    # Path to the file from ESP32
    file_path = "file_from_esp32.txt"

    # Ask user for save location
    save_location = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Save file as"
    )

    if save_location:
        try:
            # Copy the file to the user-specified location
            shutil.copy(file_path, save_location)
            print(f"File saved to {save_location}.")
        except Exception as e:
            print(f"Failed to save file: {e}")


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
    command=open_data,
    relief="flat"
)
button_1.place(x=301.0, y=151.0, width=280.0, height=56.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=save_data,
    relief="flat"
)
button_2.place(x=301.0, y=231.0, width=280.0, height=56.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=open_stats,
    relief="flat"
)
button_3.place(x=301.0, y=311.0, width=280.0, height=56.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=open_settings,
    relief="flat"
)
button_4.place(x=301.0, y=391.0, width=280.0, height=56.0)

window.resizable(False, False)
window.mainloop()
