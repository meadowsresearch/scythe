from __future__ import annotations
import json
from pandas import DataFrame
from rsatoolbox.io.meadows import extract_filename_segments


def load_dataframe(fpath: str) -> DataFrame:
    """Read data from json file and return as pandas DataFrame

    Currently only supports single task, single participant MA 

    Args:
        fpath (str): full path to json file

    Returns:
        DataFrame: long-form DataFrame
    """
    info = extract_filename_segments(fpath)
    with open(fpath) as fhandle:
        data = json.load(fhandle)
    stimuli = dict([(s['id'], s['name']) for s in data['stimuli']])
    rows = []
    for t, trial in enumerate(data['trials']):
        for position in trial['positions']:
            rows.append(dict(
                stim_id=position['id'],
                stim_fname=stimuli[position['id']],
                x=position['x'],
                y=position['y'],
                trial=t,
                trial_start=trial['start'],
                trial_end=trial['end'],
            ))
    df = DataFrame(rows)
    df['task_name'] = data['task']['name']
    df['participant'] = info['participant']
    df['task_index'] = info['task_index']
    df['experiment_name'] = info['experiment_name']
    return df
