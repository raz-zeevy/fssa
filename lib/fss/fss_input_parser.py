from typing import List, Tuple
from dotmap import DotMap
import numpy as np


def simulate_manual_format(format_txt: str, add_variable: callable,
                           labels="",
                           missing_values_txt="", ):
    """
    This function simulates the manual format page by taking in a string
    representing the format and a callable that adds a variable to the
    manual format page.
    the format is a list of strings that each represent the start column and
    the width of the variable, while the "/" sign indicates a line break. so
    the data must be read from start to end in order to know the exact line
    the variables are in.
    the add_variable is a callable that takes in the start column, width, and
    line number of the variable and adds it to the manual format page.
    example:
    format_txt : "(T59I1,/,T60I1,T61I1,T62I1,T63I1)\n"
    labels_txt : "  1  cre1
                    2  cre2
                    3  cref3 "
    add_variable(line_num, start, width, label="")
    """

    def parse_missing_values(missing_values_txt: str):
        data = []
        for line in missing_values_txt.strip().split("\n"):
            line = line.strip().split()
            width = max(len(i) for i in line[2:])
            max_val = 9 if width == 1 else 99
            min_val = 0
            intervals_num = int(line[1])
            if intervals_num == 2:
                low = int(line[3]) + 1
                high = int(line[4]) - 1
            elif intervals_num == 1:
                if int(line[3]) == max_val:
                    low, high = min_val, int(line[2]) - 1
                elif int(line[2]) == min_val:
                    low, high = int(line[3]) + 1, max_val
            data.append(dict(low=low, high=high))
        return data

    def parse_var_format(format_txt):
        vars = []
        format_txt = format_txt.strip().replace("\n", "")
        num_lines = 1
        var_num = 0
        for items in format_txt[1:-1].split(","):
            if items == "/":
                num_lines += 1
            else:
                i_index = items.find("I")
                start_col = int(items[1:i_index])
                width = int(items[i_index + 1:])
                vars.append(dict(line_num=num_lines,
                                 start_col=start_col,
                                 field_width=width))
                var_num += 1
        return vars

    label_rows = labels.strip().split("\n")
    labels = [row.strip().split(" ")[-1] for row in label_rows]
    missing_values = parse_missing_values(missing_values_txt)
    var_format = parse_var_format(format_txt)
    for i, var in enumerate(var_format):
        add_variable(line=var["line_num"], col=var["start_col"],
                     width=var["field_width"],
                     valid_low=missing_values[i]['low'],
                     valid_high=missing_values[i]['high'],
                     label=labels[i])


def simulate_facets_details(facets_txt: str, set_details: callable, ):
    """
    :param facets_txt:
           4   4   0   0
    per
    phy
    soc
    cul
    exp
    ada
    int
    con
    :param set_details:
    :return:
    """
    lines = facets_txt.strip().split("\n")
    num_labels = [int(i) for i in lines[0].split("   ")]
    data = [[] for i in num_labels if i > 0]
    line_index, var_index = 1, 0
    while line_index <= len(lines) - 1:
        if int(num_labels[var_index]) > 0:
            data[var_index].append(lines[line_index].split("   ")[-1])
            num_labels[var_index] -= 1
            line_index += 1
        else:
            var_index += 1
    set_details(data)
    return data


def simulate_facets_var_data(facets_var_txt, entries: List[List]):
    """
    :param facets_var_txt: eg.
     1 1
     1 2
     1 3
     1 4
     2 1
     2 2
    :param entries:
    :return:
    """
    for i, line in enumerate(facets_var_txt.strip().split("\n")):
        var_facets = line.strip().split()
        for j, facet_index in enumerate(var_facets):
            entries[i][j].current(facet_index)


def parse_facets_var_data(facets_var_txt: str) -> List[List]:
    entries = []
    for line in facets_var_txt.strip().split("\n"):
        var_facets = line.strip().split()
        entries.append([int(i) for i in var_facets])
    return entries


