"""CSC111 Project 2021: The Subway System Classes of the Project

Description
===========
This file is where the classes for the subway system are found. It contains a private class
representing a station of the subway system and a public class representing the subway system.
This file contains adapted code from the University of Toronto, Department of Computer Science,
David Liu's CSC111 Lecture 14 slides, 2021:
www.teach.cs.toronto.edu/~csc111h/winter/lectures/14-representing-graphs/david/14-slides.html#
/title-slide

Copyright and Usage Information
===============================
This file is for the personal and private use of Katherine Luo, Alissa Lozhkin,
Ayanaa Rahman, and Jennifer Cao. Any forms of distribution of this code, with or
without changes to this code, are prohibited.

This file is Copyright (c) 2021 Katherine Luo, Alissa Lozhkin, Ayanaa Rahman,
and Jennifer Cao.
"""
from __future__ import annotations
from typing import Optional
import pygame


class _Station(pygame.sprite.Sprite):
    """A private sprite class representing a station of the subway system.

    Instance Attributes:
        - name: The name of the station.
        - location: The latitude and longitude of the station.
        - neighbours: The station's neighbouring stations.
        - image: The current image of the station (either a grey, yellow, or red circle).
        - rect: The "rectangle" representation of the image of the station
                (mainly used to keep track of the station's coordinates in pygame).

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.location[0] is the latitude and self.location[1] is the longitude
    """
    name: str
    location: tuple[float, float]
    neighbours: set[_Station]
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, name: str, location: tuple[float, float],
                 coordinates: tuple[int, int]) -> None:
        """Initiate the name, location, and neighbours of a station.
        Also initiate the image and "rectangle" representation of the station in pygame with
        the given coordinates of the station.

        Preconditions:
            - location[0] is the latitude and location[1] is the longitude
            - coordinates[0] is the x-coordinate and coordinates[1] is the y-coordinate
        """
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Initiate the general information about this station
        self.name = name
        self.location = location
        self.neighbours = set()

        # Initiate the image and "rectangle" representation of this station in pygame
        # (station is initially a grey circle)
        self.image = pygame.image.load('images/grey_circle.png')
        # Convert the background into the same pixel format as the screen
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        # Place station in its correct location in pygame
        self.rect.center = coordinates

    def update(self, colour: str, mouse_position: Optional[tuple[int, int]] = None) \
            -> Optional[str]:
        """Update the image-representation of the station in pygame
        to the circle of given colour (if necessary).

        Return None if the user did not select this station.
        Return the name of this station if the user did select this station.

        If the mouse_position is None, it means one of two things:
            1. We are displaying the shortest path instead of determining if the user
               selected this station. In this case, the station is always updated.
            2. We are resetting the colour of the station to grey.

        Preconditions:
            - colour in {'grey', 'yellow', 'red'}
        """
        # Check if user selected this station or if we need to update for reasons (1) and (2)
        # mentioned in the docstring
        if mouse_position is None or self.rect.collidepoint(mouse_position):
            # Change the colour of the station to grey, yellow, or red
            # (depending on the value of colour)
            self.image = pygame.image.load(f'images/{colour}_circle.png')
            # Convert the background into the same pixel format as the screen
            self.image = self.image.convert_alpha()

            # Return the name of the station
            return self.name

        # User did not select this station, return None
        return None

    def possible_paths(self, target_station: str, visited: set[str]) -> list[list[str]]:
        """Return all paths between this station and the target station without using
        any stations in visited.

        Preconditions:
            - self.name not in visited
            - target_station not in visited
        """
        if self.name == target_station:
            return [[self.name]]
        else:
            # Create a new set of visited stations with this station's name included
            new_visited = visited.union({self.name})
            # Accumulator: keep track of the possible paths so far
            paths_so_far = []

            for station in self.neighbours:
                if station.name not in new_visited:
                    # Find the paths between this station and the target station,
                    # avoiding the stations in new_visited
                    paths = station.possible_paths(target_station, new_visited)

                    # Append the paths to paths_so_far
                    for path in paths:
                        paths_so_far.append([self.name] + path)

            return paths_so_far


