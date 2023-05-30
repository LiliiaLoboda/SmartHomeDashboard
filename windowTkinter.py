import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fileUtils import write_thresholds_to_file, load_file_without_session


def button_click():
    print("Input 1:", entry1.get())
    print("Input 2:", entry2.get())
    write_thresholds_to_file(entry2.get(), entry1.get())

window = tk.Tk()
window.geometry("890x690")

window.title("Window from Liliia Loboda")

initial_values = load_file_without_session()

entry1 = tk.Entry(window)
entry1.insert(0, str(initial_values.get("lowerThreshold")))
entry2 = tk.Entry(window)
entry2.insert(0, str(initial_values.get("upperThreshold")))


button = tk.Button(window, text="Save", command=button_click, width=10, height=2)

entry1_label = tk.Label(window, text="Enter lower Threshold:", font=("Arial", 16))
entry2_label = tk.Label(window, text="Enter upper Threshold:", font=("Arial", 16))

# Create the chart figure and canvas
figure = plt.Figure(figsize=(8, 6))
canvas = FigureCanvasTkAgg(figure, master=window)

# Create the chart plot
temperature_data = []  # Store the temperature data
ax = figure.add_subplot(111)
ax.plot(temperature_data, marker='o')
ax.set_title("Temperature Chart")
ax.set_xlabel("Time")
ax.set_ylabel("Temperature")

entry1_label.grid(row=0, column=0)
entry2_label.grid(row=1, column=0)
entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)
button.grid(row=2, column=0)


def start_tinker():
    window.mainloop()
