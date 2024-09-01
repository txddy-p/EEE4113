from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from tkinter import messagebox
import os
from ftplib import FTP

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Piwani\Desktop\school\Final Year\EEE4113_design\GUI_FINAL_DESIGN\Code\New folder\build\assets\frame4")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def reset_entries():
    entry_1.delete(0, 'end')
    entry_1.insert(0, "10")
    entry_2.delete(0, 'end')
    entry_2.insert(0, "10")
    entry_3.delete(0, 'end')
    entry_3.insert(0, "25")
    entry_4.delete(0, 'end')
    entry_4.insert(0, "45")

def validate_and_save():
    values = {
        'entry_1': entry_1.get(),
        'entry_2': entry_2.get(),
        'entry_3': entry_3.get(),
        'entry_4': entry_4.get()
    }
    
    try:
        float_values = {key: float(value) for key, value in values.items()}
    except ValueError:
        messagebox.showerror("Input Error", "All entries must be valid numbers.")
        return

    file_path = r"C:\Users\Piwani\Desktop\school\Final Year\EEE4113_design\GUI_FINAL_DESIGN\Code\settings_data.txt"
    with open(file_path, 'w') as file:
        for key, value in float_values.items():
            file.write(f"{key}: {value}\n")

    messagebox.showinfo("Success", "Data saved successfully.")

def send_file_to_esp32():
    file_path = r"C:\Users\Piwani\Desktop\school\Final Year\EEE4113_design\GUI_FINAL_DESIGN\Code\settings_data.txt"
    esp32_ip = "192.168.137.1"  # Replace with the ESP32 IP address
    ftp_user = "user"  # FTP user configured on the ESP32
    ftp_pass = "pass"  # FTP password configured on the ESP32
    
    try:
        ftp = FTP()
        ftp.connect(esp32_ip)
        ftp.login(ftp_user, ftp_pass)
        
        with open(file_path, 'rb') as file:
            ftp.storbinary(f"STOR settings_data.txt", file)
        
        ftp.quit()
        messagebox.showinfo("Success", "File sent to ESP32 successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send file: {e}")

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

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(374.0, 174.0, image=entry_image_1)
entry_1 = Entry(bd=0, bg="#523F38", fg="#000716", highlightthickness=0)
entry_1.place(x=356.0, y=155.0, width=36.0, height=36.0)
entry_1.insert(0, "10")  # Default value

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(591.0, 174.0, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#523F38", fg="#000716", highlightthickness=0)
entry_2.place(x=571.0, y=155.0, width=40.0, height=36.0)
entry_2.insert(0, "10")  # Default value

entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(591.0, 254.0, image=entry_image_3)
entry_3 = Entry(bd=0, bg="#523F38", fg="#000716", highlightthickness=0)
entry_3.place(x=571.0, y=235.0, width=40.0, height=36.0)
entry_3.insert(0, "25")  # Default value

entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(375.5, 254.0, image=entry_image_4)
entry_4 = Entry(bd=0, bg="#523F38", fg="#000716", highlightthickness=0)
entry_4.place(x=356.0, y=235.0, width=39.0, height=36.0)
entry_4.insert(0, "45")  # Default value

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (reset_entries()),
    relief="flat"
)
button_1.place(x=251.0, y=301.0, width=120.0, height=38.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (validate_and_save(), send_file_to_esp32()),
    relief="flat"
)
button_2.place(x=475.0, y=301.0, width=120.0, height=38.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Back to Home"),
    relief="flat"
)
button_3.place(x=8.0, y=14.0, width=48.0, height=48.0)

window.resizable(False, False)
window.mainloop()
