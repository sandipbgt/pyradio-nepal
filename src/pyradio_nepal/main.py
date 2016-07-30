from . import player
import os
import json

#radio = player.MpPlayer()
radio = player.VlcPlayer()

# relative path to package
def rel(path):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', path)

file_path = rel('.radio_stations_json')

# get list of stations from json file
def get_stations():
    stations = []
    with open(file_path, 'r') as f:
        stations_json = json.loads(f.read())
        for counter, station in enumerate(stations_json):
            stations.append([counter + 1, station['name'], station['location'], station['frequency'], station['stream_url']])
        return stations

# pretty print all the radio stations
def pretty_print_stations():
    from terminaltables import AsciiTable
    datas = [['S.N.', 'NAME', 'LOCATION', 'FREQUENCY']]
    with open(file_path, 'r') as f:
        stations_json = json.loads(f.read())
        for counter, station in enumerate(stations_json):
            datas.append([counter + 1, station['name'], station['location'], station['frequency']])
    print(AsciiTable(datas).table)

# start the player
def run():
    stations = get_stations()
    play = True
    current = None

    while play:
        user_input = input("Enter station number ({})> ".format(current)).strip()
        
        if user_input == "exit":
            user_input = 0
            radio.close()
            play = False
        elif user_input == 'list':
            pretty_print_stations()
            user_input = 0

        try:
            num = int(user_input)
            if (num > 0):
                try:
                    station = stations[num - 1]
                    radio.play(station[4])
                    print("Playing: {} @ {}".format(station[1], station[3]))
                    current = station[1]
                except IndexError:
                    print("Invalid station number")
        except ValueError:
            print("Invalid station number")

def main():
    run()

if __name__ == '__main__':
    main()
    