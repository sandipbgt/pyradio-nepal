
import sys
import logging
from .libradio import utils


def run():
    """
    starts the player
    """
    radio = utils.get_player()
    if not radio:
        logging.error("Player not available, exiting now!")
        sys.exit(0)

    stations = utils.get_stations()
    play = True
    current = None
    while play:
        user_input = input("Enter station number ({})> ".format(current)).strip()
        
        if user_input == "exit":
            radio.close()
            play = False
        elif user_input == 'list':
            utils.pretty_print_stations(stations)
            continue

        try:
            num = int(user_input)
            if num > 0:
                try:
                    station = stations[num - 1]
                    radio.play(station['stream_url'])
                    print("Playing: {} @ {} MHz, {}".format(station['name'], station['frequency'], station['location']))
                    current = "{}. {}".format(station['count'], station['name'])
                except IndexError:
                    print("Invalid station number")
        except ValueError:
            print("Invalid station number")


def main():
    run()

if __name__ == '__main__':
    main()
