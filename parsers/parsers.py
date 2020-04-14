import xml.etree.ElementTree as et
from datetime import timedelta

import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from pytz import timezone

pd.set_option('display.expand_frame_repr', False)

"""
This file contains all parsers used to bring the data in the data schema format. NOTE: this file is to be handled 
separately from the project. The needed packages are not listed in the requirements file.
"""


def parse_dynamic_traffic(filename):
    """
    Function that parses the dynamic traffic data from the MDM portal and transforms into TrafficOccupancy table
    :param filename: path to dynamic data (XML)
    :return: pandas dataframe containing TrafficOccupancy data
    """
    # used etree to navigate XML
    xtree = et.parse(filename)
    root = xtree.getroot()

    result = pd.DataFrame(columns=['road_id', 'time', 'occupancy', 'vehicle_flow'])

    # find attributes in xml and save to dataframe
    for elem in root.iter('{http://datex2.eu/schema/2/2_0}siteMeasurements'):
        road_id = elem.find('{http://datex2.eu/schema/2/2_0}measurementSiteReference').attrib['id']
        time = elem.find('{http://datex2.eu/schema/2/2_0}measurementTimeDefault').text
        occupancy = elem.find(
            '{http://datex2.eu/schema/2/2_0}measuredValue[@index="300"]/{http://datex2.eu/schema/2/2_0}measuredValue/{http://datex2.eu/schema/2/2_0}basicData/{http://datex2.eu/schema/2/2_0}occupancy/{http://datex2.eu/schema/2/2_0}percentage').text
        vehicle_flow = elem.find(
            '{http://datex2.eu/schema/2/2_0}measuredValue[@index="100"]/{http://datex2.eu/schema/2/2_0}measuredValue/{http://datex2.eu/schema/2/2_0}basicData/{http://datex2.eu/schema/2/2_0}vehicleFlow/{http://datex2.eu/schema/2/2_0}vehicleFlowRate').text
        result = result.append({'road_id': road_id, 'time': time, 'occupancy': occupancy, 'vehicle_flow': vehicle_flow},
                               ignore_index=True)

    return result


