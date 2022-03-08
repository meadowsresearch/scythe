from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from os.path import join, splitext, isdir
from os import mkdir
from tempfile import TemporaryDirectory
from matplotlib.pyplot import close, subplots
from matplotlib.patches import Circle
#from matplotlib.image import imread
from imageio import get_writer as get_iio_writer, imread
if TYPE_CHECKING:
    from rsatoolbox.data.dataset import Dataset
    from matplotlib.axes._axes import Axes
    from matplotlib.figure import Figure


def arrangement(ds: Dataset, media_path: str='', ax: Optional[Axes]=None) -> Optional[Figure]:
    ## size: meadows is Height of the stimuli in % of the width of the field.

    item_size = 5 # should be param
    half_heigth = 1/(1 - (1.25 * 0.04 * item_size)) # half axis height in data pts
    item_extent = half_heigth * 0.04 * item_size    # item height in data pts
    
    trial_idx = ds.obs_descriptors['trial']
    if len(set(trial_idx)) > 1:
        raise ValueError('DataSet contains multiple trials, expecting just one')
    fig = None
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
        y = -y ## flip given meadows coords vs mpl coords
        ax.imshow(img, zorder=3, extent=(
            x-(item_extent/2),
            x+(item_extent/2),
            y-(item_extent/2),
            y+(item_extent/2),
        )) #(left, right, bottom, top)
    return fig


def arrangements(ds: Dataset, fpath='.', media_path: str=''):
    trial_ds_list = ds.split_obs('trial')
    with create_directory(fpath) as dir_path:
        with get_writer(fpath, mode='I', duration=1) as writer:
            for trial_ds in trial_ds_list:
                fig = arrangement(trial_ds, media_path=media_path)
                assert fig is not None
                trial_idx = trial_ds.obs_descriptors['trial']
                fpath = join(dir_path, f'trial_{trial_idx[0]+1}.png')
                fig.savefig(fpath)
                close(fig)
                writer.append_data(imread(fpath))


def is_directory_path(fpath: str) -> bool:
    _, ext = splitext(fpath)
    return ext not in ('.gif',)


def create_directory(fpath: str):
    if is_directory_path(fpath):
        return PermanentDirectory(fpath)
    else:
        return TemporaryDirectory()


def get_writer(fpath: str, mode: str, duration: int):
    if is_directory_path(fpath):
        return DummyWriter()
    else:
        return get_iio_writer(fpath, mode=mode, duration=duration)


class PermanentDirectory(object):
    def __init__(self, dir_path: str):
        self.dir_path = dir_path
    def __enter__(self):
        if not isdir(self.dir_path):
            mkdir(self.dir_path)
        return self.dir_path
    def __exit__(self, type, value, traceback):
        pass

class DummyWriter(object):
    def __init__(self, *args, **kwargs):
        pass
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def append_data(self, img):
        pass
