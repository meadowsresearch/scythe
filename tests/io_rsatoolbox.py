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
        fname = 'Meadows_myExp_v_v2_profound-mammoth_1_tree.json'
        fpath = pkg_resources.resource_filename('tests', 'data/' + fname)
        ds = load_dataset(fpath)
        self.assertEqual(ds.descriptors.get('participant'), 'profound-mammoth')
        self.assertEqual(ds.descriptors.get('task_index'), 1)
        self.assertEqual(ds.descriptors.get('task_name'), 'multiarrange1')
        self.assertEqual(ds.descriptors.get('experiment_name'), 'myExp')
        self.assertEqual(ds.descriptors.get('version'), '2')
        self.assertEqual(ds.channel_descriptors.get('name'), ['x', 'y'])
        ## obs
        O = 99
        self.assertEqual(ds.obs_descriptors.get('trial')[O], 23)
        self.assertEqual(ds.obs_descriptors.get('trial_start')[O], 1646494875092)
        self.assertEqual(ds.obs_descriptors.get('trial_end')[O], 1646494884936)
        self.assertEqual(ds.obs_descriptors.get('n_actions')[O], 4)
        self.assertEqual(ds.obs_descriptors.get('stim_id')[O], 'fc3317dadd5948d807175da02bc977c4')
        self.assertEqual(ds.obs_descriptors.get('stim_name')[O], 'mud_bubbling')
        ## overall descriptor since the same for all stims:
        self.assertEqual(ds.descriptors.get('stim_type'), 'png')
        assert_array_almost_equal(ds.measurements[O, :], array([ 0.18029752, -0.94403202]))
