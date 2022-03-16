"""Tests for the MA attention checks
"""
#pylint: disable=import-outside-toplevel, no-self-use
from unittest import TestCase
import pkg_resources, json


class MaChecksTests(TestCase):
    """Tests for the MA attention checks
    """

    def test_repeat_unit(self):
        pass

    def test_from_1p_1t_json(self):
        """Test on sample data
        """
        from meadows.multiarrange import evaluate_checks
        fname = 'Meadows_MaChecks_v_vdesign_preview_1_tree.json'
        fpath = pkg_resources.resource_filename('tests', 'data/' + fname)
        with open(fpath) as fhandle:
            data = json.load(fhandle)
        acc, df = evaluate_checks(data)
        self.assertEqual(acc, 1.0)
        self.assertAlmostEqual(df.iloc[0].pair1_dist, 0.6321, 4)
        self.assertAlmostEqual(df.iloc[0].pair2_dist, 0.8214, 4)
        self.assertEqual(df.iloc[0].label, 'no')
        self.assertEqual(df.iloc[0].acc, True)
