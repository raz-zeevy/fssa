import ttkbootstrap as ttk
import tkinter as tk
from tktooltip import ToolTip
from lib.components.window import Window
from lib.components.form import NavigationButton
from tkinter import filedialog, messagebox
from lib.utils import rreal_size
import os

class RunWindow(Window):
    def __init__(self, parent, default_output_file="", **kwargs):
        super().__init__(parent, geometry=f"{rreal_size(450)}x{rreal_size(175)}", **kwargs)
        self.title("Run FSSA")
        self.default_output_file = default_output_file
        self.default_job_name = os.path.splitext(os.path.basename(default_output_file))[0] if default_output_file else ""
        self.create_widgets()

    def create_widgets(self):
        # Job Name Frame
        job_frame = ttk.Frame(self)
        job_frame.pack(fill='x', padx=10, pady=(20, 10))
        
        ttk.Label(job_frame, text="Job Name:").pack(side='left', padx=(10, 5))
        self.job_name_entry = ttk.Entry(job_frame, width=40)
        self.job_name_entry.pack(side='left', padx=5)
        if self.default_job_name:
            self.job_name_entry.insert(0, self.default_job_name)
        ToolTip(self.job_name_entry, msg="Enter a name for this job")

        # Output File Frame
        output_frame = ttk.Frame(self)
        output_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(output_frame, text="Output File:").pack(side='left', padx=(10, 5))
        self.output_file_entry = ttk.Entry(output_frame, width=40)
        self.output_file_entry.pack(side='left', padx=5)
        if self.default_output_file:
            self.output_file_entry.insert(0, self.default_output_file)
        
        browse_button = ttk.Button(output_frame, text="Browse..", command=self.browse_output)
        browse_button.pack(side='left', padx=5)
        ToolTip(self.output_file_entry, msg="Select where to save the output file")

        # Buttons Frame
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=(20, 10))

        run_button = NavigationButton(button_frame, text="Run", command=self.run)
        run_button.pack(side='left', padx=10)
        
        cancel_button = NavigationButton(button_frame, text="Cancel", 
                                       command=self.cancel, style="secondary")
        cancel_button.pack(side='left', padx=10)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".fss",
            filetypes=[("FSS files", "*.fss")],
            initialfile=self.default_output_file
        )
        if filename:
            self.output_file_entry.delete(0, tk.END)
            self.output_file_entry.insert(0, filename)

    def run(self):
        job_name = self.job_name_entry.get().strip()
        output_file = self.output_file_entry.get().strip()
        
        if not job_name:
            messagebox.showerror("Error", "Please enter a job name")
            return
        
        if not output_file:
            messagebox.showerror("Error", "Please select an output file")
            return
            
        self.result = (job_name, output_file)
        self.destroy()

if __name__ == "__main__":
    # Create root window with theme
    root = ttk.Window(themename="sandstone")
    window = RunWindow(root, default_output_file="test_analysis.fss")
    result = window.show_modal()
    print("Window result:", result)

    # Start the application
    root.mainloop()