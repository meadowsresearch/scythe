"""In this demo we analyze data from the object memory
tasks with horses, bodies, cars, bikes and
faces.
"""

import pandas
from meadows.cmt import score_cmt

annotations = pandas.read_csv('/path/to/my/file')
## faces, bikes, bodies, cars
out_score, out_df = score_cmt(annotations, 'faces')

## total score:
print(f'score: {out_score}')

# first participant, first trial:
out_df.iloc[0].score
# total (avg across trials) score per participant:
out_df.groupby('participation').mean().score.to_dict()