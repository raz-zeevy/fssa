from tkinter import Toplevel
import ttkbootstrap as ttk
from lib.utils import real_size, rreal_size

class LoadingWindow:
    def __init__(self, root, title="Running FSSA", label_text="Running... Please wait"):
        self.root = root
        self.loading_window = None
        self.title = title
        self.label_text = label_text

    def show(self):
        if self.loading_window is None:
            # Create a top-level window to act as a loading indicator
            self.loading_window = Toplevel(self.root)
            self.loading_window.title(self.title)
            self.loading_window.geometry(f"{rreal_size(200)}x{rreal_size(100)}")  # Small window size
            self.loading_window.transient(self.root)  # Attach to the main window
            self.loading_window.grab_set()  # Make it modal
            self.loading_window.resizable(False, False)

            # Center the window on the screen
            self.center_window()

            # Add a text label above the spinner
            self.loading_label = ttk.Label(self.loading_window,
                                         text=self.label_text,
                                         font=('Helvetica', rreal_size(12)))  # Integer font size
            self.loading_label.pack(pady=real_size(10))

            # Add a spinner inside
            self.spinner = ttk.Progressbar(self.loading_window, mode='indeterminate')
            self.spinner.pack(expand=True, pady=real_size(20))
            self.spinner.start(10)

    def hide(self):
        if self.loading_window is not None:
            self.spinner.stop()
            self.loading_window.destroy()
            self.loading_window = None

    def center_window(self):
        self.loading_window.update_idletasks()
        width = self.loading_window.winfo_width()
        height = self.loading_window.winfo_height()
        x = (self.loading_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.loading_window.winfo_screenheight() // 2) - (height // 2)
        self.loading_window.geometry(f'{width}x{height}+{x}+{y}')
        
if __name__ == "__main__":
    root = ttk.Window(themename="sandstone")
    root.title("Loading Window Test")
    
    # Create a button to show the loading window
    def show_loading():
        loading = LoadingWindow(root)
        loading.show()
        # Simulate some work being done
        root.after(3000, loading.hide)
    
    test_button = ttk.Button(root, text="Show Loading", command=show_loading)
    test_button.pack(padx=50, pady=50)
    
    root.mainloop()