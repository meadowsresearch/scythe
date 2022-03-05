from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from os.path import join
from matplotlib.pyplot import subplots, Circle, imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
if TYPE_CHECKING:
    from rsatoolbox.data.dataset import Dataset
    from matplotlib.axes._axes import Axes


def arrangement(ds: Dataset, media_path: str='', ax: Optional[Axes]=None):
    trial_idx = ds.obs_descriptors['trial']
    if len(set(trial_idx)) > 1:
        raise ValueError('DataSet contains multiple trials, expecting just one')
    if ax is None:
        fig, ax = subplots(figsize=(8, 8))
    
    coords = ds.get_measurements()
    fnames = ds.obs_descriptors['stim_fname']
    for i in range(ds.n_obs):
        fpath = join(media_path, fnames[i]+'.png')
        ## alternatively use imshow with "extent"
        img = OffsetImage(imread(fpath), zoom=0.2)
        ab = AnnotationBbox(img, coords[i, :], frameon=False)
        ax.add_artist(ab)

    ax.set_xlim([-1.1, 1.1])
    ax.set_ylim([-1.1, 1.1])
    arena = Circle((0, 0), 1, color='w')
    ax.add_patch(arena)
    ax.set_facecolor((0.866, 0.866, 0.866))
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ax.set_title(f'trial {trial_idx[0]+1}')
