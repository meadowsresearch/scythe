from unittest import TestCase
import pkg_resources
from random import randint


def random_row(n_rows):
    return randint(0, n_rows-1)


class IoPandasTests(TestCase):
    """Acceptance and unit tests for loading pandas Datafram from json files.
    """

    def test_load_dataframe_from_json_file_1p_1t_ma(self):
        """Acceptance test for loading data from a Meadows
        .json file download containing data for a single MA task,
        single participant. Should have data and descriptors
        as found in file.
        """
        from meadows.io.pandas import df_from_tree_file
        fname = 'Meadows_myExp_v_v1_cuddly-bunny_3_tree.json'
        fpath = pkg_resources.resource_filename('tests', 'data/' + fname)
        df = df_from_tree_file(fpath)
        self.assertEqual(df['trial'].unique().size, 109)
        N_PLACEMENTS_TOTAL = TASK_ROWS = 1758
        self.assertEqual(len(df), N_PLACEMENTS_TOTAL)
        ## file-level descriptors
        self.assertEqual(df['participant'][random_row(TASK_ROWS)], 'cuddly-bunny')
        self.assertEqual(df['task_index'][random_row(TASK_ROWS)], 3)
        self.assertEqual(df['task_name'][random_row(TASK_ROWS)], 'arrangement')
        self.assertEqual(df['experiment_name'][random_row(TASK_ROWS)], 'myExp')
        ## trial-level descriptors
        TRIAL = 23
        TRIAL_ROWS = 4
        trial_df = df[df['trial'] == TRIAL].reset_index()
        self.assertEqual(len(trial_df), TRIAL_ROWS)
        # self.assertEqual(trial_df['trial_start'][random_row(TRIAL_ROWS)], 1509300051496)
        # self.assertEqual(trial_df['trial_end'][random_row(TRIAL_ROWS)], 1509300064445)
        ## stimulus-level descriptors
        self.assertEqual(trial_df['stim_id'][0], '59f240584eae357c0f039786')
        self.assertEqual(trial_df['x'][0], 1.3041179991844583)
        self.assertEqual(trial_df['y'][0], 0.8458686782494096)
        self.assertEqual(trial_df['stim_fname'][0], 'stim069.png')

    def test_df_from_dict(self):
        """Test creating a dataframe from a data dictionary directly.
        """
        from meadows.io.pandas import df_from_task_data
        data = dict()
        data['task'] = dict(name='arrangement')
        data['stimuli'] = [
            dict(id='s1', name='stim1'),
            dict(id='s2', name='stim2'),
            dict(id='s3', name='stim3'),
        ]
        data['trials'] = [
            dict(start=111, end=222, positions=[
                dict(id='s1', x=0.17, y=0.18),
                dict(id='s2', x=0.27, y=0.28),
                dict(id='s3', x=0.37, y=0.38)
            ]),
            dict(start=333, end=444, positions=[
                dict(id='s2', x=1.27, y=1.28),
                dict(id='s3', x=1.37, y=1.38)
            ]),
        ]
        meta = dict(participant='cuddly-bunny', task_index=3, experiment_name='myExp')
        df = df_from_task_data(data, meta)
        N_PLACEMENTS_TOTAL = TASK_ROWS = 5
        self.assertEqual(len(df), N_PLACEMENTS_TOTAL)
        self.assertEqual(df['participant'][random_row(TASK_ROWS)], 'cuddly-bunny')
        self.assertEqual(df['task_index'][random_row(TASK_ROWS)], 3)
        self.assertEqual(df['task_name'][random_row(TASK_ROWS)], 'arrangement')
        self.assertEqual(df['experiment_name'][random_row(TASK_ROWS)], 'myExp')
        ## trial-level descriptors
        TRIAL = 1
        TRIAL_ROWS = 2
        trial_df = df[df['trial'] == TRIAL].reset_index()
        self.assertEqual(len(trial_df), TRIAL_ROWS)
        # self.assertEqual(trial_df['trial_start'][random_row(TRIAL_ROWS)], 333)
        # self.assertEqual(trial_df['trial_end'][random_row(TRIAL_ROWS)], 444)
        ## stimulus-level descriptors
        self.assertEqual(trial_df['stim_id'][0], 's2')
        self.assertEqual(trial_df['x'][0], 1.27)
        self.assertEqual(trial_df['y'][0], 1.28)
        self.assertEqual(trial_df['stim_fname'][0], 'stim2')
