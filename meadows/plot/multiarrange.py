from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from os.path import join
from matplotlib.pyplot import subplots, Circle #, imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.image import imread
if TYPE_CHECKING:
    from rsatoolbox.data.dataset import Dataset
    from matplotlib.axes._axes import Axes


def arrangement(ds: Dataset, media_path: str='', ax: Optional[Axes]=None):
    ## size: meadows is Height of the stimuli in % of the width of the field.
    ## arena =

    item_size = 10 # should be param
    half_heigth = 1/(1 - (1.25 * 0.04 * item_size)) # half axis height in data pts
    item_extent = half_heigth * 0.04 * item_size    # item height in data pts
    
    trial_idx = ds.obs_descriptors['trial']
    if len(set(trial_idx)) > 1:
        raise ValueError('DataSet contains multiple trials, expecting just one')
    if ax is None:
        fig, ax = subplots(figsize=(8, 8))

    ax.set_xlim([-half_heigth, half_heigth])
    ax.set_ylim([-half_heigth, half_heigth])
    arena = Circle((0, 0), 1, color='w')
    ax.add_patch(arena)
    ax.set_facecolor((0.866, 0.866, 0.866)) # #DDD, meadows bg color
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ax.set_title(f'trial {trial_idx[0]+1}')

    coords = ds.get_measurements()
    fnames = ds.obs_descriptors['stim_fname']
    for i in range(ds.n_obs):
        fpath = join(media_path, fnames[i]+'.png')
        img = imread(fpath)
        x, y = coords[i, :]
        ax.imshow(img, zorder=3, extent=(
            x-(item_extent/2),
            x+(item_extent/2),
            y-(item_extent/2),
            y+(item_extent/2),
        )) #(left, right, bottom, top)
