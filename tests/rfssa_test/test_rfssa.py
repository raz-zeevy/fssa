from lib.controller.controller import *
from lib.controller.controller import Controller

# SET_MODE_PRODUCTION()
SET_MODE_TEST()

class testRFSSA(Controller):
    def __init__(self):
        super().__init__()
        self.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()

    def test_mms(self):
        # get the absoult path of the data file
        # load the mms file
        session_path = (
            r"C:\Users\raz3z\Projects\Shmuel\fssaDist\fssa\tests\rfssa_test\rFssa.mms"
        )
        self.load_session(session_path)
        self.next_page()
        self.next_page()
        self.next_page()
        self.gui.pages[DIMENSIONS_PAGE_NAME].set_correlation_type(PEARSON)
        try:
            self.output_path = (
                r"C:\Users\raz3z\Projects\Shmuel\fssaDist\fssa\output"
                r"\test_simple.fss"
            )
            self.run_fss(self._run_fss)
            self.enable_view_results()
        except Exception as e:
            print(e)
            assert False
        # run_file_path = p_FSS_DRV

    def test_simple_csv(self):
        """
        this test won't work if the dimensions is 2-5 and the number of
        variables is 4. for some reason.
        :return:
        """
        # get the absoult path of the data file
        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(test_dir_path,
                                      'diamond6.csv')
        self.gui.pages[INPUT_PAGE_NAME].set_data_file_path(
            data_file_path)
        self._suggest_parsing()
        self.has_header = True
        self.next_page()
        self.previous_page()
        self.next_page()
        self.previous_page()
        self.reset_session(False)
        #
        self.gui.pages[INPUT_PAGE_NAME].set_data_file_path(
            data_file_path)
        self._suggest_parsing()
        self.gui.pages[INPUT_PAGE_NAME].set_missing_value(True)
        self.has_header = True
        self.next_page(); self.next_page()
        #
        self.previous_page(); self.previous_page()
        self.gui.pages[INPUT_PAGE_NAME].set_missing_value(False)
        self.next_page(); self.next_page()
        self.previous_page(); self.previous_page()
        self.gui.pages[INPUT_PAGE_NAME].set_missing_value(True)
        self.next_page()
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].select_csv_variables([0, 1, 2, 3])
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].set_labels(['a','b','c','d',
                                                            'e'])
        self.next_page()
        data = self.gui.pages[DATA_PAGE_NAME].get_all_visible_data()
        assert len(data[0]) == 4
        assert len(data) == 22
        assert self.gui.pages[DATA_PAGE_NAME].get_visible_labels() == ['a','b','c','d']
        self.next_page()
        self.next_page()
        try:
            self.output_path = (
                r"C:\Users\raz3z\Projects\Shmuel\fssaDist\fssa\output"
                r"\test_simple.fss"
            )
            self.run_fss(self._run_fss)
            self.enable_view_results()
        except Exception as e:
            print(e)
            # print("################FAILURE###############")
            assert False

if __name__ == '__main__':
    a = testRFSSA()
    a.test_mms()
    a.run_process()