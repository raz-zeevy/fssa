import numpy as np
import ttkbootstrap as ttk
import tkinter as tk
from lib.components.form import NavigationButton
import matplotlib.pyplot as plt
import matplotlib
from lib.components.window import Window
from lib.components.shapes import Line, Circle, DivideAxis

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
BORDER_WIDTH = 0
OC = 0.05

class DiagramWindow(Window):
    def __init__(self, parent, graph_data_lst : list, **kwargs):
        """
        graph_data: list of dictionaries containing the data to be plotted
        should contain "x", "y", "annotations", "title", "legend",
         "captions", "geom" keys
        """
        super().__init__(**kwargs, geometry="800x700")
        self.title("FSS Solution")
        # sets the geometry of toplevel
        self.graph_data_lst = graph_data_lst
        self.index = 0
        # init
        self.create_navigation()
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.load_page(self.index)
        # Bind key presses to the respective methods
        self.bind("<Return>", lambda x : self.next_graph())
        self.bind("<Right>", lambda x : self.next_graph())
        self.bind("<BackSpace>", lambda x : self.previous_graph())
        self.bind("<Left>", lambda x : self.previous_graph())
        self.bind("<Escape>", lambda x : self.exit())

    def init_scrollable_legend(self):
        self.legend_canvas = tk.Canvas(self.main_frame,
                                       borderwidth=BORDER_WIDTH,
                                       background="red",
                                       width=175)
        self.diagram_labels_frame = ttk.Frame(self.legend_canvas,
                                              borderwidth=BORDER_WIDTH,
                                              relief="solid", )
         # Adjust the width as needed
        self.vsb = ttk.Scrollbar(self.main_frame, orient="vertical",
                                 command=self.legend_canvas.yview)
        self.legend_canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.legend_canvas.pack(side="right", fill="both", expand=True)
        self.canvas_frame = self.legend_canvas.create_window((0, 0),
                                                             window=self.diagram_labels_frame,
                                                             anchor="nw")
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
            self.load_page(self.index)

    def previous_graph(self):
        if self.index > 0:
            self.index -= 1
            self.load_page(self.index)
    def exit(self):
        self.destroy()

    def load_page(self, i):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.navigate_control()
        #
        self.diagram_frame = ttk.Frame(self.main_frame)
        self.diagram_frame.pack(side=tk.LEFT, fill=tk.BOTH,expand=True)
        self.plot_scatter(self.graph_data_lst[i])
        if len(self.graph_data_lst[i]["legend"]) > 20:
            self.init_scrollable_legend()
        else:
            self.diagram_labels_frame = ttk.Frame(self.main_frame)
            self.diagram_labels_frame.pack(side=tk.RIGHT,
                                           expand=True,
                                           fill=tk.BOTH,
                                           padx=(0, 10))
        self.diagram_labels_frame.config(
            width=40)
        self.plot_legend(self.graph_data_lst[i])
    def plot_legend(self, graph_data):
        diagram_title_frame = ttk.Frame(self.diagram_labels_frame,
                                        borderwidth=BORDER_WIDTH)
        diagram_title_frame.pack(side=tk.TOP, fill=tk.X, expand=False,
                                 pady=(10,0))
        diagram_label = ttk.Label(diagram_title_frame,
                                       text=graph_data["title"],
                                        bootstyle="primary-bold",
                                  font='Helvetica 8 bold')
        diagram_label.pack(side=tk.TOP,
                           expand=True,
                           fill='x')
        # now create labels for all the variables and their labels, this will
        # be done in a loop and serve like a legend for the diagram
        legend_items_frame = ttk.Frame(self.diagram_labels_frame,)
        legend_items_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True,
                                pady=(5,0))
        for item in graph_data["legend"]:
            space = "     " if item["index"] < 10 else "   "
            label = ttk.Label(legend_items_frame,
                              text=f'{item["index"]}{space}{item["value"]}',
                              bootstyle=ttk.PRIMARY,
                              borderwidth=BORDER_WIDTH,
                              relief="solid", )
            label.pack(side=tk.TOP, fill=tk.BOTH)

    def plot_scatter(self, graph_data):
        def add_geoms(x, axes, graph_data):
            def add_line(x, axes, line: Line):
                # Create a figure and axis
                start, end = min(x), max(x)
                start, end = start - (end - start) * OC, end + (
                            end - start) * OC

                # Plot each line
                x_values, y_values = line.get_points(start, end)
                axes.plot(x_values, y_values)
            def add_circle(axes, circle: Circle):
                # Create a circle patch
                circle_plot = matplotlib.patches.Circle(circle.center,
                                                        circle.radius,
                                                        edgecolor='r',
                                                        facecolor='none')
                # Add the circle to the plot
                axes.add_patch(circle_plot)
            def add_divide_axis(axes, divide_axis: DivideAxis):
                x_values, y_values = divide_axis.get_points(1000)
                axes.plot(x_values, y_values, linestyle='dashed', )
            if 'geoms' not in graph_data:
                return
            for geom in graph_data["geoms"]:
                if isinstance(geom, Line):
                    add_line(x, axes, geom)
                elif isinstance(geom, Circle):
                    add_circle(axes, geom)
                elif isinstance(geom, DivideAxis):
                    add_divide_axis(axes, geom)
                else:
                    raise ValueError(f"Unknown geometry type: {type(geom)}")
        x = graph_data["x"]
        y = graph_data["y"]
        z = graph_data["annotations"]
        # create a figure and axis
        figure = Figure(figsize=(2,4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure,
                                          self.diagram_frame)
        axes = figure.add_subplot()
        # plot the data
        axes.scatter(x, y, alpha=0)
        # set the title
        caption = ""
        if "caption" in graph_data:
            caption = graph_data["caption"]
        # set the title text to be smaller
        axes.text(0, -0.1, caption, ha='left', va='top',
                  transform=axes.transAxes, fontsize=8)
        figure.subplots_adjust(left=0.1,
                               right=0.95,
                               top=0.95,
                               bottom=0.15)
        # create annotations
        annot_offset = (max(y) - min(y)) / 100
        for i, txt in enumerate(z):
            axes.annotate(txt, (x[i], y[i]-annot_offset),
                          ha='center',
                          fontsize=8)
        # add geom
        add_geoms(x, axes, graph_data)
        # Adjust the plot limits to make sure all of your circle is shown
        start_x, end_x = min(x), max(x)
        start_y, end_y = min(y), max(y)
        x_offset, y_offset = (end_x - start_x) * OC, (end_y - start_y) * OC
        axes.set_xlim([min(x)-x_offset, max(x)+x_offset])
        axes.set_ylim([min(y)-y_offset, max(y)+y_offset])
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def create_navigation(self):
        # Navigation Buttons Frame
        frame_navigation = ttk.Frame(self)
        # pack the navigation at the bottom of the screen but above the help
        # bar
        frame_navigation.pack(side=ttk.BOTTOM, fill='x', padx=10,
                              pady=(0, 40))
        center_frame = ttk.Frame(frame_navigation)
        center_frame.pack(pady=5, expand=True)
        self.button_previous = NavigationButton(center_frame,
                                                text="Previous",
                                                command=self.previous_graph,)
        self.button_previous.pack(side=ttk.LEFT, padx=20)
        self.button_next = NavigationButton(center_frame, text="Next",
                                            command=self.next_graph,)
        self.button_next.pack(side=ttk.LEFT, padx=20, )
        self.button_exit = NavigationButton(center_frame, text="Exit",
                                            bootstyle='secondary',
                                            command=self.exit,)
        self.button_exit.pack(side=ttk.LEFT, padx=20)