def parse_hypotheses_per_facet(hypotheses_txt: str) -> List[List]:
    """
    retrns a dict of hypotheses data that contains:
    1. all: (List[List]) a list of lists of all the hypotheses data
            the way it is displayed in the .DRV
    2. models: List[List] a list for each facets of the models
                     to be tested for dim_2
    3. facets_dim: List[List] a list for each dimension, of the facets
                   to be tested for that dimension
    """
    hypotheses = DotMap()
    data = []
    for line in hypotheses_txt.strip().split("\n"):
        data.append([int(i) for i in line.strip().split()])
    # all
    hypotheses.all = data
    # dim_2_models
    data = np.array(data)
    # filter to get only rows where the first column is 2
    filtered_data = data[data[:, 0] == 2, :]
    # bring the fifth column but group by the second column
    hypotheses.models = []
    for i in range(1, 5):
        var_models = filtered_data[filtered_data[:, 1] == i, 4].tolist()
        if var_models:
            hypotheses.models.append(var_models)
    # facets_dim
    hypotheses.facets_dim = {}
    filtered_data = data[:, [0, 1]]
    for dim in np.unique(filtered_data[:, 0]):
        dim_facets = np.unique(filtered_data[filtered_data[:, 0] == dim,
        1]).tolist()
        hypotheses.facets_dim[dim] = dim_facets
    return hypotheses


def simulate_hypothesis(hypo_per_facet: List[List], widgets: List[List]):
    for i, facet in enumerate(hypo_per_facet):
        for model in range(1, 4):
            if not model in facet:
                widgets[i][model - 1].invoke()


def simulate_facets_dim(facets_dim: List[List], widgets: List[List]):
    for dim in widgets:
        for widget in widgets[dim]:
            widget.invoke()
    for dim, facets in facets_dim.items():
        for facet in facets:
            widgets[dim][facet - 1].invoke()


def parse_missing_values(valid_values_range: List[Tuple]):
    var_missing_values = []
    for var in valid_values_range:
        intervals = []
        low, high = int(var[0]), int(var[1])
        max_num = 99 if high > 9 else 9
        min_num = 0
        if low > min_num:
            intervals.append((min_num, low-1))
        if high < max_num:
            intervals.append((high+1, max_num))
        var_missing_values.append(intervals)
    return var_missing_values

if __name__ == '__main__':
    exe_3 = """(/,T59I1,T60I1,T61I1,T62I1,T63I1,T64I1,T65I1,T66I1,T67I1,T68I1,T69I1,T70I1,T71I1
,T72I1,T73I1,T74I1,T75I1,T76I1,T77I1,T78I1,T79I1,T80I1,T81I1,T82I1,T83I1,T84I1,T
85I1,T86I1,T87I1,T88I1,T89I1,T90I1,T92I2,T94I2,T96I2,T98I2,/,T1I2,T3I2,T5I2,T7I2
,T9I2,T11I2,T13I2,T15I2,T17I2,T19I2,T21I2,T23I2,T25I2,T27I2,T29I2,T31I2,T33I2,T3
5I2,T37I2,T39I2,T43I2,T45I2,T49I2,T51I2,T55I2,T60I2,T62I2,T64I2,T66I2,T68I2,T70I
2,T72I2,T74I2,T76I2,T78I2,T80I2,T82I2,T84I2,T86I2,T88I2,T90I2,T92I2,T94I2,T98I2,
T102I2,T106I2,T110I2,T114I2,/)"""
    labels = """  1  cre1
   2  cre2
   3  cref3
   4  cref4
   5  cref5
   6  cref6
   7  cref7
   8  cref8
   9  crev1
  10  crev2
  11  crev3
  12  crev4
  13  crev5
  14  crev6
  15  crev7
  16  crev8
  17  cren1
  18  cren2
  19  cren3
  20  cren4
  21  cren5
  22  cren6
  23  cren7
  24  cren8
  25  cres1
  26  cres2
  27  cres3
  28  cres4
  29  cres5
  30  cres6
  31  cres7
  32  cres8
  33  creavf
  34  creaver
  35  creavn
  36  creavs
  37  torverf1
  38  torverf2
  39  torverf3
  40  torverf4
  41  torver5
  42  torver7
  43  torverflx1
  44  torverflx2
  45  torverflx3
  46  torflx4
  47  torverflx5
  48  torverflx7
  49  torverorg1
  50  torverorg2
  51  torverorg3
  52  torverorg4
  53  torverorg5
  54  torverorg7
  55  torverflutot
  56  torvflu_stn
  57  torvflxtot
  58  torvflx_stn
  59  torvorgtot
  60  torvorg_sn
  61  torvave_sn
  62  torzflu2
  63  torzflu3
  64  torzorg1
  65  tozrorg2
  66  torzorg3
  67  torztit1
  68  torztit2
  69  torzela1
  70  torzela2
  71  torzela3
  72  torzcls
  73  torzflutot
  74  torzorgtot
  75  torztittot
  76  torzelatot
  77  bounus2
  78  bonus3
  79  torzflu_sn
  80  torzorg_sn
  81  torztit_sn
  82  torzela_sn
  83  torzcls_sn
  84  torzave_sn"""
    simulate_manual_format(exe_3, lambda *args: None, labels)
