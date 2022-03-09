from meadows.io.rsatoolbox import load_dataset
from meadows.plot.multiarrange import arrangement, arrangements
from matplotlib.pyplot import show

## your meadows data file for just one MA task:
fpath = 'tests/data/Meadows_myExp_v_v2_profound-mammoth_1_tree.json'

## this reads the data and turns it into an rsatoolbox "Dataset" object:
ds = load_dataset(fpath)

## this plots all trials as a gif:
arrangements(ds, 'trials.gif', media_path='/path/to/my/stimuli')

## or if you wish to see just one trial, extract the data for trial 5:
ds_trial5 = ds.subset_obs('trial', 5)

## this plots trial 5 in a new window:
arrangement(ds_trial5, media_path='/path/to/my/stimuli')
show()
