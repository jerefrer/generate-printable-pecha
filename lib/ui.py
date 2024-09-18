import os
from tkinter import Tk, PhotoImage, Frame, Button, Label, filedialog, Radiobutton, Checkbutton, StringVar, IntVar
from .process_file import process_file

root = Tk()

input_file_path = ''

def select_file():
    if filepath := filedialog.askopenfilename(title="Select File"):
        global input_file_path
        input_file_path = filepath
        _, inputFileName = os.path.split(input_file_path)
        file_selected_label.config(text=f"File selected: {inputFileName}")
        process_button.config(state="normal")

def click_process_button():
    progress_label.config(text="Processing...")
    root.update_idletasks()

    autoscale_mapping = {
        "No": False,
        "Fit paper": "pdfjam",
        "Crop to content": "podofo"
    }
    process_file(input_file_path, paper_size.get(), autoscale_mapping[autoscale.get()], True)

    directory, filename = os.path.split(input_file_path)
    filename, ext = os.path.splitext(filename)
    output_file_name = f"{filename}_processed{ext}"
    progress_label.config(text=f"Done!\n\nNew file generated: {output_file_name}")

root.title("Generate Printable Pecha")

root.configure(padx=50, pady=20)

save_label = Label(root, text="")
save_label.pack()

select_button = Button(root, text="Select File", command=select_file, pady=10, width=20)
select_button.pack()

file_selected_label = Label(root, text="", pady=20)
file_selected_label.pack()

options_grid = Frame(root, pady=30)
options_grid.pack()
paper_size_label = Label(options_grid, text="Paper size")
paper_size_label.grid(row=0, column=0, padx=(0, 10), pady=10)
paper_size = StringVar()
paper_size.set("A4")
paper_size_options = ["A4", "A3"]
for i, option in enumerate(paper_size_options):
    radio_button = Radiobutton(options_grid, text=option, variable=paper_size, value=option)
    radio_button.grid(row=0, column=i+1, padx=10, pady=10, sticky="w")

autoscale = StringVar()
autoscale.set("No")
autoscale_label = Label(options_grid, text="Autoscale")
autoscale_label.grid(row=1, column=0, padx=(0, 10), pady=10)
autoscale_options = ["No", "Fit paper", "Crop to content"]
for i, option in enumerate(autoscale_options):
    radio_button = Radiobutton(options_grid, text=option, variable=autoscale, value=option)
    radio_button.grid(row=1, column=i+1, padx=10, pady=10, sticky="w")

empty_label_for_padding = Label(root, text="")
empty_label_for_padding.pack()

process_button = Button(root, text="Go", state="disabled", command=click_process_button, padx=10, pady=20, width=20)
process_button.pack()

progress_label = Label(root, text="", pady=20)
progress_label.pack()


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    window.geometry(f"+{x_coordinate}+{y_coordinate}")

center_window(root)

root.mainloop()