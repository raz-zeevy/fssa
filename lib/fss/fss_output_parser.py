import inspect
import json
import os
import warnings

import numpy as np

from lib.utils import *

END_BLOCK = '\x0c'
BUFFER = "."


class OutputParser:
    _cache = {}

    def __init__(self, file_path):
        self.index = 0
        self.current_row = None # Initialize to None
        self.rows = None # Initialize to None

        current_mtime = os.path.getmtime(file_path)

        if file_path in OutputParser._cache:
            cached_mtime, cached_data = OutputParser._cache[file_path]
            if current_mtime == cached_mtime:
                self.metadata = cached_data["metadata"]
                self.dim_data = cached_data["dimensions"]
                self.models = cached_data["models"]
                return

        with open(file_path, 'r', encoding='latin-1') as file:
            self.rows = file.readlines()
            self.current_row = self.rows[0]

            #
            self.metadata = None
            self.dim_data = {}
            self.models = []
            self.extract_data()

            # Cache the parsed data
            OutputParser._cache[file_path] = (
                current_mtime, self.get_output()
            )

    def next_row(self, called_function=None):
        # get the name of the function that called next_row
        if not called_function:
            called_function = inspect.stack()[1].function
        try:
            self.index += 1
            self.current_row = self.rows[self.index]
        except IndexError as e:
            if IS_PRODUCTION():
                pass
            else:
                warnings.warn(f"OUTPUT PARSER ERORR: {e} \non {called_function}")

    def next_rows(self, num: int):
        called_function = inspect.stack()[1].function
        for i in range(num):
            self.next_row(called_function=called_function)

    def extract_data(self):
        while self.index < len(self.rows) - 1:
            if "NAME OF THE JOB" in self.current_row:
                self.metadata = self.extract_metadata()
            if "D I M E N S I O N A L I T Y" in self.current_row:
                dim_data = self.parse_dimension()
                self.dim_data[dim_data['dimension']] = dim_data
            if " MODEL TYPE " in self.current_row:
                model = self.parse_model()
                self.models.append(model)
            self.next_row()

    def parse_dimension(self):
        def parse_dimension_info():
            data = {}
            while not self.current_row == "\n":
                row_data = self.parse_data_line_format(self.current_row)
                data.update(row_data)
                self.next_row()
            return data

        def parse_dimension_data():
            data = []
            while not self.end_block_reached():
                row_rdata = self.current_row.split()
                row_data = {
                    "serial_number": int(row_rdata[0]),
                    "distance_from_centroid": float(row_rdata[1]),
                    "coordinates": [float(row_rdata[i]) for i in range(2,
                                                                       len(
                                                                           row_rdata))],
                }
                data.append(row_data)
                self.next_row()
            return data

        self.current_dim = int(self.current_row.strip().split()[-1])
        self.next_rows(3)
        dim_info = parse_dimension_info()
        self.next_rows(4)
        dim_coord = parse_dimension_data()
        dim_info['coordinates'] = dim_coord
        dim_info['dimension'] = self.current_dim
        return dim_info

    def parse_model(self):
        def parse_divide_geom():
            def find_dot_x_y():
                c_s = self.current_row.find("(")
                c_e = self.current_row.find(")")
                return eval(self.current_row[c_s:c_e + 1].replace(" ", ""))

            row = self.current_row.split()
            shape = row[1]
            if shape == "LINE":
                return {
                    "shape": shape,
                    "x": float(row[4][:-2]),
                    "y": float(row[6][:-2]),
                    "n": float(row[8]),
                }
            elif shape == "AXIS":
                center = find_dot_x_y()
                angle = self.current_row.strip()[-7:]
                return {
                    "shape": shape,
                    "center": center,
                    "angle": float(angle),
                }
            elif shape == "CIRCLE":
                center = find_dot_x_y()
                return {
                    "shape": shape,
                    "center": center,
                    "radius": float(row[-1]),
                }

        def parse_separation_index():
            row = self.current_row.split()
            if len(row) < 8: return {
                "deviant_points_num": np.nan,
                "seperation_index": np.nan,
            }
            return {
                "deviant_points_num": int(row[3]),
                "seperation_index": float(row[7]),
            }

        facet = int(self.current_row.split("AND FACET")[-1].strip()[0])
        model = int(self.current_row.split("MODEL TYPE")[-1].strip())
        self.next_rows(60)
        d_geoms = []
        while " DIVIDING " in self.current_row:
            d_geom = parse_divide_geom()
            d_geoms.append(d_geom)
            self.next_row()
        separation_index = parse_separation_index()
        model_data = {
            "facet": facet,
            "model": model,
            "divide_geoms": d_geoms,
        }
        model_data.update(separation_index)
        return model_data

    @staticmethod
    def split_by_buffer(text):
        first_buffer_index = text.find(BUFFER)
        last_buffer_index = None
        for i in range(first_buffer_index, len(text)):
            if text[i] != BUFFER:
                last_buffer_index = i - 1
                break
        return text[:first_buffer_index], text[last_buffer_index + 1:]

    def parse_data_line_format(self, text):
        var, value = self.split_by_buffer(text)
        var = var.strip().replace(" ", "_").lower()
        value = value.strip().lower()
        try:
            value = float(value)
        except ValueError:
            pass
        if value is None: return
        return {var: value}

    def end_block_reached(self):
        return END_BLOCK in self.current_row

    def extract_metadata(self):
        data = {}
        while not self.end_block_reached():
            row_data = self.parse_data_line_format(self.current_row)
            if not row_data:
                self.next_row()
                continue
            data.update(row_data)
            self.next_row()
        return data

    def get_output(self):
        return {
            "metadata": self.metadata,
            "dimensions": self.dim_data,
            "models": self.models,
        }

def parse_output(file_path):
    output_parser = OutputParser(file_path)
    return output_parser.get_output()


if __name__ == '__main__':
    output_path = r"C:\Users\raz3z\Projects\Shmuel\fssa\output\test_3_gui.fss"
    # output_path = r"C:\Users\raz3z\Projects\Shmuel\fssa\output\test_simple.fss"
    print(json.dumps(parse_output(output_path),
                     sort_keys=True, indent=4))
