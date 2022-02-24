"""Tests for the trial replicability index
"""
#pylint: disable=import-outside-toplevel, no-self-use
from unittest import TestCase
import numpy
from rsatoolbox.data import Dataset


class MaTrialReplicibalityTests(TestCase):
    """Tests for the trial replicability index
    """

    def test_index(self):
        from meadows.multiarrange import calc_trial_rep
        ds = Dataset(
            measurements=numpy.random.rand(3, 2),
            descriptors=dict(foo='bar'),
            obs_descriptors=dict(participant=['a', 'b', 'c']),
            channel_descriptors=dict(foc=['x', 'y'], bac=[1, 2])
        )
        self.assertEqual(calc_trial_rep(ds), 0.5)
