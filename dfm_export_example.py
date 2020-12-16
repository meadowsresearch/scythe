"""
## fully array based:

trials x meta (object, response, etc), dataframe
objects x features x params (freq, ori, x, y)
trials x (max) features, dtype= boolean
objects x gabvects


PARAMS (6): size, freq, oris, phase, x, y;
"""
from os.path import join, expanduser
import json
import pandas
from meadows.rng import RandomNumberGenerator

data_dir = expanduser('~/Data/scythe/dfm')
fname = 'Meadows_GaborsTest_v_v1_meet-wombat_1_annotations.csv'
fpath = join(data_dir, fname)
rng = RandomNumberGenerator()

## read annotations and embellish
df = pandas.read_csv(fpath)
df['cond'] = df.stim1_name.str.split('_').str[0]
conditions = sorted(df.cond.unique())
df['correct'] = df.label.str.split('_').str[0].astype(bool)
df['nfeats'] = df.label.str.split('_').str[1].astype(int)
df['seed'] = df.label.str.split('_').str[2].astype(int)
stim_ids = df.stim1_id.unique()
df = df.drop(['stim2_id', 'stim2_name','stim3_id', 'stim3_name'], axis=1)

## read features
stim_dfs = dict()
size = -1
for sid in stim_ids:
    fpath = join(data_dir, f'{sid}.gabors')
    with open(fpath) as fhandle:
        data = json.load(fhandle)
    name = data['source']['name']
    size = data['settings']['size']
    freqs = data['settings']['frequencies']
    oris = data['settings']['orientations']
    stim_df = pandas.DataFrame(data['features'])
    stim_df['frequency'] = [freqs[f] for f in stim_df.f]
    stim_df['orientation'] = [oris[o] for o in stim_df.o]
    stim_dfs[name] = stim_df

## from json can get size, from annotations have to load features
feat_idx = []
for t, trial in df.iterrows():
    nfeats_max = len(stim_dfs[trial.stim1_name].index)
    feat_idx.append(rng.sample_indices(
        pop_size=nfeats_max,
        n=trial.nfeats,
        seed=trial.seed
    ))
df['feat_idx'] = feat_idx

## bool array
max_feats = max([len(sdf.index) for sdf in stim_dfs.values()])