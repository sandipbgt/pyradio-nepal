import json
from collections import OrderedDict
import os

# scrape radio stations
def scrape_stations():
    with open('/home/sandip/Desktop/stations.json', 'r') as f:
        stations_json = json.loads(f.read())
        stations = []
        for station in stations_json['tables'][0]['rows']:
            station = OrderedDict([
                            ('name', station['name'].strip()),
                            ('location', station['location'].strip()),
                            ('frequency', station['frequency'].strip()),
                            ('stream_url', station['streamingURL']),
                        ])
            stations.append(station)
    return stations

# export the radio stations to simple json format in user's home directory
def export_stations(stations=[], filename='.radio_stations_json'):
    file_path = os.path.join(os.path.expanduser('~'), filename)
    with open(file_path, 'w') as f:
        f.write(json.dumps(stations, indent=4))

# pretty print all the radio stations
def pretty_print(stations, search=None):
    from terminaltables import AsciiTable

    datas = [['S.N.', 'NAME', 'LOCATION', 'FREQUENCY'],]

    for counter, station in enumerate(stations):
        if search and search in station['name'] or not search:
            datas.append([counter + 1, station['name'], station['location'], station['frequency']])

    table = AsciiTable(datas)
    print(table.table)

def main():
    stations = scrape_stations()
    export_stations(stations)
    pretty_print(stations)

if __name__ == '__main__':
    main()
