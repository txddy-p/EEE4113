from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from ftplib import FTP
import subprocess
import time
import os

# Paths to assets
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Piwani\Desktop\school\Final Year\EEE4113_design\GUI_FINAL_DESIGN\Code\New folder\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def create_AP():
    # Function to create a Wi-Fi hotspot on Windows
    hotspot_name = "esp32B7DCA0"
    hotspot_password = "123456789"
    
    # Command to create a Wi-Fi hotspot
    subprocess.run([
        "netsh", "wlan", "set", "hostednetwork", 
        f"mode=allow", f"ssid={hotspot_name}", f"key={hotspot_password}"
    ], check=True)
    
    # Start the Wi-Fi hotspot
    subprocess.run(["netsh", "wlan", "start", "hostednetwork"], check=True)

    print(f"Hotspot '{hotspot_name}' started.")

def download_file_from_esp32():
    esp32_ip = "192.168.137.1"  # Replace with the ESP32 IP address
    file_name = "file_from_esp32.txt"  # Desired name for the downloaded file
    ftp_user = "user"  # FTP user configured on the ESP32
    ftp_pass = "pass"  # FTP password configured on the ESP32
    
    try:
        # Connect to the FTP server
        ftp = FTP()
        ftp.connect(esp32_ip)
        ftp.login(ftp_user, ftp_pass)
        
        # Define the path for saving the file in the current working directory
        current_directory = os.getcwd()
        file_path = Path(current_directory) / file_name
        
        # Download the file
        with open(file_path, 'wb') as file:
            ftp.retrbinary(f"RETR yourfile.txt", file.write)
        
        ftp.quit()
        print(f"File downloaded to {file_path}.")
    except Exception as e:
        print(f"Failed to download file: {e}")

def open_home():
    # Close current window and open home window
    window.destroy()
    import home  # Import home module
    home.show_home()  # Call the function to show home window

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
    command=lambda: (create_AP(), time.sleep(10), download_file_from_esp32(), open_home()),
    relief="flat"
)
button_1.place(x=287.0, y=290.0, width=280.0, height=56.0)

window.resizable(False, False)
window.mainloop()
