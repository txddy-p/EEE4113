import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider, CheckButtons
from datetime import datetime
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, ttk, filedialog

# File paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Piwani\Desktop\school\Final Year\EEE4113_design\GUI_FINAL_DESIGN\Code\New folder\build\assets\frame3")
DATA_FILE = r"C:\Users\Piwani\Desktop\school\Final Year\EEE4113_design\GUI_FINAL_DESIGN\Code\data.txt"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def calculate_stats(dataframe):
    # Calculate statistics
    stats = {}
    columns = ['temp1', 'humd1', 'temp2', 'humd2']
    for col in columns:
        stats[col] = {
            'mean': dataframe[col].mean(),
            'mode': dataframe[col].mode().iloc[0],
            'median': dataframe[col].median(),
            'range': dataframe[col].max() - dataframe[col].min(),
            'variance': dataframe[col].var(),
            'std_dev': dataframe[col].std()
        }
    return stats

def update_stats_on_gui(stats, treeview):
    # Clear the existing data in the treeview
    for row in treeview.get_children():
        treeview.delete(row)
    
    # Insert new data into the treeview
    rows = ['mean', 'mode', 'median', 'range', 'variance', 'std_dev']
    columns = ['temp1', 'humd1', 'temp2', 'humd2']
    for i, stat_name in enumerate(rows):
        values = [f"{stats[col][stat_name]:.2f}" for col in columns]
        treeview.insert('', 'end', values=[stat_name] + values)

def show_plot():
    # Read data from file
    data = []
    with open(DATA_FILE, 'r') as file:
        for line in file:
            elements = [e.strip() for e in line.split(',')]
            date_str = f"{elements[0]} {elements[1]}"
            date = datetime.strptime(date_str, "%A %B %d %Y %H:%M:%S")
            temp1 = float(elements[3])
            humd1 = float(elements[5])
            temp2 = float(elements[7])
            humd2 = float(elements[9])
            alarm = elements[11]
            data.append([date, temp1, humd1, temp2, humd2, alarm])

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['date', 'temp1', 'humd1', 'temp2', 'humd2', 'alarm'])
    
    # Calculate stats and update GUI
    stats = calculate_stats(df)
    update_stats_on_gui(stats, treeview)
    
    # Convert dates to ordinal
    dates = [d.toordinal() for d in df['date']]

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.subplots_adjust(bottom=0.35)
    
    # Initial plot with all data
    line1, = ax.plot(df['date'], df['temp1'], lw=2, label='Temperature 1')
    line2, = ax.plot(df['date'], df['temp2'], lw=2, label='Temperature 2')
    line3, = ax.plot(df['date'], df['humd1'], lw=2, label='Humidity 1')
    line4, = ax.plot(df['date'], df['humd2'], lw=2, label='Humidity 2')

    # Create check buttons
    lines_by_label = {
        'Temperature 1': line1,
        'Temperature 2': line2,
        'Humidity 1': line3,
        'Humidity 2': line4
    }
    rax = fig.add_axes([0.01, 0.1, 0.15, 0.15], frame_on=False)
    check = CheckButtons(
        ax=rax,
        labels=lines_by_label.keys(),
        actives=[line.get_visible() for line in lines_by_label.values()],
        label_props={'color': [line.get_color() for line in lines_by_label.values()]},
        frame_props={'edgecolor': [line.get_color() for line in lines_by_label.values()]},
        check_props={'facecolor': [line.get_color() for line in lines_by_label.values()]}
    )

    # Create the RangeSlider
    slider_ax = fig.add_axes([0.20, 0.1, 0.60, 0.03])
    slider = RangeSlider(
        slider_ax, 
        "Date Range", 
        min(dates), 
        max(dates), 
        valinit=(min(dates), max(dates))
    )

    # Update function
    def update(val):
        lower = datetime.fromordinal(int(val[0]))
        upper = datetime.fromordinal(int(val[1]))
        filtered_data = df[(df['date'] >= lower) & (df['date'] <= upper)]
        if not filtered_data.empty:
            line1.set_data(filtered_data['date'], filtered_data['temp1'])
            line2.set_data(filtered_data['date'], filtered_data['temp2'])
            line3.set_data(filtered_data['date'], filtered_data['humd1'])
            line4.set_data(filtered_data['date'], filtered_data['humd2'])
            ax.set_xlim(lower, upper)
            ax.relim()
            ax.autoscale_view()
        fig.canvas.draw_idle()

    def toggle_lines(label):
        line = lines_by_label[label]
        line.set_visible(not line.get_visible())
        ax.figure.canvas.draw_idle()

    # Connect events
    check.on_clicked(toggle_lines)
    slider.on_changed(update)

    plt.show()

def save_data():
    # Open file dialog to select file to save data
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        # Assume df is your DataFrame and save it to the selected file
        df.to_csv(file_path, index=False)

def go_to_settings():
    # Function to go to settings
    print("Navigating to settings...")

def go_home():
    # Function to go back home
    print("Going home...")

window = Tk()

window.geometry("854x480")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 480,
    width = 854,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    427.0,
    240.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=save_data,
    relief="flat"
)
button_1.place(
    x=661.0,
    y=401.0,  # Adjusted y to avoid overlap
    width=179.0,
    height=56.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=go_home,
    relief="flat"
)
button_2.place(
    x=8.0,
    y=14.0,
    width=48.0,
    height=48.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=go_to_settings,
    relief="flat"
)
button_3.place(
    x=798.0,
    y=14.0,
    width=48.0,
    height=48.0
)

# Create a treeview for displaying stats
treeview = ttk.Treeview(
    window,
    columns=('Stat', 'temp1', 'humd1', 'temp2', 'humd2'),
    show='headings',
    height=10
)
treeview.heading('Stat', text='Stat')
treeview.heading('temp1', text='Temp1')
treeview.heading('humd1', text='Humd1')
treeview.heading('temp2', text='Temp2')
treeview.heading('humd2', text='Humd2')

treeview.column('Stat', width=150)
treeview.column('temp1', width=150)
treeview.column('humd1', width=150)
treeview.column('temp2', width=150)
treeview.column('humd2', width=150)

treeview.place(x=10, y=60, width=640, height=350)  # Position it so it doesn't overlap with buttons

# Button to show plot
plot_button = Button(
    window,
    text="Show Plot",
    command=show_plot,
    borderwidth=0,
    relief="flat",
    bg="#00FF00"  # Green background
)
plot_button.place(
    x=700.0,
    y=60.0,  # Position the button
    width=130.0,
    height=30.0
)

window.resizable(False, False)
window.mainloop()
