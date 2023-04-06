from os.path import expanduser
import json
import seaborn, pandas
import matplotlib.pyplot as plt

fpath = expanduser('~/data/meadows/Meadows_mmmouse_v_vdesign_preview_1_tree.json')
with open(fpath) as fhandle:
    data = json.load(fhandle)
mouse_data = data['trials'][0]['mouse']

df = pandas.DataFrame(mouse_data['frames'])
seaborn.scatterplot(df, x='x', y='y', hue='t')