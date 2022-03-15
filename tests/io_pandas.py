from unittest import TestCase
import pkg_resources
from random import randint
from dateutil.tz import tzutc
from datetime import datetime


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
        fname = 'Meadows_myExp_v_v2_profound-mammoth_1_tree.json'
        fpath = pkg_resources.resource_filename('tests', 'data/' + fname)
        df = df_from_tree_file(fpath)
        self.assertEqual(df['trial'].unique().size, 56)
        N_PLACEMENTS_TOTAL = TASK_ROWS = 205
        self.assertEqual(len(df), N_PLACEMENTS_TOTAL)
        ## file-level descriptors
        self.assertEqual(df['participant'][random_row(TASK_ROWS)], 'profound-mammoth')
        self.assertEqual(df['task_index'][random_row(TASK_ROWS)], 1)
        self.assertEqual(df['task_name'][random_row(TASK_ROWS)], 'multiarrange1')
        self.assertEqual(df['experiment_name'][random_row(TASK_ROWS)], 'myExp')
        self.assertEqual(df['version'][random_row(TASK_ROWS)], '2')
        ## trial-level descriptors
        TRIAL = 23
        TRIAL_ROWS = 4
        trial_df = df[df['trial'] == TRIAL].reset_index()
        self.assertEqual(len(trial_df), TRIAL_ROWS)
        self.assertEqual(trial_df['trial_start'][random_row(TRIAL_ROWS)], 1646494875092)
        self.assertEqual(trial_df['trial_end'][random_row(TRIAL_ROWS)], 1646494884936)
        self.assertEqual(trial_df['n_actions'][random_row(TRIAL_ROWS)], 4)
        ## stimulus-level descriptors
        self.assertEqual(trial_df['stim_id'][0], '6f3bcd859365621cb1fac620122aad98')
        self.assertEqual(trial_df['x'][0], 0.316031215513301)
        self.assertEqual(trial_df['y'][0], -0.690127377517038)
        self.assertEqual(trial_df['stim_name'][0], 'rain')
        self.assertEqual(trial_df['stim_type'][0], 'png')

    def test_df_from_dict(self):
        """Test creating a dataframe from a data dictionary directly.
        """
        from meadows.io.pandas import df_from_task_data
        data = dict()
        data['task'] = dict(name='arrangement')
        data['stimuli'] = [
            dict(id='s1', name='stim1', type='png'),
            dict(id='s2', name='stim2', type='wav'),
            dict(id='s3', name='stim3', type='jpg'),
        ]
        data['trials'] = [
            dict(start=111, end=222, positions=[
                dict(id='s1', x=0.17, y=0.18),
                dict(id='s2', x=0.27, y=0.28),
                dict(id='s3', x=0.37, y=0.38)
            ], log=[
                [111, 'logStarted', {}],
                [112, 'placed', {}],
                [113, 'displaced', {}],
                [114, 'placed', {}],
                [115, 'placed', {}],
                [116, 'finish', {}],
            ]),
            dict(start=333, end=444, positions=[
                dict(id='s2', x=1.27, y=1.28),
                dict(id='s3', x=1.37, y=1.38)
            ], log=[
                [111, 'logStarted', {}],
                [112, 'placed', {}],
                [113, 'displaced', {}],
                [114, 'placed', {}],
                [115, 'displaced', {}],
                [116, 'placed', {}],
                [117, 'finish', {}],
            ]),
        ]
        meta = dict(participant='cuddly-bunny', task_index=3,
            experiment_name='myExp', version='7')
        df = df_from_task_data(data, meta)
        N_PLACEMENTS_TOTAL = TASK_ROWS = 5
        self.assertEqual(len(df), N_PLACEMENTS_TOTAL)
        self.assertEqual(df['participant'][random_row(TASK_ROWS)], 'cuddly-bunny')
        self.assertEqual(df['task_index'][random_row(TASK_ROWS)], 3)
        self.assertEqual(df['task_name'][random_row(TASK_ROWS)], 'arrangement')
        self.assertEqual(df['experiment_name'][random_row(TASK_ROWS)], 'myExp')
        self.assertEqual(df['version'][random_row(TASK_ROWS)], '7')
        ## trial-level descriptors
        TRIAL = 1
        TRIAL_ROWS = 2
        trial_df = df[df['trial'] == TRIAL].reset_index()
        self.assertEqual(len(trial_df), TRIAL_ROWS)
        self.assertEqual(trial_df['trial_start'][random_row(TRIAL_ROWS)], 111)
        self.assertEqual(trial_df['trial_end'][random_row(TRIAL_ROWS)], 117)
        self.assertEqual(trial_df['n_actions'][random_row(TRIAL_ROWS)], 5)
        ## stimulus-level descriptors
        self.assertEqual(trial_df['stim_id'][0], 's2')
        self.assertEqual(trial_df['x'][0], 1.27)
        self.assertEqual(trial_df['y'][0], 1.28)
        self.assertEqual(trial_df['stim_name'][0], 'stim2')
        self.assertEqual(trial_df['stim_type'][0], 'wav')

    def test_load_checks_dataframe_from_data(self):
        """Create dataframe from acceptance checks in ma data.
        """
        from meadows.io.pandas import df_checks_from_task_data
        data = dict(trials=[
            dict(annotations=[
                dict(
                    ids=['5c', '3b', '3b', 'f63'],
                    start='2022-02-21T16:21:33.703Z',
                    resp='2022-02-21T16:21:38.128Z',
                    label='no'
                ),
                dict(
                    ids=['5c', '3b', '3b', 'f63'],
                    start='2022-02-21T16:21:33.703Z',
                    resp='2022-02-21T16:21:38.128Z',
                    label='no'
                ),
            ]),
            dict(annotations=[
                dict(
                    ids=['5c', '3b', '3b', 'f63'],
                    start='2022-02-21T16:21:33.703Z',
                    resp='2022-02-21T16:21:38.128Z',
                    label='no'
                ),
            ]),
        ])
        df = df_checks_from_task_data(data)
        self.assertEqual(len(df), 3)
        self.assertEqual(df.iloc[0].stim1_id, '5c')
        self.assertEqual(df.iloc[0].stim2_id, '3b')
        self.assertEqual(df.iloc[0].stim3_id, 'f63')
        self.assertEqual(df.iloc[0].start.to_pydatetime(),
            datetime(2022, 2, 21, 16, 21, 33, 703000, tzinfo=tzutc()))
        self.assertEqual(df.iloc[0].resp.to_pydatetime(),
            datetime(2022, 2, 21, 16, 21, 38, 128000, tzinfo=tzutc())) 
        self.assertEqual(df.iloc[0].label, 'no')
