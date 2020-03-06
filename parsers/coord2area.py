import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from shapely.geometry.polygon import Polygon
from shapely.geometry.point import Point



def get_coord_info(data):
    geolocator = Nominatim(timeout=10)
    geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1)
    for index, row in data.iterrows():
        coord_pair = str(row['latitude']) + ", " + str(row['longitude'])
        location = geocode(coord_pair).raw
        data.at[index, 'point_id'] = row['point_id']
        data.at[index, 'road'] = location.get('address').get('road')
        data.at[index, 'suburb'] = location.get('address').get('suburb')
        data.at[index, 'city_district'] = location.get('address').get('city_district')
        data.at[index, 'city'] = location.get('address').get('city')
        data.at[index, 'state_district'] = location.get('address').get('state_district')
        data.at[index, 'state'] = location.get('address').get('state')
        data.at[index, 'postcode'] = location.get('address').get('postcode')
        data.at[index, 'country'] = location.get('address').get('country')
        print(location)
    return data


if __name__ == '__main__':
    input = pd.read_json('parser_test_data/points.json', orient='records')
    output = get_coord_info(input)
    output.to_csv('points_info.csv', sep=";", na_rep="NaN")
    print(output)

