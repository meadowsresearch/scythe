from warnings import warn
import pkg_resources
from os.path import expanduser, join
import numpy
from scipy.stats import spearmanr
from sklearn.manifold import MDS
from rsatoolbox.data import Dataset
from rsatoolbox.rdm.calc import calc_rdm_euclid
from rsatoolbox.rdm.combine import from_partials, rescale
from meadows.io.rsatoolbox import load_dataset

fname = 'Meadows_myExp_v_v2_profound-mammoth_1_tree.json'
#fpath = pkg_resources.resource_filename('tests', 'data/' + fname)
fname = 'Meadows_maqual_short_v_v2_profound-mammoth_1_tree.json'
fpath = join(expanduser('~/Data/maqual/test/'), fname)
ds = load_dataset(fpath)

# ds = Dataset(
#     measurements=numpy.array([
#         [-1,    0   ], # trial 1, courgette
#         [-0.9,  0.1 ], # trial 1, cucumber
#         [ 0.4,  0.4 ], # trial 1, banana
#         [ 0.7,  0.7 ], # trial 1, apple
#         [ 0.6,  0.75], # trial 1, orange
#         [ 0,   -1   ], # trial 2, banana
#         [ 0.2,  0.9 ], # trial 2, apple
#         [-0.2,  0.9 ], # trial 2, orange
#         [ 0,    -1  ], # trial 3, courgette
#         [-0.1,  0.8 ], # trial 3, cucumber
#         [ 0,    1   ], # trial 3, banana
#     ]),
#     descriptors=dict(foo='bar'),
#     obs_descriptors=dict(
#         trial=[1,1,1,1,1,2,2,2,3,3,3],
#         stim_name=['co', 'cu', 'ba', 'ap', 'or', 'ba', 'ap', 'or', 
#             'co', 'cu', 'ba']
#     ),
#     channel_descriptors=dict(dimension=['x', 'y'])
# )

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
for t in reversed(range(n_trials)):
    print(t)
    test_rdm = rdm_list[t]
    test_items = test_rdm.pattern_descriptors['stim_name'] ## TODO must be intersection instead
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
    trial_wise_prediction[t], p = spearmanr(
        predicted_rdm.dissimilarities[0,:], test_rdm.dissimilarities[0,:])
