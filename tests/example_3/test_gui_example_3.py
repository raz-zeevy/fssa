from lib.controller import *
from lib.fss_parsers import *
from tests.tests_utils import *
EX_3_FORMAT_TXT = """(/,T59I1,T60I1,T61I1,T62I1,T63I1,T64I1,T65I1,T66I1,T67I1,T68I1,T69I1,T70I1,T71I1
,T72I1,T73I1,T74I1,T75I1,T76I1,T77I1,T78I1,T79I1,T80I1,T81I1,T82I1,T83I1,T84I1,T
85I1,T86I1,T87I1,T88I1,T89I1,T90I1,T92I2,T94I2,T96I2,T98I2,/,T1I2,T3I2,T5I2,T7I2
,T9I2,T11I2,T13I2,T15I2,T17I2,T19I2,T21I2,T23I2,T25I2,T27I2,T29I2,T31I2,T33I2,T3
5I2,T37I2,T39I2,T43I2,T45I2,T49I2,T51I2,T55I2,T60I2,T62I2,T64I2,T66I2,T68I2,T70I
2,T72I2,T74I2,T76I2,T78I2,T80I2,T82I2,T84I2,T86I2,T88I2,T90I2,T92I2,T94I2,T98I2,
T102I2,T106I2,T110I2,T114I2,/)"""
EX_3_MISSING_VALUES_TXT = """   1   2   0   0   4   9
   2   2   0   0   4   9
   3   2   0   0   4   9
   4   2   0   0   4   9
   5   2   0   0   4   9
   6   2   0   0   4   9
   7   2   0   0   4   9
   8   2   0   0   4   9
   9   2   0   0   4   9
  10   2   0   0   4   9
  11   2   0   0   4   9
  12   2   0   0   4   9
  13   2   0   0   4   9
  14   2   0   0   4   9
  15   2   0   0   4   9
  16   2   0   0   4   9
  17   2   0   0   4   9
  18   2   0   0   4   9
  19   2   0   0   4   9
  20   2   0   0   4   9
  21   2   0   0   4   9
  22   2   0   0   4   9
  23   2   0   0   4   9
  24   2   0   0   4   9
  25   2   0   0   4   9
  26   2   0   0   4   9
  27   2   0   0   4   9
  28   2   0   0   4   9
  29   2   0   0   4   9
  30   2   0   0   4   9
  31   2   0   0   4   9
  32   2   0   0   4   9
  33   2   0   7  25  99
  34   2   0   7  25  99
  35   2   0   7  25  99
  36   2   0   7  25  99
  37   1   0   0
  38   1   0   0
  39   1   0   0
  40   1   0   0
  41   1   0   0
  42   1   0   0
  43   1   0   0
  44   1   0   0
  45   1   0   0
  46   1   0   0
  47   1   0   0
  48   1   0   0
  49   1   0   0
  50   1   0   0
  51   1   0   0
  52   1   0   0
  53   1   0   0
  54   1   0   0
  55   1   0   0
  56   1   0   0
  57   1   0   0
  58   1   0   0
  59   1   0   0
  60   1   0   0
  61   1   0   0
  62   1   0   0
  63   1   0   0
  64   1   0   0
  65   1   0   0
  66   1   0   0
  67   1   0   0
  68   1   0   0
  69   1   0   0
  70   1   0   0
  71   1   0   0
  72   1   0   0
  73   1   0   0
  74   1   0   0
  75   1   0   0
  76   1   0   0
  77   1   0   0
  78   1   0   0
  79   1   0   0
  80   1   0   0
  81   1   0   0
  82   1   0   0
  83   1   0   0
  84   1   0   0"""
