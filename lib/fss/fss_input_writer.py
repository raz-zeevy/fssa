import os
from typing import List, Dict
from lib.utils import *

class FssInputWriter():
    def __init__(self):
        pass

    def create_fssa_input_file(
            self,
            # variables_details,
            variables_labels: List[Dict],
            min_dim: int = 2,
            max_dim: int = 2,
            is_similarity_data: bool = True,
            eps=0,
            missing_cells: list = [(99, 99)],
            iweigh=2,
            nfacet=0,
            ntface=0,
            store_coordinates_on_file: bool = False,
            iboxstring=0,
            default_form_feed=0,
            facet_details=None,
            facet_var_details=None,
            hypotheses_details=None,
            facet_dim_details=None, ):
        """
    This function creates the FSSA input file (FSSAINP.DRV) for the FSSA program
        :param variables_labels:
        :param min_dim: the minimum dimension of the data matrix
        :param max_dim: the maximum dimension of the data matrix
        :param is_similarity_data: a boolean variable indicating whether the data
        is similarity data or not
        :param eps:
        :param missing_cells: a list of tuples, each tuple contains a range of
        values to be considered as missing cells
        :param iweigh: an integer variable indicating the weighing method
        :param nfacet: an integer variable indicating the number of facets
        :param ntface: an integer variable indicating the number of t-faces
        :param store_coordinates_on_file: a boolean variable indicating whether
        the plotted coordinates should be stored on a file or not
        :param iboxstring: an integer variable indicating the boxstring
        :param default_form_feed: an integer variable indicating the default form
        feed
        :return: None
        """
        # checks if the directory RUN_FILES_DIR exists, if not creates it in the
        # root directory
        if not os.path.exists(RUN_FILES_DIR):
            os.makedirs(RUN_FILES_DIR)
        nvar = len(variables_labels)
        with open(p_FSS_DRV, "w") as f:
            f.write("FSSA-24 INPUT FILE\n")
            f.write(f"  {nvar}   {min_dim}   {max_dim}")
            f.write(f"   {int(is_similarity_data)}   {eps}   "
                    f"{len(missing_cells)}")
            f.write(f"   {iweigh}  {nvar}   {nfacet}  "
                    f" {ntface}   1")
            f.write(f"   {int(store_coordinates_on_file)}   {iboxstring}")
            f.write(f"   {default_form_feed}\n   {len(missing_cells)}")
            for missing_cell_range in missing_cells:
                f.write(
                    f" {missing_cell_range[0]:.7f} {missing_cell_range[1]:.7f}")
            f.write("\n")
            f.write(INPUT_MATRIX_FORMAT + "\n")
            for variable in variables_labels:
                f.write(f" {' ' if variable['index'] < 10 else ''}"
                        f" {variable['index']} "
                        f" {variable['label']}\n")
            # facet variable details
            for variable in facet_var_details:
                for var_facet in variable:
                    f.write(f" {var_facet}")
                f.write("\n")
            # facet details
            for facet_labels in facet_details:
                f.write(f"   {len(facet_labels)}")
            f.write("\n")
            for facet_labels in facet_details:
                [f.write(f"{label}\n") for label in facet_labels]
            # hypotheses details
            self.write_hypotheses(f, facet_dim_details, hypotheses_details)

    def write_hypotheses(self, f, facet_dim_details, hypotheses_details):
        """
        This function writes the hypotheses details to the FSSA input file
        :param facet_dim_details:
        :param hypotheses_details:
        :return:
        """
        for dim, facets in facet_dim_details.items():
            dim_axes = list(range(1, dim + 1))
            axes_pairs = [(a, b) for idx, a in enumerate(dim_axes) for b in
                          dim_axes[idx + 1:]]
            for facet_i, facet in enumerate(facets):
                for a, b in axes_pairs:
                    if dim == 2:
                        for model in hypotheses_details[facet_i]:
                            f.write(
                                f"   {dim}   {facet}   {a}   {b}   {model}\n")
                    else:
                        f.write(f"   {dim}   {facet}   {a}   {b}   0\n")
