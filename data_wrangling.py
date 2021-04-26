"""CSC111 Project 2021: The Data Wrangling of the Project

Description
===========
This file is where the data wrangling of this project occurs. It contains a function
that reads from a csv file with a format matching the 'vancouver_subway.csv' file and
returns a Subway graph class representation of the subway system csv file given.

Copyright and Usage Information
===============================
This file is for the personal and private use of Katherine Luo, Alissa Lozhkin,
Ayanaa Rahman, and Jennifer Cao. Any forms of distribution of this code, with or
without changes to this code, are prohibited.

This file is Copyright (c) 2021 Katherine Luo, Alissa Lozhkin, Ayanaa Rahman,
and Jennifer Cao.
"""
import csv
import pygame
import subway_system


def read_csv_data(filepath: str, screen: pygame.Surface) -> subway_system.Subway:
    """Return a Subway graph class representing the subway system of the given filepath.

    screen is the pygame Surface the subway system will be later displayed on.

    Preconditions:
        - the csv file of the corresponding filepath matches the format of 'vancouver_subway.csv'
    """
    with open(filepath) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)

        # Initialize a subway system
        subway = subway_system.Subway(screen)

        for row in reader:
            # Determine the name, location, coordinates, and neighbours of the current station
            name = row[0]
            location = (float(row[1]), float(row[2]))
            coordinates = (int(row[3]), int(row[4]))
            neighbours = str.split(row[5], ',')

            # Add the current station to the subway system
            subway.add_station(name, location, coordinates)

            # Add edges between the current station and its neighbours
            for neighbour_name in neighbours:
                subway.add_edge(name, neighbour_name)

    return subway


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(
        config={
            # The names (strs) of imported modules
            'extra-imports': ['python_ta.contracts', 'csv', 'pygame', 'subway_system'],
            # The names (strs) of functions that call print/open/input
            'allowed-io': ['read_csv_data'],
            'max-line-length': 100,
            'disable': ['E1136']
        }
    )
