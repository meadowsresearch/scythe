from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Union, Literal
from meadows.keys import CFMT_KEY, BODIES_KEY, CARS_KEY, BIKES_KEY
if TYPE_CHECKING:
    from pandas.core.frame import DataFrame
CmtSubtype = Union[
    Literal['faces'],
    Literal['bodies'],
    Literal['horses'],
    Literal['bikes'],
    Literal['cars']
]
KEYS = {'faces': CFMT_KEY, 'bodies': BODIES_KEY, 'cars': CARS_KEY, 'bikes': BIKES_KEY}


def score_cfmt(annotations: DataFrame) -> Tuple[int, DataFrame]:
    """Determine total score and mark correct responses

    Args:
        annotations (DataFrame): Annotations

    Returns:
        Tuple[int, DataFrame]: First element is the total score,
            second a copy of the dataframe with a new "correct" column
    """
    return score_cmt(annotations, 'faces')

def score_cmt(annotations: DataFrame, subtype: CmtSubtype) -> Tuple[int, DataFrame]:
    """Determine total score and mark correct responses

    Args:
        annotations (DataFrame): Annotations

    Returns:
        Tuple[int, DataFrame]: First element is the total score,
            second a copy of the dataframe with a new "correct" column
    """
    scored = annotations.copy()
    scored = scored.loc[~scored.stim1_name.str.contains('pract')]
    key = KEYS[subtype]
    def isCorrect(row):
        return key[row.stim1_name] == int(row.label)
    scored['correct'] = scored.apply(isCorrect, axis=1)
    return (scored.correct.values.sum(), scored)
