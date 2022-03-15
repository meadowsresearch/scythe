from __future__ import annotations
from typing import Dict, Optional
import json
from pandas import DataFrame
from dateutil.parser import isoparse as parse_iso_dt
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
    stim_names = dict([(s['id'], s['name']) for s in data['stimuli']])
    stim_types = dict([(s['id'], s['type']) for s in data['stimuli']])
    rows = []
    for t, trial in enumerate(data['trials']):
        actions = [e for e in trial['log'] if e[1] in ('placed', 'displaced')]
        start_event = [e for e in trial['log'] if e[1] == 'logStarted'][0]
        finish_event = [e for e in trial['log'] if e[1] == 'finish'][0]
        for position in trial['positions']:
            rows.append(dict(
                stim_id=position['id'],
                stim_name=stim_names[position['id']],
                stim_type=stim_types[position['id']],
                x=position['x'],
                y=position['y'],
                trial=t,
                n_actions=len(actions),
                trial_start=start_event[0],
                trial_end=finish_event[0],
            ))
        
    df = DataFrame(rows)
    df['task_name'] = data['task']['name']
    for key in ['participant', 'task_index', 'experiment_name', 'version']:
        if key in meta:
            df[key] = meta[key]
    return df

def df_checks_from_task_data(data: dict) -> DataFrame:
    """Create a dataframe with attention checks from an MA task

    Args:
        data (dict): data for one task such as loaded from json

    Returns:
        DataFrame: Each row is one check
    """
    rows = []
    for t, trial in enumerate(data['trials']):
        for annotation in trial['annotations']:
            row = dict(
                trial=t,
                stim1_id=annotation['ids'][0],
                stim2_id=annotation['ids'][1],
                label=annotation['label'],
                start=parse_iso_dt(annotation['start']),
                resp=parse_iso_dt(annotation['resp']),
            )
            if len(annotation['ids']) > 2:
                row['stim3_id'] = annotation['ids'][3]
            rows.append(row)
    return DataFrame(rows)
