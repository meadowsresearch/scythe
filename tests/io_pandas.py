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
        self.assertEqual(df['trial'].unique().size, 109)
        N_PLACEMENTS_TOTAL = TASK_ROWS = 1758
        self.assertEqual(len(df), N_PLACEMENTS_TOTAL)
        ## file-level descriptors
        def random_row(n_rows):
            return randint(0, n_rows-1)
        self.assertEqual(df['participant'][random_row(TASK_ROWS)], 'cuddly-bunny')
        self.assertEqual(df['task_index'][random_row(TASK_ROWS)], 3)
        self.assertEqual(df['task_name'][random_row(TASK_ROWS)], 'arrangement')
        self.assertEqual(df['experiment_name'][random_row(TASK_ROWS)], 'myExp')
        ## trial-level descriptors
        TRIAL = 23
        TRIAL_ROWS = 4
        trial_df = df[df['trial'] == TRIAL].reset_index()
        self.assertEqual(len(trial_df), TRIAL_ROWS)
        self.assertEqual(trial_df['trial_start'][random_row(TRIAL_ROWS)], 1509300051496)
        self.assertEqual(trial_df['trial_end'][random_row(TRIAL_ROWS)], 1509300064445)
        ## stimulus-level descriptors
        self.assertEqual(trial_df['stim_id'][0], '59f240584eae357c0f039786')
        self.assertEqual(trial_df['x'][0], 1.3041179991844583)
        self.assertEqual(trial_df['y'][0], 0.8458686782494096)
        self.assertEqual(trial_df['stim_fname'][0], 'stim069.png')