class Subway:
    """A graph representation of a subway system with stations.
    """
    # Private Instance Attributes:
    #   - _screen:
    #       A pygame Surface that stations in this Subway class will be displayed on.
    # 	- _stations:
    # 		A dictionary of the stations contained in this subway system.
    # 		Maps the station's name to the corresponding _Station object.
    #   - _sprites:
    #       A pygame.sprite.Group whose purpose is to draw the stations of
    #       this subway system on _screen.
    _screen: pygame.Surface
    _stations: dict[str, _Station]
    _sprites: pygame.sprite.Group

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize an empty subway system (no stations or edges).

        screen is the pygame Surface that the subway system will be displayed on.
        """
        self._screen = screen
        self._stations = {}
        self._sprites = pygame.sprite.Group()

    def is_station_in_subway(self, station_name: str) -> bool:
        """Return True if the given station name is in this subway system
        and False otherwise.
        """
        return station_name in self._stations

    def add_station(self, name: str, location: tuple[float, float],
                    coordinates: tuple[int, int]) -> None:
        """Add a station with the given station name, location, and pygame coordinates to this
        subway system.

        Do nothing if the given station name is already in this subway system.

        Preconditions:
            - location[0] is the latitude and location[1] is the longitude
            - coordinates[0] is the x-coordinate and coordinates[1] is the y-coordinate
        """
        if not self.is_station_in_subway(name):
            station = _Station(name, location, coordinates)
            self._stations[name] = station
            self._sprites.add(station)

    def add_edge(self, name1: str, name2: str) -> None:
        """Add an edge between the two stations with the given station names in this subway system.

        Do nothing if the given station name1 and name2 are not in this subway system.

        Preconditions:
            - name1 != name2
        """
        if self.is_station_in_subway(name1) and self.is_station_in_subway(name2):
            station1 = self._stations[name1]
            station2 = self._stations[name2]

            station1.neighbours.add(station2)
            station2.neighbours.add(station1)

    def get_locations(self, stations: list[str]) -> dict[str, tuple[float, float]]:
        """Return a dictionary of the given stations mapping to their locations
        represented as a tuple (latitude, longitude).

        Preconditions:
            - all(self.is_station_in_subway(station) for station in stations)
        """
        station_locations = {}

        for station_name in stations:
            station_locations[station_name] = self._stations[station_name].location

        return station_locations

    def update_all_stations(self, colour: str, mouse_position: tuple[int, int]) -> Optional[str]:
        """Update the image-representation of the stations in pygame to the given
         colour (if necessary).

         Preconditions:
            - colour in {'grey', 'yellow', 'red'}
        """
        for name in self._stations:
            # Update the station's image-representation in pygame (if necessary)
            station_name = self._stations[name].update(colour, mouse_position)

            if station_name is not None:
                # User selected this station, return the station's name
                return station_name

        # User did not select any station, return None
        return None

    def update_selected_station(self, name: str, colour: str) -> None:
        """Update the image-representation of the station with the given station name
        in pygame to the given colour.

        Do nothing if the given station name is not in this subway system.

        Precondition:
            - colour in {'grey', 'yellow', 'red'}
        """
        if self.is_station_in_subway(name):
            station = self._stations[name]
            station.update(colour)

    def draw_stations(self) -> None:
        """Draw the stations of this subway system onto the pygame screen.
        """
        self._sprites.draw(self._screen)

    def shortest_path(self, name1: str, name2: str, visited: set[str]) -> list[str]:
        """Return the shortest path between the two stations with the given names
        without visiting any of the stations in visited.

        Preconditions:
            - name1 not in visited and name2 not in visited
            - self.is_station_in_subway(name1) and self.is_station_in_subway(name2)
            - all(self.is_station_in_subway(name) for name in visited)
        """
        possible_paths = self._stations[name1].possible_paths(name2, visited)

        if possible_paths == []:
            # No path was found between the two stations, return []
            return []
        else:
            # Assign shortest_path the last path in possible_paths for now
            # and reassign later if another path is shorter
            shortest_path = possible_paths.pop()

            # Find the shortest path out of all possible paths
            for path in possible_paths:
                if len(path) < len(shortest_path):
                    shortest_path = path

            return shortest_path


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(
        config={
            # The names (strs) of imported modules
            'extra-imports': ['python_ta.contracts', 'pygame'],
            # The names (strs) of functions that call print/open/input
            'allowed-io': [],
            'max-line-length': 100,
            'disable': ['E1136'],
            'max-nested-blocks': 4
        }
    )
