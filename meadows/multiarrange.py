"""Tools related to the Multiple Arrangements task
"""
from __future__ import annotations
from typing import TYPE_CHECKING
import numpy
from scipy.stats import spearmanr
from sklearn.manifold import MDS
from rsatoolbox.rdm.calc import calc_rdm_euclid
from rsatoolbox.rdm.combine import from_partials, rescale
if TYPE_CHECKING:
    from rsatoolbox.data import Dataset


def calc_trial_rep(ds: Dataset) -> float:
    ## TODO: arg: include_partial_trials
    ## can use smacoff with nans or 0s?
    ## or median distance
    """Calculate MA Trial Replicability Index

    Args:
        ds (Dataset): rsatoolbox Dataset with the MA experiment data

    Returns:
        float: replicability index
    """
    ## a simple replicability index would be the accuracy 
    # (measured as rank correlation) with which we can predict the distances 
    # in each trial from all other trials. 
    # we would infer the RDM from all training trials, 
    # perform 2D MDS on the subset of that RDM describing the test trial items 
    # (to simulate subject behavior in the test trial) 
    # and rank-correlate the 2D MDS distances with 
    # the test-trial arrangement distances.
    mds = MDS(
        n_components=2,
        random_state=numpy.random.RandomState(seed=1),
        dissimilarity='precomputed'
    )
    rdm_list = []
    for ds in ds.split_obs('trial'):
        rdm = calc_rdm_euclid(ds)
        rdm.pattern_descriptors['stim_fname'] = ds.obs_descriptors['stim_fname']
        rdm_list.append(rdm)
    n_trials = len(rdm_list)
    trial_wise_prediction = numpy.full(n_trials, numpy.nan)
    for t in range(n_trials):
        print(t)
        test_rdm = rdm_list[t]
        test_items = test_rdm.pattern_descriptors['stim_fname'] ## TODO must be intersection instead
        training_rdm_list = [rdm for r, rdm in enumerate(rdm_list) if r != t]
        training_rdms = from_partials(training_rdm_list, descriptor='stim_fname')
        training_rdms_scaled = rescale(training_rdms, method='evidence')
        training_rdm = training_rdms_scaled.mean(weights='rescalingWeights')
        training_subset = training_rdm.subset_pattern('stim_fname', test_items)
        predicted = mds.fit_transform(training_subset.get_matrices()[0, :, :])
        predicted_rdm = calc_rdm_euclid(Dataset(predicted))
        trial_wise_prediction[t], p = spearmanr(
            predicted_rdm.dissimilarities, test_rdm.dissimilarities)
    return trial_wise_prediction.mean()
