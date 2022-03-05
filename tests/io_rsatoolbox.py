from unittest import TestCase
import pkg_resources
from numpy import array
from numpy.testing import assert_array_almost_equal


class IoRsatoolboxTests(TestCase):
    """Acceptance and unit tests for loading DataSets from json files.
    """

    def test_load_datasets_from_json_file_1p_1t(self):
        """Acceptance test for loading data from a Meadows
        .json file download containing data for a single MA task,
        single participant. Should have data and descriptors
        as found in file.
        """
        from meadows.io.rsatoolbox import load_dataset
        fname = 'Meadows_myExp_v_v1_cuddly-bunny_3_tree.json'
        fpath = pkg_resources.resource_filename('tests', 'data/' + fname)
        ds = load_dataset(fpath)
        self.assertEqual(ds.descriptors.get('participant'), 'cuddly-bunny')
        self.assertEqual(ds.descriptors.get('task_index'), 3)
        self.assertEqual(ds.descriptors.get('task_name'), 'arrangement')
        self.assertEqual(ds.descriptors.get('experiment_name'), 'myExp')
        self.assertEqual(ds.channel_descriptors.get('name'), ['x', 'y'])
        ## obs
        O = 731
        self.assertEqual(ds.obs_descriptors.get('trial')[O], 23)
        #self.assertEqual(ds.obs_descriptors.get('trial_start')[O], 1509300051496)
        #self.assertEqual(ds.obs_descriptors.get('trial_end')[O], 1509300064445)
        self.assertEqual(ds.obs_descriptors.get('stim_id')[O], '59f240584eae357c0f039786')
        self.assertEqual(ds.obs_descriptors.get('stim_fname')[O], 'stim069.png')
        assert_array_almost_equal(ds.measurements[O, :], array([1.304118, 0.845869]))
