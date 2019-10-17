import pandas as pd

def predict_occupancy(data):

    road_data = pd.DataFrame(data)

    road_data['occupancy'] = 20

    return road_data.to_dict(orient="records")


'''
# load trained classifier
clf_path = 'lib/models/SentimentClassifier.pkl'
with open(clf_path, 'rb') as f:
    model.clf = pickle.load(f)

# load trained vectorizer
vec_path = 'lib/models/TFIDFVectorizer.pkl'
with open(vec_path, 'rb') as f:
    model.vectorizer = pickle.load(f)
'''
