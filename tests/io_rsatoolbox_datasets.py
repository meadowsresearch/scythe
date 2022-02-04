from unittest import TestCase
import pkg_resources
from numpy.testing import assert_array_equal, assert_array_almost_equal


class IoRsatoolboxDatasetsTests(TestCase):
    """Acceptance and unit tests for loading DataSets from json files.
    """

    def test_load_datasets_from_json_file_1p_1t(self):
        """Acceptance test for loading data from a Meadows
        .json file download containing data for a single MA task,
        single participant. Should have data and descriptors
        as found in file.
        """
        from meadows.io.rsatoolbox import load_datasets
        ## obs (trials, stimuli) x channels (features)
        ## one dataset per? task? subject? trial?
        ## one per task for now, can split later 
        ## json -> Dataframe -> rsatoolbox.DataSet ## probbaly this for now?
        ## json -> rsatoolbox.DataSet -> Dataframe ## separate feature
        fname = 'Meadows_myExp_v_v1_cuddly-bunny_3_tree.json'
        fpath = pkg_resources.resource_filename('tests', 'data/' + fname)
        datasets = load_datasets(fpath)
        self.assertEqual(len(datasets), 1)
        ds = datasets[0]
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