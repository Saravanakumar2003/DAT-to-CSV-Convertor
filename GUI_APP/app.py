import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from conversion_utils import convert_dat_to_csv
import os
import csv

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DAT to CSV Converter")
        self.root.geometry("600x200")

        self.status = tk.StringVar()
        self.status.set("Waiting for file...")

        tk.Label(self.root, text="DAT to CSV Converter", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        tk.Label(self.root, text="Input File Location:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.input_entry = tk.Entry(self.root, width=50)
        self.input_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_input)
        self.browse_button.grid(row=1, column=2, padx=10, pady=10)

        tk.Label(self.root, text="Output Location:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.output_entry = tk.Entry(self.root, width=50)
        self.output_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_output)
        self.browse_button.grid(row=2, column=2, padx=10, pady=10)

        self.convert_button = tk.Button(self.root, text="Convert Now", command=self.convert_files)
        self.convert_button.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

        tk.Label(self.root, textvariable=self.status, font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10, columnspan=3)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def browse_input(self):
        file_path = filedialog.askopenfilename(title="Select .dat File", filetypes=[("All files", "*.*"), ("DAT files", "*.dat")])
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)

    def browse_output(self):
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, dir_path)

    def convert_files(self):
        input_file_path = self.input_entry.get()
        output_dir_path = self.output_entry.get()
        if input_file_path and output_dir_path:
            self.status.set("Converting file...")
            converted_data = convert_dat_to_csv(input_file_path)
            if converted_data:
                self.save_csv(converted_data, output_dir_path)
            else:
                messagebox.showerror("Error", "Conversion failed for file: {}".format(os.path.basename(input_file_path)))
            self.status.set("Waiting for file...")
        else:
            messagebox.showerror("Error", "Please select input file and output directory.")

    def save_csv(self, data, output_dir_path):
        output_file_path = os.path.join(output_dir_path, "output.csv")
        with open(output_file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys(), restval="N/A")
            writer.writeheader()
            writer.writerows(data)
        messagebox.showinfo("Success", "Conversion completed. CSV file saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()