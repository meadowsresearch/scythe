from __future__ import annotations
from pandas import DataFrame
import numpy
from dateutil.parser import isoparse as parse_iso_dt


def score_cfpt(annotations: DataFrame) -> DataFrame:
    """Trial-wise score and RT for a CFPT OrderSort task annotations

    To get a dictionary of total scores by participant:
    ```
        df.groupby('participation').mean().score.to_dict()
    ```

    Args:
        annotations (DataFrame): Annotations

    Returns:
        Tuple[Dict[str, int], DataFrame]: First element is the
            dictionary of total scores,
            second a copy of the dataframe with a new "score" column
    """
    MAX_DEVIATION = 18
    rows = []
    for _, trial in annotations.iterrows():
        start_dt = parse_iso_dt(trial.start)
        resp_dt = parse_iso_dt(trial.resp)
        n_moves = int(trial.label.split('_')[0])
        stims_str = '_'.join(trial.label.split('_')[1:])
        parts = dict()
        for p, part in enumerate(['cond', 'id', 'mix']):
            parts[part] = [s.split('_')[p] for s in stims_str.split('-')]
        deviations = numpy.abs(numpy.argsort(parts['mix']) - numpy.arange(6)).sum()
        rows.append(dict(
            participation=trial.participation,
            identity=int(parts['id'][0]),
            condition=parts['cond'][0],
            n_moves=n_moves,
            rt=(resp_dt-start_dt).total_seconds(),
            deviations=deviations,
            score=100*(1-(deviations/MAX_DEVIATION))
        ))
    return DataFrame(rows)
    