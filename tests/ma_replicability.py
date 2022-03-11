"""Tests for the trial replicability index
"""
#pylint: disable=import-outside-toplevel, no-self-use
from unittest import TestCase
import pkg_resources
from numpy.random import RandomState
import numpy
from rsatoolbox.data import Dataset


class MaTrialReplicabilityTests(TestCase):
    """Tests for the trial replicability index
    """

    def test_index_high(self):
        from meadows.multiarrange import calc_trial_rep
        ds = Dataset(
            measurements=numpy.array([
                [-1,    0   ], # trial 1, courgette
                [-0.9,  0.1 ], # trial 1, cucumber
                [ 0.4,  0.4 ], # trial 1, banana
                [ 0.7,  0.7 ], # trial 1, apple
                [ 0.6,  0.75], # trial 1, orange
                [ 0,   -1   ], # trial 2, banana
                [ 0.2,  0.9 ], # trial 2, apple
                [-0.2,  0.9 ], # trial 2, orange
                [ 0,    -1  ], # trial 3, courgette
                [-0.1,  0.8 ], # trial 3, cucumber
                [ 0,    1   ], # trial 3, banana
            ]),
            descriptors=dict(foo='bar'),
            obs_descriptors=dict(
                trial=[1,1,1,1,1,2,2,2,3,3,3],
                stim_name=['co', 'cu', 'ba', 'ap', 'or', 'ba', 'ap', 'or', 
                    'co', 'cu', 'ba']
            ),
            channel_descriptors=dict(dimension=['x', 'y'])
        )
        self.assertAlmostEqual(calc_trial_rep(ds), 0.683, places=3)

    def test_index_random(self):
        from meadows.multiarrange import calc_trial_rep
        rng = RandomState(seed=1)
        ds = Dataset(
            measurements=(rng.rand(11, 2)*2)-1,
            descriptors=dict(foo='bar'),
            obs_descriptors=dict(
                trial=[1,1,1,1,1,2,2,2,3,3,3],
                stim_name=['co', 'cu', 'ba', 'ap', 'or', 'ba', 'ap', 'or', 
                    'co', 'cu', 'ba']
            ),
            channel_descriptors=dict(dimension=['x', 'y'])
        )
        self.assertAlmostEqual(calc_trial_rep(ds), 0.0)

    def test_load_datasets_from_json_file_1p_1t(self):
        """Test on sample data
        """
        from meadows.multiarrange import calc_trial_rep
        from meadows.io.rsatoolbox import load_dataset
        fname = 'Meadows_myExp_v_v2_profound-mammoth_1_tree.json'
        fpath = pkg_resources.resource_filename('tests', 'data/' + fname)
        ds = load_dataset(fpath)
        self.assertAlmostEqual(calc_trial_rep(ds), 0.9057, places=4)
