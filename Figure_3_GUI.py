import tkinter as tk
from tkinter import ttk, colorchooser
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data = pd.read_csv('Maintenance_Data.csv')

fault_columns = ['TWF', 'HDF', 'PWF', 'OSF', 'RNF']

numerical_columns = ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']

box_plot_color = "#ffffff"

def update_sliders(*args):
    global y_min_scale, y_max_scale

    selected_column = y_axis_var.get()
    y_min = data[selected_column].min()
    y_max = data[selected_column].max()

    y_min_scale.config(from_=y_min, to=y_max)
    y_min_scale.set(y_min)

    y_max_scale.config(from_=y_min, to=y_max)
    y_max_scale.set(y_max)

def update_box_plot():
    global box_plot_color

    column = y_axis_var.get()
    y_min = y_min_scale.get()
    y_max = y_max_scale.get()

    fig.clear()
    ax = fig.add_subplot(111)
    for fault in fault_columns:
        subset = data[(data[fault] == 1) & (data[column] >= y_min) & (data[column] <= y_max)]
        ax.boxplot(subset[column], positions=[fault_columns.index(fault)], widths=0.6, patch_artist=True, boxprops=dict(facecolor=box_plot_color))
    ax.set_xticks(range(len(fault_columns)))
    ax.set_xticklabels(fault_columns)
    ax.set_ylim(y_min, y_max)
    ax.set_ylabel(column)
    ax.set_title('Box plot of Fault Types vs. ' + column)
    canvas.draw()

def choose_color():
    global box_plot_color

    color_code = colorchooser.askcolor(title="Choose Box Plot Color")
    if color_code[1] is not None:
        box_plot_color = color_code[1]
        update_box_plot()


root = tk.Tk()
root.title("Interactive Box Plot")

y_axis_var = tk.StringVar(root)
y_axis_var.trace("w", update_sliders)
y_axis_dropdown = ttk.Combobox(root, textvariable=y_axis_var, values=numerical_columns)
y_axis_dropdown.grid(row=0, column=0, padx=10, pady=10)
y_axis_dropdown.current(0)

y_min_scale = tk.Scale(root, orient=tk.HORIZONTAL, label="Y-min")
y_min_scale.grid(row=1, column=0, padx=10, pady=10)

y_max_scale = tk.Scale(root, orient=tk.HORIZONTAL, label="Y-max")
y_max_scale.grid(row=2, column=0, padx=10, pady=10)

update_sliders()

update_button = tk.Button(root, text="Update Plot", command=update_box_plot)
update_button.grid(row=3, column=0, padx=10, pady=10)

color_button = tk.Button(root, text="Choose Box Plot Color", command=choose_color)
color_button.grid(row=4, column=0, padx=10, pady=10)

fig = plt.Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
widget = canvas.get_tk_widget()
widget.grid(row=0, column=1, rowspan=5, padx=10, pady=10)

root.mainloop()


