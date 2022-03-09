from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from os.path import join, splitext, isdir
from os import mkdir
from tempfile import TemporaryDirectory
from matplotlib.pyplot import close, subplots, text
from matplotlib.patches import Circle
from imageio import get_writer as get_iio_writer, imread
if TYPE_CHECKING:
    from rsatoolbox.data.dataset import Dataset
    from matplotlib.axes._axes import Axes
    from matplotlib.figure import Figure


def arrangement(ds: Dataset, media_path: str, item_size=5.0, ax: Optional[Axes]=None) -> Optional[Figure]:
    """Plot a single trial of a MultiArrangement task

    Args:
        ds (Dataset): rsatoolbox Dataset containing a single trial
        media_path (str): Path to directory containing your stimuli.
        item_size (int): The stimulus size as you configured it on Meadows.
            This is the height of the stimulus in % of the width of the window,
            (note the height of the window is 2x the width). Default is 5.
        ax (Optional[Axes], optional): Matplotlib axes to plot the trial on.
            Defaults to None.

    Raises:
        ValueError: Will throw if Dataset contains multiple trials

    Returns:
        Optional[Figure]: If no axes passed, will create a figure and return it.
    """

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
    fnames = ds.obs_descriptors['stim_name']
    if 'stim_type' in ds.descriptors:
        stim_types = [ds.descriptors['stim_type']]*len(fnames)
    else:
        stim_types = ds.obs_descriptors['stim_type']
    for i in range(ds.n_obs):
        fpath = join(media_path, f'{fnames[i]}.{stim_types[i]}')
        img = imread(fpath)
        x, y = coords[i, :]
        y = -y ## flip given meadows coords vs mpl coords
        ax.imshow(img, zorder=3, extent=(
            x-(item_extent/2),
            x+(item_extent/2),
            y-(item_extent/2),
            y+(item_extent/2),
        )) #(left, right, bottom, top)

    ## add right-side metadata annotations
    trial_start = ds.obs_descriptors['trial_start'][0]
    trial_end = ds.obs_descriptors['trial_end'][0]
    n_actions = ds.obs_descriptors['n_actions'][0]
    dur_secs = (trial_end-trial_start)/1000
    trial_meta = [
        ('items', ds.n_obs, ''),
        ('time/item', dur_secs/ds.n_obs, 's'),
        ('actions/item', n_actions/ds.n_obs, ''),
    ]
    text_kwargs = dict(horizontalalignment='right', verticalalignment='center')
    y_offset = 0.1
    for label, val, suffix in trial_meta:
        content = f'{label}: {round(val, 1)}{suffix} '
        text(half_heigth, half_heigth-y_offset, content, **text_kwargs)
        y_offset += 0.1
    return fig


def arrangements(ds: Dataset, fpath='.', media_path: str='', item_size=5.0):
    """Plot each trial in a MultiArrange Dataset

    Args:
        ds (Dataset): rsatoolbox Dataset for a MultiArrangement task.
            See meadows.io.rsatoolbox.load_dataset()
        fpath (str, optional): Where to save the plots. The format, either a gif
            or a directory with pngs, will be inferred from the extension.
            Defaults to '.', saving pngs in the current directory.
        media_path (str, optional): Path to directory containing your stimuli.
            Defaults to ''.
        item_size (int): The stimulus size as you configured it on Meadows.
            This is the height of the stimulus in % of the width of the window,
            (note the height of the window is 2x the width). Default is 5.
    """
    trial_ds_list = ds.split_obs('trial')
    with create_directory(fpath) as dir_path:
        with get_writer(fpath, mode='I', duration=1) as writer:
            for trial_ds in trial_ds_list:
                fig = arrangement(trial_ds, media_path=media_path, item_size=item_size)
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
