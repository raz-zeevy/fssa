import os
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import filedialog
from lib.components.form import NavigationButton, DataButton
import matplotlib
from lib.windows.window import Window
from lib.components.shapes import Line, Circle, DivideAxis, VerticalLine
from lib.utils import get_resource, real_size, rreal_size

G_COLOR = '#a4aab3'
DPI_SAVE = 300
matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

BORDER_WIDTH = 0
OC = 0.05

class DiagramWindow(Window):
    def __init__(self, parent, graph_data_lst: list, title, **kwargs):
        """
        graph_data: list of dictionaries containing the data to be plotted
        should contain "x", "y", "annotations", "title", "legend",
         "captions", "geom" keys
        """
        super().__init__(**kwargs, geometry=f"{rreal_size(900)}x{rreal_size(700)}")
        self.title(title)
        # self.iconbitmap(get_resource("icon.ico"))
        # sets the geometry of toplevel
        self.graph_data_lst = graph_data_lst
        self.index = 0
        # init
        # Create main container with padding
        self.container = ttk.Frame(self, padding=rreal_size(10))
        self.container.pack(fill=tk.BOTH, expand=True)
        
        self.main_frame = ttk.Frame(self.container)
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.create_menu()
        self.create_bottom_panel()
        self.load_page(self.index)
        # Bind key presses to the respective methods
        self.bind("<Return>", lambda x: self.next_graph())
        self.bind("<Right>", lambda x: self.next_graph())
        self.bind("<BackSpace>", lambda x: self.previous_graph())
        self.bind("<Left>", lambda x: self.previous_graph())
        self.bind("<Escape>", lambda x: self.exit())
        self.resizable(True, True)
        # set default to maximize 
        self.state("zoomed")

    def create_menu(self):
        # create a file menu with save figure command to save the current graph
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save figure ",
                                   command=self.save_figure)
        # add an option to save all figures
        self.file_menu.add_command(label="Save all figures",
                                   command=self.save_all_figures)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit)

    def get_default_fig_file_name(self):
        label = self.graph_data_lst[self.index]["title"]
        clean_label = label.replace(" ", "_").replace(":","_").replace("\n","_")
        default_name = f"{clean_label}.png"
        return default_name

    def save_figure(self):
        default_name = self.get_default_fig_file_name()
        file = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files",
                                                        "*.png")],
                                            initialfile=default_name)
        if file:
            self.figure.savefig(file, dpi=DPI_SAVE)

    def save_all_figures(self):
        dir = filedialog.askdirectory()
        current_page = self.index
        self.load_page(0)
        for i in range (len(self.graph_data_lst)):
            # I don't use the self.get_name because it would cause that
            # some figures would not be saved
            path = os.path.join(dir, "figure_" + str(i + 1) + ".png")
            self.figure.set_size_inches(real_size(5), real_size(5))
            self.figure.savefig(path, dpi=DPI_SAVE)
            self.next_graph()
        self.index = current_page
        self.load_page(current_page)

    def init_scrollable_legend(self):
        # Create canvas with grid instead of pack
        self.legend_canvas = tk.Canvas(self.main_frame,
                                       borderwidth=BORDER_WIDTH,
                                       background="red",
                                       width=rreal_size(175))
        self.diagram_labels_frame = ttk.Frame(self.legend_canvas,
                                              borderwidth=BORDER_WIDTH,
                                              relief="solid")
        
        # Create scrollbar and use grid
        self.vsb = ttk.Scrollbar(self.main_frame, orient="vertical",
                                 command=self.legend_canvas.yview)
        self.legend_canvas.configure(yscrollcommand=self.vsb.set)
        
        # Use grid for both canvas and scrollbar
        self.legend_canvas.grid(row=0, column=1, sticky='nsew')
        self.vsb.grid(row=0, column=2, sticky='ns')
        
        # Create the window for the canvas content
        self.canvas_frame = self.legend_canvas.create_window((0, 0),
                                                             window=self.diagram_labels_frame,
                                                             anchor="nw")
        
        # Keep the existing bindings
        self.diagram_labels_frame.bind("<Configure>", self.onFrameConfigure)
        self.legend_canvas.bind('<Configure>', self.FrameWidth)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.legend_canvas.configure(
            scrollregion=self.legend_canvas.bbox("all"))

    def FrameWidth(self, event):
        '''Reset the canvas window to encompass inner frame when resizing'''
        canvas_width = event.width
        self.legend_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def navigate_control(self):
        """
        This function is now Obsolete because we have circular paging
        :return:
        """
        if self.index < len(self.graph_data_lst) - 1:
            self.button_next.state(["!disabled"])
        else:
            self.button_next.state(["disabled"])
        if self.index > 0:
            self.button_previous.state(["!disabled"])
        else:
            self.button_previous.state(["disabled"])

    def next_graph(self):
        if self.index < len(self.graph_data_lst) - 1:
            self.index += 1
        else:
            self.index = 0  # Loop back to the first graph
        self.load_page(self.index)

    def previous_graph(self):
        if self.index > 0:
            self.index -= 1
        else:
            self.index = len(self.graph_data_lst) - 1  # Loop to the last graph
        self.load_page(self.index)

    def exit(self):
        self.destroy()

    def load_page(self, i):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Configure grid weights to control space allocation
        self.main_frame.grid_columnconfigure(0, weight=3)  # Graph gets 3/4 of width
        self.main_frame.grid_columnconfigure(1, weight=1)  # Legend gets 1/4 of width
        self.main_frame.grid_rowconfigure(0, weight=1)     # Row expands to fill height

        # Create frames using grid instead of pack
        self.diagram_frame = ttk.Frame(self.main_frame)
        self.diagram_frame.grid(row=0, column=0, sticky='nsew')

        if len(self.graph_data_lst[i]["legend"]) > 20:
            self.init_scrollable_legend()
            self.vsb.grid(row=0, column=2, sticky='ns')
        else:
            self.diagram_labels_frame = ttk.Frame(self.main_frame)
            self.diagram_labels_frame.grid(row=0, column=1, sticky='nsew', padx=real_size((0, 10)))
            self.diagram_labels_frame.config(width=rreal_size(40))

        self.plot_scatter(self.graph_data_lst[i])
        self.plot_legend(self.graph_data_lst[i])

    def plot_legend(self, graph_data):
        # Create a container frame for all legend content
        legend_container = ttk.Frame(self.diagram_labels_frame)
        legend_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Title frame at the top of the container
        diagram_title_frame = ttk.Frame(legend_container, borderwidth=BORDER_WIDTH)
        diagram_title_frame.pack(side=tk.TOP, fill=tk.X, pady=real_size((10, 5)))
        
        diagram_label = ttk.Label(diagram_title_frame,
                                text=graph_data["title"],
                                font=f'Helvetica {rreal_size(11)} bold',
                                wraplength=rreal_size(200))  # Add wraplength to handle long titles
        diagram_label.pack(side=tk.TOP, fill='x')
        
        # Legend items frame directly below the title
        legend_items_frame = ttk.Frame(legend_container)
        legend_items_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        for item in graph_data["legend"]:
            space = "     " if item["index"] < 10 else "   "
            item_frame = ttk.Frame(legend_items_frame)
            item_frame.pack(side=tk.TOP, fill=tk.X, pady=real_size(1))
            
            label = ttk.Label(item_frame,
                            text=f'{item["index"]}{space}{item["value"]}',
                            borderwidth=BORDER_WIDTH,
                            font=f'Helvetica {rreal_size(11)}')
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def plot_scatter(self, graph_data):
        def add_geoms(x, axes, graph_data):
            def add_line(x, axes, line: Line):
                # Create a figure and axis
                start, end = min(x) * 0.5, max(
                    x) * 2  # buffers to ensure it is
                # long enough
                start, end = start - (end - start) * OC, end + (
                        end - start) * OC

                # Plot each line
                x_values, y_values = line.get_points(start, end)
                axes.plot(x_values, y_values, color=G_COLOR)

            def add_circle(axes, circle: Circle):
                # Create a circle patch
                circle_plot = matplotlib.patches.Circle(circle.center,
                                                        circle.radius,
                                                        edgecolor=G_COLOR,
                                                        facecolor='none')
                # Add the circle to the plot
                axes.add_patch(circle_plot)

            def add_divide_axis(axes, divide_axis: DivideAxis):
                x_values, y_values = divide_axis.get_points(1000)
                axes.plot(x_values, y_values, color=G_COLOR)

            if 'geoms' not in graph_data:
                return
            for geom in graph_data["geoms"]:
                if isinstance(geom, Line):
                    add_line(x, axes, geom)
                elif isinstance(geom, Circle):
                    add_circle(axes, geom)
                elif isinstance(geom, DivideAxis):
                    add_divide_axis(axes, geom)
                elif isinstance(geom, VerticalLine):
                    add_line(x, axes, geom)
                else:
                    raise ValueError(f"Unknown geometry type: {type(geom)}")

        x = graph_data["x"]
        y = graph_data["y"]
        z = graph_data["annotations"]
        # create a figure and axis
        self.figure = Figure(figsize=real_size((4, 4)), dpi=100)
        figure_canvas = FigureCanvasTkAgg(self.figure, self.diagram_frame)
        axes = self.figure.add_subplot()
        # Force square aspect ratio
        axes.set_aspect('equal', adjustable='box')
        # plot the data
        axes.scatter(x, y, alpha=0)
        # set the title
        caption = ""
        if "caption" in graph_data:
            caption = graph_data["caption"]
        # set the title text to be smaller
        axes.text(0, -0.1, caption, ha='left', va='top',
                  transform=axes.transAxes, fontsize=rreal_size(8))
        self.figure.subplots_adjust(left=0.12,
                                    right=0.88,
                                    top=0.95,
                                    bottom=0.12)
        # create annotations
        annot_offset = (max(y) - min(y)) / 100
        for i, txt in enumerate(z):
            axes.annotate(txt, (x[i], y[i] - annot_offset),
                          ha='center',
                          fontsize=rreal_size(9))
        # add geom
        add_geoms(x, axes, graph_data)
        # Adjust the plot limits to make sure it fits
        start_x, end_x = 0, 100
        start_y, end_y = 0, 100
        x_offset, y_offset = (end_x - start_x) * OC * 0.75, \
                             (end_y - start_y) * OC * 0.75
        axes.set_xlim([start_x - x_offset, end_x + x_offset])
        axes.set_ylim([start_y - y_offset, end_y + y_offset])
        figure_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        # Configure the diagram_frame grid weights
        self.diagram_frame.grid_columnconfigure(0, weight=1)
        self.diagram_frame.grid_rowconfigure(0, weight=1)

    def create_bottom_panel(self):
        # Navigation Buttons Frame
        frame_navigation = ttk.Frame(self.container)
        # pack the navigation at the bottom of the screen but above the help
        # bar
        frame_navigation.pack(side=ttk.BOTTOM, fill='x', padx=real_size(10),
                              pady=real_size((0, 40)))
        center_frame = ttk.Frame(frame_navigation)
        center_frame.pack(pady=real_size(5), expand=False)
        self.button_previous = NavigationButton(center_frame,
                                                text="Previous",
                                                command=self.previous_graph, )
        self.button_previous.pack(side=ttk.LEFT, padx=real_size(20))
        self.button_next = NavigationButton(center_frame, text="Next",
                                            command=self.next_graph, )
        self.button_next.pack(side=ttk.LEFT, padx=real_size(20))
        self.button_save_figure = NavigationButton(center_frame,
                                                    text="Save Figure",
                                                    command=self.save_figure, )
        self.button_save_figure.pack(side=ttk.LEFT, padx=real_size(20))
        self.button_exit = NavigationButton(center_frame, text="Exit",
                                            bootstyle='secondary',
                                            command=self.exit, )
        self.button_exit.pack(side=ttk.LEFT, padx=real_size(20))
        # modify permanent state of the buttons
        if len(self.graph_data_lst) == 1:
            self.button_previous.state(["disabled"])
            self.button_next.state(["disabled"])
        else:
            self.button_previous.state(["!disabled"])
            self.button_next.state(["!disabled"])

def test_diagram_window(n=35):
    # Create dummy data with 35 points
    import random
    num_points = n
    x_coords = [random.uniform(0, 100) for _ in range(num_points)]
    y_coords = [random.uniform(0, 100) for _ in range(num_points)]
    annotations = [chr(65 + i) if i < 26 else f'AA{i-25}' for i in range(num_points)]
    legend_items = [{"index": i+1, "value": f"Variable {annotations[i]}"} for i in range(num_points)]
    
    dummy_data = [{
        "x": x_coords,
        "y": y_coords,
        "annotations": annotations,
        "title": "No Partition\nSSA Solution d=1X3",
        "legend": legend_items,
        "caption": f"This is a test diagram with {num_points} variables"
    }]
    
    return DiagramWindow(None, dummy_data, "Test Diagram")


if __name__ == "__main__":    
    # Create two separate windows
    window1 = test_diagram_window(n=35)
    window1.mainloop()
    