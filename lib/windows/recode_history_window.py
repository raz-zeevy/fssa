import ttkbootstrap as ttk
from lib.windows.window import Window
from lib.windows.recoding_window import RecodeWindow, RecodingOperation
from lib.utils import real_size, rreal_size

class RecodeHistoryWindow(Window):
    def __init__(self, parent=None):
        super().__init__(parent, geometry=f"{rreal_size(500)}x{rreal_size(400)}")
        self.title("Recoding History")
        self.create_widgets()
        
    def create_widgets(self):
        # Add explanatory label
        explanation = "History of all recoding operations applied to the current data:"
        label = ttk.Label(
            self, 
            text=explanation,
            justify="left"
        )
        label.pack(fill='x', padx=10, pady=(10,5))
        
        # Create treeview with style
        style = ttk.Style()
        style.configure(
            "Treeview.Heading",
            background='#2B5D8C',  # Dark gray background
            foreground='white',    # White text
            relief='flat'          # Flat appearance
        )
        
        columns = ('Variables', 'Old Values', 'New Value', 'Reversal')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        
        # Configure columns with center alignment
        for col in columns:
            self.tree.heading(col, text=col, anchor='center')
            self.tree.column(col, width=rreal_size(120), anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Load history
        self.load_history()
        
    def load_history(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add history items
        for operation in RecodeWindow.SAVED_VALUES['RECODING_HISTORY']:
            for value_pair in operation.value_pairs:
                old_values = value_pair[0]
                new_value = value_pair[1]
                self.tree.insert('', 'end', values=(
                    operation.variables,
                    old_values,
                    new_value,
                    'No' 
                ))
            if not operation.value_pairs:
                self.tree.insert('', 'end', values=(
                    operation.variables,
                    '',
                    '',
                    'Yes'
                ))

if __name__ == '__main__':
    # Test code with mock data
    root = ttk.Window()
    
    # Add some mock history
    RecodeWindow.SAVED_VALUES['RECODING_HISTORY'] = [
        RecodingOperation("1,2,3", [("1-5", "9"), ("2-6", "10")], False),
        RecodingOperation("4,5", [("2,4,6", "1"), ("3,5,7", "2")], True),
        RecodingOperation("7", [("1-3,5,7", "4")], False)
    ]
    
    # Show window
    history_window = RecodeHistoryWindow(root)
    root.mainloop() 