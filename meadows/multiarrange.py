"""Tools related to the Multiple Arrangements task
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from rsatoolbox.data import Dataset


def calc_trial_rep(ds: Dataset) -> float:
    """Calculate MA Trial Replicability Index

    Args:
        ds (Dataset): rsatoolbox Dataset with the MA experiment data

    Returns:
        float: replicability index
    """
    return 0.0
