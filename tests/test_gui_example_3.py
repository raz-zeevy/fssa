from lib.controller import *
from lib.fss_parsers import simulate_manual_format

EX_3_FORMAT_TXT = """(/,T59I1,T60I1,T61I1,T62I1,T63I1,T64I1,T65I1,T66I1,T67I1,T68I1,T69I1,T70I1,T71I1
,T72I1,T73I1,T74I1,T75I1,T76I1,T77I1,T78I1,T79I1,T80I1,T81I1,T82I1,T83I1,T84I1,T
85I1,T86I1,T87I1,T88I1,T89I1,T90I1,T92I2,T94I2,T96I2,T98I2,/,T1I2,T3I2,T5I2,T7I2
,T9I2,T11I2,T13I2,T15I2,T17I2,T19I2,T21I2,T23I2,T25I2,T27I2,T29I2,T31I2,T33I2,T3
5I2,T37I2,T39I2,T43I2,T45I2,T49I2,T51I2,T55I2,T60I2,T62I2,T64I2,T66I2,T68I2,T70I
2,T72I2,T74I2,T76I2,T78I2,T80I2,T82I2,T84I2,T86I2,T88I2,T90I2,T92I2,T94I2,T98I2,
T102I2,T106I2,T110I2,T114I2,/)"""
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
EX_3_DATA_PATH = "example_3.prn"
class example_3_controller(Controller):
    def __init__(self):
        super().__init__()
        self.test_3()

    def test_3(self):
        # get the absoult path of the data file
        self.data_file_path = os.path.join(os.getcwd(), EX_3_DATA_PATH)
        self.gui.pages[START_PAGE_NAME].set_entry_lines(4)
        self.gui.switch_page(MANUAL_FORMAT_PAGE_NAME)
        manual_page = self.gui.pages[MANUAL_FORMAT_PAGE_NAME]
        simulate_manual_format(EX_3_FORMAT_TXT, manual_page.add_variable,
                               labels=EX_3_LABELS_TXT)

if __name__ == '__main__':
    test = example_3_controller()
    test.run_process()