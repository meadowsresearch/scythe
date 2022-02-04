from unittest import TestCase
import pkg_resources
from numpy.testing import assert_array_equal, assert_array_almost_equal


class IoDataframeTests(TestCase):
    """Acceptance and unit tests for loading pandas Datafram from json files.
    """

    def test_load_dataframe_from_json_file_1p_1t_ma(self):
        """Acceptance test for loading data from a Meadows
        .json file download containing data for a single MA task,
        single participant. Should have data and descriptors
        as found in file.
        """
        from meadows.io.pandas import load_ma_dataframe
        fname = 'Meadows_myExp_v_v1_cuddly-bunny_3_tree.json'
        fpath = pkg_resources.resource_filename('tests', 'data/' + fname)
        df = load_ma_dataframe(fpath)
        self.assertEqual(rdms.descriptors.get('participant'), 'cuddly-bunny')
        self.assertEqual(rdms.descriptors.get('task_index'), 3)
        self.assertEqual(rdms.descriptors.get('experiment_name'), 'myExp')
        self.assertEqual(rdms.dissimilarity_measure, 'euclidean')
        conds = rdms.pattern_descriptors.get('conds')
        assert_array_equal(conds[:2], ['stim118', 'stim117'])
        assert_array_almost_equal(
            rdms.dissimilarities[0, :2],
            [0.00791285387561264, 0.00817090931233484]
        )