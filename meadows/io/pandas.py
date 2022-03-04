from __future__ import annotations
from typing import Dict, Optional
import json
from pandas import DataFrame
from rsatoolbox.io.meadows import extract_filename_segments


def df_from_tree_file(fpath: str) -> DataFrame:
    """Read data from json file and return as pandas DataFrame

    Currently only supports single task, single participant MA 

    Args:
        fpath (str): full path to json file

    Returns:
        DataFrame: long-form DataFrame
    """
    meta = extract_filename_segments(fpath)
    with open(fpath) as fhandle:
        data = json.load(fhandle)
    return df_from_task_data(data, meta)

def df_from_task_data(data: dict, meta: Optional[Dict]=None) -> DataFrame:
    """Create a pandas DataFrame for MultiArrange task data

    Args:
        data (dict): Data for one MultiArrangement task
        meta (Optional[Dict], optional): Optional dictionary with metadata.
            Defaults to None.

    Returns:
        DataFrame: rows are item placements, with xy coordinates, trial index
            and more as columns.
    """
    if meta is None:
        meta = dict()
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
                #trial_start=trial['start'],
                #trial_end=trial['end'],
            ))
    df = DataFrame(rows)
    df['task_name'] = data['task']['name']
    for key in ['participant', 'task_index', 'experiment_name']:
        if key in meta:
            df[key] = meta[key]
    return df
