"""Tools related to the Multiple Arrangements task
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Tuple
from warnings import warn
import numpy
from pandas import DataFrame
from scipy.stats import spearmanr
from sklearn.manifold import MDS
from rsatoolbox.rdm.calc import calc_rdm_euclid
from rsatoolbox.rdm.combine import from_partials, rescale
from rsatoolbox.data import Dataset
from meadows.io.pandas import df_checks_from_task_data, df_from_task_data


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
    mds = MDS(
        n_components=2,
        random_state=numpy.random.RandomState(seed=1),
        dissimilarity='precomputed'
    )
    rdm_list = []
    for ds in ds.split_obs('trial'):
        rdm = calc_rdm_euclid(ds)
        rdm.pattern_descriptors['stim_name'] = ds.obs_descriptors['stim_name']
        rdm_list.append(rdm)
    n_trials = len(rdm_list)
    trial_wise_prediction = numpy.full(n_trials, numpy.nan)
    for t in range(n_trials):
        test_rdm = rdm_list[t]
        test_items = test_rdm.pattern_descriptors['stim_name']
        training_rdm_list = [rdm for r, rdm in enumerate(rdm_list) if r != t]
        training_rdms = from_partials(training_rdm_list, descriptor='stim_name')
        training_rdms_scaled = rescale(training_rdms, method='evidence')
        training_rdm = training_rdms_scaled.mean(weights='rescalingWeights')
        training_subset = training_rdm.subset_pattern('stim_name', test_items)
        n_nans = numpy.sum(numpy.isnan(training_subset.dissimilarities))
        if n_nans > 0:
            warn(f'Training trials missing {n_nans} pairs, skipping fold.')
            continue
        predicted = mds.fit_transform(training_subset.get_matrices()[0, :, :])
        predicted_rdm = calc_rdm_euclid(Dataset(predicted))
        predicted_rdm.pattern_descriptors['stim_name'] = training_subset.pattern_descriptors['stim_name']
        predicted_rdm.sort_by(stim_name=test_rdm.pattern_descriptors['stim_name'])
        trial_wise_prediction[t], _ = spearmanr(
            predicted_rdm.dissimilarities[0,:], test_rdm.dissimilarities[0,:])
    return numpy.nanmean(trial_wise_prediction)

def evaluate_checks(data: Dict) -> Tuple[float, DataFrame]:
    """Compare attention check responses to arranged distances

    Args:
        data (Dict): MA task data

    Returns:
        Tuple[float, DataFrame]: _description_
    """
    ## Did you place the top pair further apart than the bottom pair?
    df_ma = df_from_task_data(data)
    stim_set = set([(r.stim_id, r.stim_name) for _, r in df_ma.iterrows()])
    stim_dict = dict(list(stim_set))
    df = df_checks_from_task_data(data)
    triplets = 'stim2_id' in df
    stim_nrs = (1, 2, 3) if triplets else (1, 2)
    pairs = [(1, 2), (2, 3)] if triplets else [(1, 2)]
    for nr in stim_nrs:
        names = [stim_dict[i] for i in df[f'stim{nr}_id']]
        df[f'stim{nr}_name'] = names
    for r, row in df.iterrows():
        for p, pair in enumerate(pairs, start=1):
            pair_pos = []
            for pair_index in pair:
                sid = row[f'stim{pair_index}_id']
                pos = df_ma.loc[(df_ma.trial == row.trial) & (df_ma.stim_id == sid)]
                pair_pos.append(numpy.array([pos.x, pos.y]))
            df.loc[r, f'pair{p}_dist'] = numpy.linalg.norm(pair_pos[0]-pair_pos[1])
    ## below analysis part specific for "repeat" mode with triplets
    df['true'] = df.pair1_dist > df.pair2_dist
    df['acc'] = df.true == (df.label == 'yes')
    ## remove ids for readability
    df = df[[c for c in df.columns if '_id' not in c]]
    return (df.acc.mean(), df)
