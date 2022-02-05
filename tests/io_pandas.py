from unittest import TestCase
import pkg_resources
from random import randint
from numpy.testing import assert_array_equal, assert_array_almost_equal


class IoPandasTests(TestCase):
    """Acceptance and unit tests for loading pandas Datafram from json files.
    """

    def test_load_dataframe_from_json_file_1p_1t_ma(self):
        """Acceptance test for loading data from a Meadows
        .json file download containing data for a single MA task,
        single participant. Should have data and descriptors
        as found in file.
        """
        from meadows.io.pandas import load_dataframe
        fname = 'Meadows_myExp_v_v1_cuddly-bunny_3_tree.json'
        fpath = pkg_resources.resource_filename('tests', 'data/' + fname)
        df = load_dataframe(fpath)
        self.assertEqual(df['trial'].unique.size, 109)
        NROWS = 999
        self.assertEqual(len(df), NROWS)
        ## file-level descriptors
        def random_row():
            return randint(0, NROWS-1)
        self.assertEqual(df['participant'][random_row()], 'cuddly-bunny')
        self.assertEqual(df['task_index'][random_row()], 3)
        self.assertEqual(df['task_name'][random_row()], 'arrangement')
        self.assertEqual(df['experiment_name'][random_row()], 'myExp')
        ## trial-level descriptors
        # trial index
        ## stimulus-level descriptors
        # stim id
        # stim name
        # x
        # y
        assert_array_equal(df['stim_name'], ['stim118', 'stim117'])
        assert_array_equal(df['stim_id'], ['stim118', 'stim117'])
        assert_array_almost_equal(df['x'],
            [0.00791285387561264, 0.00817090931233484])
