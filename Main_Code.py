import tkinter as tk
import subprocess

# Mapping of button numbers to script names
scripts = {
    1: "Figure_1.py",
    2: "Figure_2.py",
    3: "Figure_3_GUI.py",
    4: "Figure_4.py",
    5: "Figure_5.py",
    6: "Figure_6.py"
}

def run_script(script_number):
    script_name = scripts[script_number]
    subprocess.run(["python", script_name], check=True)

# Create the main window
root = tk.Tk()
root.title("Shir Grief & Yogev Attias")

root.geometry("400x300")

# Create buttons with "Figure - X" labels
for i in range(1, 7):
    button_label = f"Figure - {i}"
    button = tk.Button(root, text=button_label, command=lambda i=i: run_script(i))
    button.pack(pady=10)

# Run the application
root.mainloop()