EX_3_LABELS_TXT = """  1  cre1
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
EX_3_FACETS_TXT = """   4   7   2   6
figural
verbal
numeral
social
fluency
flexibility
orginality
elaboration
closure
titles
appropriateness
creativity
torrance
cre v
cre f
tor v
tor f
cre n
cre s"""
EX_3_FACETS_VAR_TXT = """1 7 1 2
 1 7 1 2
 1 7 1 2
 1 7 1 2
 1 7 1 2
 1 7 1 2
 1 7 1 2
 1 7 1 2
 2 7 1 1
 2 7 1 1
 2 7 1 1
 2 7 1 1
 2 7 1 1
 2 7 1 1
 2 7 1 1
 2 7 1 1
 3 7 1 5
 3 7 1 5
 3 7 1 5
 3 7 1 5
 3 7 1 5
 3 7 1 5
 3 7 1 5
 3 7 1 5
 4 7 1 6
 4 7 1 6
 4 7 1 6
 4 7 1 6
 4 7 1 6
 4 7 1 6
 4 7 1 6
 4 7 1 6
 1 0 1 2
 2 0 1 1
 3 0 1 5
 4 0 1 6
 2 1 2 3
 2 1 2 3
 2 1 2 3
 2 1 2 3
 2 1 2 3
 2 1 2 3
 2 2 2 3
 2 2 2 3
 2 2 2 3
 2 2 2 3
 2 2 2 3
 2 2 2 3
 2 3 2 3
 2 3 2 3
 2 3 2 3
 2 3 2 3
 2 3 2 3
 2 3 2 3
 2 1 2 3
 2 1 2 3
 2 2 2 3
 2 2 2 3
 2 3 2 3
 2 3 2 3
 2 0 2 3
 1 1 2 4
 1 1 2 4
 1 3 2 4
 1 3 2 4
 1 3 2 4
 1 6 2 4
 1 6 2 4
 1 4 2 4
 1 4 2 4
 1 4 2 4
 1 5 2 4
 1 1 2 4
 1 3 2 4
 1 6 2 4
 1 4 2 4
 1 3 2 4
 1 3 2 4
 1 1 2 4
 1 3 2 4
 1 6 2 4
 1 4 2 4
 1 5 2 4
 1 0 2 4"""
EX_3_HYPOTHESES_TXT = """   2   1   1   2   0
   2   1   1   2   1
   2   1   1   2   2
   2   1   1   2   3
   2   2   1   2   0
   2   2   1   2   1
   2   2   1   2   2
   2   2   1   2   3
   2   3   1   2   0
   2   3   1   2   1
   2   3   1   2   2
   2   3   1   2   3
   2   4   1   2   0
   2   4   1   2   1
   2   4   1   2   2
   2   4   1   2   3
   3   1   1   2   0
   3   1   1   3   0
   3   1   2   3   0
   3   2   1   2   0
   3   2   1   3   0
   3   2   2   3   0
   3   3   1   2   0
   3   3   1   3   0
   3   3   2   3   0
   3   4   1   2   0
   3   4   1   3   0
   3   4   2   3   0"""
EX_3_DATA_PATH = "example_3.prn"

###
test_facets = [
                ["figural", "verbal", "numeral", "social"],
                ["fluency", "flexibility", "orginality", "elaboration", "closure"],
                ["titles", "appropriateness"],
                ["creativity", "torrance"],
            ]

class example_3_controller(Controller):
    def __init__(self):
        super().__init__()
        self.test_example_3()

    def test_example_3(self):
        # get the absoult path of the data file
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(self.dir_path,
                                      EX_3_DATA_PATH)
        self.gui.pages[START_PAGE_NAME].set_data_file_path(data_file_path)
        self.gui.pages[START_PAGE_NAME].set_entry_lines(4)
        self.gui.pages[START_PAGE_NAME].button_manual_input.state(["!disabled"])
        self.gui.pages[START_PAGE_NAME].button_manual_input.invoke()
        manual_page = self.gui.pages[MANUAL_FORMAT_PAGE_NAME]
        simulate_manual_format(EX_3_FORMAT_TXT, manual_page.add_variable,
                               labels=EX_3_LABELS_TXT,
                               missing_values_txt=EX_3_MISSING_VALUES_TXT)
        self.gui.button_next.invoke()
        self.gui.button_next.invoke()
        dims_page = self.gui.pages[DIMENSIONS_PAGE_NAME]
        dims_page.dimension_combo.current(1)
        dims_page.dimension_combo_selected(None)
        dims_page.set_dims(2,3)
        self.gui.button_next.invoke()
        facet_page = self.gui.pages[FACET_PAGE_NAME]
        facet_page.set_facets_num(4)
        self.on_facet_num_change(None)
        facet_page.set_facets_details(test_facets)
        assert facet_page.get_facets_details() == test_facets
        facet_data = simulate_facets_details(EX_3_FACETS_TXT,
                                 facet_page.set_facets_details)
        assert facet_data == facet_page.get_facets_details()
        self.gui.button_next.invoke()
        simulate_facets_var_data(EX_3_FACETS_VAR_TXT, self.gui.pages[
            FACET_VAR_PAGE_NAME].combo_by_var)
        assert self.gui.pages[FACET_VAR_PAGE_NAME].get_all_var_facets_indices() == \
               parse_facets_var_data(EX_3_FACETS_VAR_TXT)
        self.gui.button_next.invoke()
        hypo_data = parse_hypotheses_per_facet(EX_3_HYPOTHESES_TXT)
        simulate_hypothesis(hypo_data.models,
                          self.gui.pages[HYPOTHESIS_PAGE_NAME].models)
        assert self.gui.pages[HYPOTHESIS_PAGE_NAME].get_hypotheses() == \
                hypo_data.models
        self.gui.button_next.invoke()
        simulate_facets_dim(hypo_data.facets_dim,
                           self.gui.pages[FACET_DIM_PAGE_NAME].facets_dim_check_buttons)
        assert self.gui.pages[FACET_DIM_PAGE_NAME].get_facets_dim() == \
                hypo_data.facets_dim
        try:
            self.gui.button_run.invoke()
        except Exception as e:
            raise Exception(e)
        run_file_path = r"C:\Users\Raz_Z\Projects\Shmuel\fssa\run_files" \
                        r"\FSSAINP.DRV"
        true_file_path = os.path.join(self.dir_path, "FSSAINP.DRV")
        assert diff_lines_num(run_file_path, true_file_path) == 1
        quit()

if __name__ == '__main__':
    test = example_3_controller()
    test.run_process()