def feature_engineer_dataset(data):
    data['last_occupancy'] = data.groupby(['id'])['occupancy'].shift()
    # data['last_occupancy_diff'] = data.groupby(['id'])['last_occupancy'].diff()
    data['last-1_occupancy'] = data.groupby(['id'])['occupancy'].shift(2)
    # data['last-1_occupancy_diff'] = data.groupby(['id'])['last-1_occupancy'].diff()
    data['last-5_occupancy'] = data.groupby(['id'])['occupancy'].shift(5)
    # data['last-5_occupancy_diff'] = data.groupby(['id'])['last-5_occupancy'].diff()

    data = data.dropna()
    print("\n Feature engineered dataset")
    print(data.head())
    print(data.shape)

    return data
