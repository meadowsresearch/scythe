from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from matplotlib.pyplot import subplots
if TYPE_CHECKING:
    from rsatoolbox.data.dataset import Dataset
    from matplotlib.axes._axes import Axes


def arrangement(ds: Dataset, ax: Optional[Axes]=None):
    trial_idx = ds.obs_descriptors['trial']
    if len(set(trial_idx)) > 1:
        raise ValueError('DataSet contains multiple trials, expecting just one')
    if ax is None:
        fig, ax = subplots()
    ax.set_title(f'trial {trial_idx[0]+1}')
    