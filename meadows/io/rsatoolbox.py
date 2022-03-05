from rsatoolbox.data.dataset import Dataset
from meadows.io.pandas import df_from_tree_file


def load_dataset(fpath: str) -> Dataset:
    df = df_from_tree_file(fpath)
    return Dataset.from_df(df)