def parse_static_traffic(filename):
    """
    Function that parses the static traffic data from the MDM portal and transforms into Roads, Points and Road_Points
    table
    :param filename: path to static data (XML)
    :return: three pandas dataframes for respective tables
    """
    # used etree to navigate XML
    xtree = et.parse(filename)
    root = xtree.getroot()

    roads = pd.DataFrame(columns=['road_id', 'road_name', 'type', 'numberOfLanes'])
    points = pd.DataFrame(columns=['road_id', 'point_id', 'longitude', 'latitude'])
    road_points = pd.DataFrame(columns=['point_id', 'road_id'])

    # find attributes in xml and save to dataframes
    for elem in root.iter('{http://datex2.eu/schema/2/2_0}measurementSiteRecord'):
        road_id = elem.find('{http://datex2.eu/schema/2/2_0}measurementSiteIdentification').text
        location_elem = elem.find('{http://datex2.eu/schema/2/2_0}measurementSiteLocation')
        start_point = location_elem.find(
            '{http://datex2.eu/schema/2/2_0}pointExtension/{http://datex2.eu/schema/2/2_0}extendedPoint/{http://datex2.eu/schema/2/2_0}additonalPointAlongLinearElement/{http://datex2.eu/schema/2/2_0}pointAlongLinearElement/{http://datex2.eu/schema/2/2_0}linearElement/{http://datex2.eu/schema/2/2_0}startPointOfLinearElement')
        end_point = location_elem.find(
            '{http://datex2.eu/schema/2/2_0}pointExtension/{http://datex2.eu/schema/2/2_0}extendedPoint/{http://datex2.eu/schema/2/2_0}additonalPointAlongLinearElement/{http://datex2.eu/schema/2/2_0}pointAlongLinearElement/{http://datex2.eu/schema/2/2_0}linearElement/{http://datex2.eu/schema/2/2_0}endPointOfLinearElement')
        road_name = location_elem.find(
            '{http://datex2.eu/schema/2/2_0}pointExtension/{http://datex2.eu/schema/2/2_0}extendedPoint/{http://datex2.eu/schema/2/2_0}additonalPointAlongLinearElement/{http://datex2.eu/schema/2/2_0}pointAlongLinearElement/{http://datex2.eu/schema/2/2_0}linearElement/{http://datex2.eu/schema/2/2_0}roadName/{http://datex2.eu/schema/2/2_0}values/{http://datex2.eu/schema/2/2_0}value').text
        numberOfLanes = elem.find('{http://datex2.eu/schema/2/2_0}measurementSiteNumberOfLanes').text

        roads = roads.append(
            {'road_id': road_id, 'road_name': road_name, 'type': "car", 'numberOfLanes': numberOfLanes},
            ignore_index=True)

        start_id = start_point.find('{http://datex2.eu/schema/2/2_0}referentIdentifier').text
        start_latitude = start_point.find(
            '{http://datex2.eu/schema/2/2_0}pointCoordinates/{http://datex2.eu/schema/2/2_0}latitude').text
        start_longitude = start_point.find(
            '{http://datex2.eu/schema/2/2_0}pointCoordinates/{http://datex2.eu/schema/2/2_0}longitude').text

        points = points.append(
            {'road_id': road_id, 'point_id': start_id, 'latitude': start_latitude, 'longitude': start_longitude},
            ignore_index=True)
        road_points = road_points.append({'road_id': road_id, 'point_id': start_id}, ignore_index=True)

        for loc_elem in location_elem.iter('{http://datex2.eu/schema/2/2_0}intermediatePointOnLinearElement'):
            point_id = loc_elem.find(
                '{http://datex2.eu/schema/2/2_0}referent/{http://datex2.eu/schema/2/2_0}referentIdentifier').text
            latitude = loc_elem.find(
                '{http://datex2.eu/schema/2/2_0}referent/{http://datex2.eu/schema/2/2_0}pointCoordinates/{http://datex2.eu/schema/2/2_0}latitude').text
            longitude = loc_elem.find(
                '{http://datex2.eu/schema/2/2_0}referent/{http://datex2.eu/schema/2/2_0}pointCoordinates/{http://datex2.eu/schema/2/2_0}longitude').text

            points = points.append(
                {'road_id': road_id, 'point_id': point_id, 'latitude': latitude, 'longitude': longitude},
                ignore_index=True)
            road_points = road_points.append({'road_id': road_id, 'point_id': point_id}, ignore_index=True)

        end_id = end_point.find(
            '{http://datex2.eu/schema/2/2_0}referentIdentifier').text
        end_latitude = end_point.find(
            '{http://datex2.eu/schema/2/2_0}pointCoordinates/{http://datex2.eu/schema/2/2_0}latitude').text
        end_longitude = end_point.find(
            '{http://datex2.eu/schema/2/2_0}pointCoordinates/{http://datex2.eu/schema/2/2_0}longitude').text

        points = points.append(
            {'road_id': road_id, 'point_id': end_id, 'latitude': end_latitude, 'longitude': end_longitude},
            ignore_index=True)
        road_points = road_points.append({'road_id': road_id, 'point_id': end_id}, ignore_index=True)

    return roads, road_points, points


