import requests
import logging
from . import player
import json
import os

# this is a test url, create a live server.
STATION_FETCH_URL = 'https://stations.radiostationserver.com'


def get_player():
    """
    :returns a radio instance
    """
    radio = None
    try:
        radio = player.VlcPlayer()
    except Exception as e:
        logging.warn('Failed to load first player option, trying another, %s' % str(e))
        radio = player.MpPlayer()
    finally:
        return radio


def pretty_print_stations(stations=[], search=None):
    """
    prints all the radio stations in a table
    """
    from terminaltables import AsciiTable
    data = [['S.N.', 'NAME', 'LOCATION', 'FREQUENCY']]
    data.extend([[v['count'], v['name'], v['location'], v['frequency']] for v in stations
                        if search and search.lower() in v['name'].lower() or not search])
    print(AsciiTable(data).table)


def get_stations():
    """
    :returns list of all the(available) radio stations fetching from a server
    helps to manage station list in one place
    """
    stations_json = []
    try:
        response = requests.get(STATION_FETCH_URL, timeout=60, verify=False)
        json_content = json.loads(response.content)
        stations_json = json_content.get('stations', []) or []
    except Exception as e:
        logging.warn('Unable to load data from server. Processing local data.')
        stations_json = get_stations_from_json()
    finally:
        return _format_station_json_to_dict(stations_json)


def _format_station_json_to_dict(json_content):
    """
    iterates json content, makes a dict adds it to a list
    :returns a list of dictionary
    """
    stations = []
    required_fields = ['name', 'location', 'frequency', 'stream_url']
    for counter, station in enumerate(json_content, start=1):
        station = {field: station[field] for field in required_fields if field in station}
        station.update({"count": counter})
        stations.append(station)

    return stations


def get_stations_from_json():
    """
    :returns station list reading from static json file
    """
    parent_dir = os.path.normpath(os.path.abspath(os.path.dirname(__file__)) + os.sep + os.pardir)
    json_file_path = os.path.join(parent_dir, 'data', '.radio_stations_json')
    with open(json_file_path, 'r') as f:
        stations = json.loads(f.read())

    return stations


def main():
    stations = get_stations()
    pretty_print_stations(stations)
    print(get_player())

if __name__ == '__main__':
    main()
