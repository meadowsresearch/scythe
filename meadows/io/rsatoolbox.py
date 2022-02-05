from rsatoolbox.data.dataset import Dataset
from meadows.io.pandas import load_dataframe


def load_dataset(fpath: str) -> Dataset:
    df = load_dataframe(fpath)
    return Dataset.from_DataFrame(df)
