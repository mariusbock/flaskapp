import pandas as pd

test = pd.read_json("../../static/parsed_data/points.json", orient="records")

print(test.head())
print(test['point_id'].value_counts())