def parse_dates(messe_path, holiday_s_path, holiday_c_path, school_holiday_path):
    """
    Parses event data (CSVs) to one dataframe (Events table)
    :param messe_path: path to messe dates file (for now just in Frankfurt)
    :param holiday_s_path: path to state holiday dates file (for now just Hessen)
    :param holiday_c_path: path to nationwide holiday dates file
    :param school_holiday_path: path to school holiday dates file (for now just Hessen)
    :return:
    """
    # create dataframe of events from separate CSV files
    school_break_state = pd.read_csv(school_holiday_path, parse_dates=['Start Time', 'End Time'])
    holiday_state = pd.read_csv(holiday_s_path, parse_dates=['Start Time', 'End Time'])
    holiday_country = pd.read_csv(holiday_c_path, parse_dates=['Start Time', 'End Time'])
    messe = pd.read_csv(messe_path, parse_dates=['Start Time', 'End Time'])

    school_break_state["Validity_Type"] = "state"
    holiday_state["Validity_Type"] = "state"
    messe["Validity_Type"] = "city"
    holiday_country["Validity_Type"] = "country"

    school_break_state["Valid_For"] = "Hessen"
    holiday_state["Valid_For"] = "Hessen"
    messe["Valid_For"] = "Frankfurt am Main"
    holiday_country["Valid_For"] = "Deutschland"

    school_break_state["Type"] = "school_holiday"
    holiday_state["Type"] = "state_holiday"
    messe["Type"] = "messe"
    holiday_country["Type"] = "state_holiday"

    school_break_state['Start Time'] = school_break_state['Start Time'].apply(
        lambda x: x.replace(tzinfo=timezone("UTC")))
    holiday_state['Start Time'] = holiday_state['Start Time'].apply(lambda x: x.replace(tzinfo=timezone("UTC")))
    messe['Start Time'] = messe['Start Time'].apply(lambda x: pd.to_datetime(x).tz_convert("UTC")) + timedelta(hours=2)
    holiday_country['Start Time'] = holiday_country['Start Time'].apply(lambda x: x.replace(tzinfo=timezone("UTC")))

    school_break_state['End Time'] = school_break_state['End Time'].apply(lambda x: x.replace(tzinfo=timezone("UTC")))
    holiday_state['End Time'] = holiday_state['End Time'].apply(lambda x: x.replace(tzinfo=timezone("UTC")))
    messe['End Time'] = messe['End Time'].apply(lambda x: pd.to_datetime(x).tz_convert("UTC")) + timedelta(hours=2)
    holiday_country['End Time'] = holiday_country['End Time'].apply(lambda x: x.replace(tzinfo=timezone("UTC")))

    result_table = pd.DataFrame()
    result_table["name"] = pd.concat(
        [school_break_state["Summary"], holiday_state["Summary"], holiday_country["Summary"], messe["Summary"]])
    result_table["type"] = pd.concat(
        [school_break_state["Type"], holiday_state["Type"], holiday_country["Type"], messe["Type"]])
    result_table["validity_type"] = pd.concat(
        [school_break_state["Validity_Type"], holiday_state["Validity_Type"], holiday_country["Validity_Type"],
         messe["Validity_Type"]])
    result_table["valid_for"] = pd.concat(
        [school_break_state["Valid_For"], holiday_state["Valid_For"], holiday_country["Valid_For"],
         messe["Valid_For"]])
    result_table["start_date"] = pd.concat(
        [school_break_state["Start Time"], holiday_state["Start Time"], holiday_country["Start Time"],
         messe["Start Time"]])
    result_table["end_date"] = pd.concat(
        [school_break_state["End Time"], holiday_state["End Time"], holiday_country["End Time"], messe["End Time"]])

    return result_table


def get_coord_info(data):
    """
    Funtion that retrieves geo metadata from point data (long and lat coordinate).
    :param data: pandas dataframe containing latitude & longitude column (e.g. Points)
    :return: pandas dataframe with geo metadata columns appended
    """
    # use geolocater to retrieve geo-information (used a RateLimiter to avoid being blocked by API)
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
    return data


if __name__ == '__main__':
    """
    Here is the workflow how the above functions were used to create CSV in parsed_data folder.
    NOTE: the geoinformation retrieval takes a lot of time and is therefore commented out.
    """
    # Parse event data and save to CSV
    events = parse_dates(messe_path="raw_data/MesseTermine-2019.csv",
                         holiday_s_path="raw_data/gesetzliche_feiertage_hessen_2019.csv",
                         holiday_c_path="raw_data/gesetzliche_feiertage_deutschland_2019.csv",
                         school_holiday_path="raw_data/ferien_hessen_2019.csv")
    events = events.append(parse_dates(messe_path="raw_data/MesseTermine-2020.csv",
                                       holiday_s_path="raw_data/gesetzliche_feiertage_hessen_2020.csv",
                                       holiday_c_path="raw_data/gesetzliche_feiertage_deutschland_2020.csv",
                                       school_holiday_path="raw_data/ferien_hessen_2020.csv"))
    events.to_csv("parsed_data/events.csv", index=None)

    # Parse static & dynamic traffic data and save to CSV
    roads, road_points, points = parse_static_traffic("raw_data/static_road_data.xml")
    traffic_occupancy = parse_dynamic_traffic("raw_data/traffic_dynamic.xml")

    roads.to_csv("parsed_data/roads.csv", index=None, sep=";")
    road_points.to_csv("parsed_data/road_points.csv", index=None, sep=";")
    points.to_csv("parsed_data/points.csv", index=None, sep=";")
    traffic_occupancy.to_csv("parsed_data/traffic_occupancy.csv", index=None, sep=";")

    ## Uncomment this section if you want point_info data to be retrieved (Note: this will take some time!)
    # points_info = get_coord_info(points)
    # points_info.to_csv('points_info.csv', sep=";")
