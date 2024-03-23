from tkinter import filedialog, Menu
import ttkbootstrap as ttk
from lib.utils import *
from lib.components.form import *
ENTRIES_PADX = 20


class HypothesisPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.models = []
        self.main_frame = None

    def create_entries(self, facets_num):
        # Main Frame
        if self.main_frame:
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            self.main_frame.destroy()
            self.models = []

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill='x', padx=ENTRIES_PADX, pady=(40, 0))
        # Label for the text
        label_text = Label(self.main_frame,
                               text="Regional Hypotheses To Be Tested",)
        label_text.pack(side=ttk.TOP, fill='x',
                        expand=True, padx=ENTRIES_PADX+20)
        # boxes frame
        hypo_boxes_frame = ttk.Frame(self.main_frame)
        hypo_boxes_frame.pack(fill='x', padx=ENTRIES_PADX, pady=10)

        # Checkbox, without text, aligned to the right
        for facet in range(facets_num):
            facet_models = []
            facet_txt = f"Facet {chr(65 + facet)}"
            facet_frame = ttk.LabelFrame(hypo_boxes_frame, text=facet_txt)
            facet_frame.pack(side="left", fill='x', padx=ENTRIES_PADX, pady=10)
            for hypo in ["Axial", "Angular", "Radial"]:
                hypo_label_frame = ttk.Frame(facet_frame)
                hypo_label_frame.pack(side=ttk.TOP, fill='x', expand=True,
                                      pady=15)
                hypo_var = ttk.BooleanVar(value=True)
                checkbox_hypo = ttk.Checkbutton(hypo_label_frame,
                                                bootstyle="round-toggle",
                                                variable=hypo_var,
                                                onvalue=True,
                                                offvalue=False)
                checkbox_hypo.pack(side=ttk.LEFT, padx=(10,0))
                facet_models.append(checkbox_hypo)
                hypo_label = Label(hypo_label_frame,
                                        text=hypo,
                                        anchor='w',)
                hypo_label.pack(side=ttk.LEFT, fill='x', expand=True,
                                padx=(0,10))
            self.models.append(facet_models)

    def set_hypotheses(self, hypo_details):
        """
        Set the hypotheses for the facets
        :param hypo_details: eg. [[0, 1, 2, 3], [0, 1, 2, 3]]
        :return:
        """
        for i, facet in enumerate(hypo_details):
            for j, model in enumerate(self.models[i]):
                if j in facet:
                    model.state(['selected'])
                else:
                    model.state(['!selected'])

    def get_hypotheses(self):
        """
        Returns the list of lists of hypotheses per facets
        including the 0th hypothesis
        :return: eg. [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
        """
        hypotheses = []
        for facet in self.models:
            facet_hypotheses = [0]
            for i, model in enumerate(facet):
                if model.instate(['selected']):
                    facet_hypotheses.append(i+1)
            hypotheses.append(facet_hypotheses)
        return hypotheses
