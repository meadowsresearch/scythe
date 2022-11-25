import pandas
from meadows.cfpt import score_cfpt

annotations = pandas.read_csv('/path/to/my/file')
out_df = score_cfpt(annotations)

# first participant, first trial:
out_df.iloc[0].score
# total (avg across trials) score per participant:
out_df.groupby('participation').mean().score.to_dict()