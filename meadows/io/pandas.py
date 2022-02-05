from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
import json
from pandas import DataFrame


def load_dataframe(fpath: str) -> DataFrame:
    with open(fpath) as fhandle:
        data = json.load(fhandle)
    return DataFrame([])
