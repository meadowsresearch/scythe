"""Unit tests for expanding RDMs to include missing data.
"""
#pylint: disable=import-outside-toplevel
from unittest import TestCase
from numpy import array, nan
from numpy.testing import assert_array_equal


class RdmsExpandTests(TestCase):
    """Unit tests for expanding RDMs to include missing data.
    """

    def test_expand_based_on_list_of_rdms_objects(self):
        """In this case the complete list of conditions is determined
        from the RDMs passed.
        """
        from meadows.brdms import BehavioralRDMs as RDMs
        rdms1 = RDMs(
            dissimilarities=array([[1, 2, 3]]),
            dissimilarity_measure='shared_measure',
            descriptors=dict(shared_desc='shared_val', diff_desc='one'),
            rdm_descriptors=dict(rdesc=['foo1']),
            pattern_descriptors=dict(conds=['a', 'b', 'c']),
        )
        rdms23 = RDMs(
            dissimilarities=array([[4, 5, 6], [7, 8, 9]]),
            dissimilarity_measure='shared_measure',
            descriptors=dict(shared_desc='shared_val', diff_desc='two-three'),
            rdm_descriptors=dict(rdesc=['foo2', 'foo3']),
            pattern_descriptors=dict(conds=['b', 'c', 'd']),
        )
        rdms = RDMs.expand([rdms1, rdms23])
        self.assertEqual(rdms.n_rdm, 3)
        self.assertEqual(rdms.n_cond, 4)
        self.assertEqual(rdms.dissimilarity_measure, 'shared_measure')
        self.assertEqual(rdms.descriptors.get('shared_desc'), 'shared_val')
        assert_array_equal(
            rdms.rdm_descriptors.get('diff_desc'),
            ['one', 'two-three', 'two-three']
        )
        assert_array_equal(
            rdms.rdm_descriptors.get('rdesc'),
            ['foo1', 'foo2', 'foo3']
        )
        assert_array_equal(
            rdms.pattern_descriptors.get('conds'),
            ['a', 'b', 'c', 'd']
        )
        assert_array_equal(
            rdms.dissimilarities,
            array([
                [  1,   2, nan,   3, nan, nan],
                [nan, nan, nan,   4,   5,   6],
                [nan, nan, nan,   7,   8,   9]
            ])
        )

    def test_expand_with_list_of_pattern_descriptors(self):
        """Where the user explicitly chooses the patterns

        We pass a list with a single RDMs object containing one RDM,
        then specify one additional pattern not covered in the RDM.
        """
        from meadows.brdms import BehavioralRDMs as RDMs
        rdms1 = RDMs(
            dissimilarities=array([[1, 2, 3]]),
            dissimilarity_measure='measure',
            pattern_descriptors=dict(conds=['b', 'c', 'd']),
        )
        rdms = RDMs.expand([rdms1], all_patterns=['a', 'b', 'c', 'd'])
        self.assertEqual(rdms.n_rdm, 1)
        self.assertEqual(rdms.n_cond, 4)
        assert_array_equal(
            rdms.pattern_descriptors.get('conds'),
            ['a', 'b', 'c', 'd']
        )
        assert_array_equal(
            rdms.dissimilarities,
            array([
                [nan, nan, nan,   1,   2,   3],
            ])
        )
