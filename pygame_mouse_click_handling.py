"""CSC111 Project 2021: The Pygame Mouse Click Handling of the Project

Description
===========
This file is where the pygame mouse click event handling of this project occurs. It contains a
function that handles the mouse click events in the pygame visualization and helper functions
with their individual actions depending on what the user clicked. This file contains adapted code
from the University of Toronto, Department of Computer Science, CSC111 Assignment 1, 2021:
www.teach.cs.toronto.edu/~csc111h/winter/assignments/a1/handout/

Copyright and Usage Information
===============================
This file is for the personal and private use of Katherine Luo, Alissa Lozhkin,
Ayanaa Rahman, and Jennifer Cao. Any forms of distribution of this code, with or
without changes to this code, are prohibited.

This file is Copyright (c) 2021 Katherine Luo, Alissa Lozhkin, Ayanaa Rahman,
and Jennifer Cao.
"""
import pygame
from pygame.colordict import THECOLORS
import pygame_visualization
import pygame_buttons
import subway_system
import plotly_visualization


def handle_mouse_click(screen: pygame.Surface, subway: subway_system.Subway,
                       buttons: pygame_buttons.Buttons, event: pygame.event.Event,
                       selected_stations: list[str], removed_stations: set[str],
                       path: list[str]) -> list[str]:
    """Handle the given mouse click event.

    screen is the pygame Surface the subway system is displayed on.
    subway is a Subway class representing the subway system being visualized.
    buttons are the group of buttons being used in this visualization.
    selected_stations is the stations the user selected.
    removed_stations is the stations the user wants to avoid.
    path is the current "shortest path" between two stations (it is an empty list
    if no path has been created yet or no path was found). It is a list of stations names.

    selected_stations and removed_stations may be mutated.

    Preconditions:
        - event.type == pygame.MOUSEBUTTONDOWN
        - len(selected_stations) <= 2
    """
    shortest_path = path

    # Check if user left-clicked a station and act accordingly
    handle_left_click_station(subway, buttons, event, selected_stations, removed_stations)

    # Check if user right-clicked a station and act accordingly
    handle_right_click_station(screen, subway, buttons, event, selected_stations, removed_stations)

    # Check if RESET button should be enabled and act accordingly
    if selected_stations != [] or removed_stations != set():
        # User can now press the RESET button
        buttons.update_button('reset', 'blue')

    # Check if RESET button was pressed and act accordingly
    handle_click_reset(screen, subway, buttons, event,
                       selected_stations, removed_stations, shortest_path)

    # Check if GO! button was pressed and act accordingly
    shortest_path = handle_click_go(screen, subway, buttons, event,
                                    selected_stations, removed_stations, shortest_path)

    # Check if MAP VIEW button was pressed and act accordingly
    handle_click_map_view(subway, buttons, event, shortest_path)

    return shortest_path


def handle_left_click_station(subway: subway_system.Subway, buttons: pygame_buttons.Buttons,
                              event: pygame.event.Event, selected_stations: list[str],
                              removed_stations: set[str]) -> None:
    """Handle the given mouse click event, checking if the user left-clicked and selected a
    station.

    subway is a Subway class representing the subway system being visualized.
    buttons are the group of buttons being used in this visualization.
    selected_stations is the stations the user selected.
    removed_stations is the stations the user wants to avoid.

    selected_stations and removed_stations may be mutated.

    Preconditions:
        - event.type == pygame.MOUSEBUTTONDOWN
        - len(selected_stations) <= 2
    """
    station_name = None

    # Check if user left-clicked a station and hasn't selected two stations yet
    if event.button == 1 and len(selected_stations) < 2:
        # Update selected station to a yellow circle (if necessary)
        station_name = subway.update_all_stations('yellow', event.pos)

    if station_name is not None:
        # User selected a station, add it to the set of selected stations
        selected_stations.append(station_name)

        # If the station_name is in removed_stations, removed station_name from it
        if station_name in removed_stations:
            removed_stations.remove(station_name)

        # Check if GO! button should be enabled
        if len(selected_stations) == 2:
            # User can now press the GO! button
            buttons.update_button('go', 'blue')


def handle_right_click_station(screen: pygame.Surface, subway: subway_system.Subway,
                               buttons: pygame_buttons.Buttons, event: pygame.event.Event,
                               selected_stations: list[str], removed_stations: set[str]) -> None:
    """Handle the given mouse click event, checking if the user right-clicked and selected a
    station to avoid.

    screen is the pygame Surface the subway system is displayed on.
    subway is a Subway class representing the subway system being visualized.
    buttons are the group of buttons being used in this visualization.
    selected_stations is the stations the user selected.
    removed_stations is the stations the user wants to avoid.

    selected_stations and removed_stations may be mutated.

    Preconditions:
        - event.type == pygame.MOUSEBUTTONDOWN
        - len(selected_stations) <= 2
    """
    station_name = None

    # Note: can only add to removed stations when MAP VIEW button is grey
    # and 'Sorry, no path was found.' message is not displayed
    # (i.e., the point at (1113, 651) is not dark red)
    if event.button == 3 and buttons.get_button_colour('map view') == 'grey' and \
            screen.get_at((1113, 651)) != THECOLORS['darkred']:
        # Update removed station to a red circle (if necessary)
        station_name = subway.update_all_stations('red', event.pos)

    if station_name is not None:
        # User removed a station, add it to the set of removed stations
        removed_stations.add(station_name)

        # While the station_name is in selected_stations, removed station_name from it
        while station_name in selected_stations:
            selected_stations.remove(station_name)

        # Check if GO! button should be disabled
        if len(selected_stations) < 2:
            # User cannot press the GO! button
            buttons.update_button('go', 'grey')


def handle_click_reset(screen: pygame.Surface, subway: subway_system.Subway,
                       buttons: pygame_buttons.Buttons, event: pygame.event.Event,
                       selected_stations: list[str], removed_stations: set[str],
                       shortest_path: list[str]) -> None:
    """Handle the given mouse click event, checking if the user left-clicked and pressed the RESET
    button.

    screen is the pygame Surface the subway system is displayed on.
    subway is a Subway class representing the subway system being visualized.
    buttons are the group of buttons being used in this visualization.
    selected_stations is the stations the user selected.
    removed_stations is the stations the user wants to avoid.
    shortest_path is the shortest path between two stations (it is an empty list if no path has
    been created yet or no path was found). It is a list of stations names.

    selected_stations and removed_stations may be mutated.

    Preconditions:
        - event.type == pygame.MOUSEBUTTONDOWN
        - len(selected_stations) <= 2
    """
    # Check if user left-clicked, if the RESET button is allowed to be pressed
    # and if the user actually pressed the RESET button
    if event.button == 1 and buttons.get_button_colour('reset') == 'blue' and \
            buttons.was_pressed('reset', event.pos):
        # Reset all the buttons (change buttons back to grey)
        buttons.update_button('go', 'grey')
        buttons.update_button('reset', 'grey')
        buttons.update_button('map view', 'grey')

        # Change yellow- and red-coloured stations back to grey-coloured stations
        stations = set.union(set(shortest_path + selected_stations), removed_stations)
        for station_name in stations:
            subway.update_selected_station(station_name, 'grey')

        # Clear the selected and removed stations
        selected_stations.clear()
        removed_stations.clear()

        # Draw a rectangle that is the colour of the screen to cover
        # the 'Sorry, no path was found' message (if necessary)
        pygame_visualization.draw_no_path_found_message(screen, False)


def handle_click_go(screen: pygame.Surface, subway: subway_system.Subway,
                    buttons: pygame_buttons.Buttons, event: pygame.event.Event,
                    selected_stations: list[str], removed_stations: set[str],
                    path: list[str]) -> list[str]:
    """Handle the given mouse click event, checking if the user left-clicked and pressed the GO!
    button.

    Return a list of station names representing the shortest path from selected_stations[0] and
    selected_stations[1]. Return the given path passed in if the user did not press GO!.

    screen is the pygame Surface the subway system is displayed on.
    subway is a Subway class representing the subway system being visualized.
    buttons are the group of buttons being used in this visualization.
    selected_stations is the stations the user selected.
    removed_stations is the stations the user wants to avoid.
    path is the current "shortest path" between two stations (it is an empty list
    if no path has been created yet or no path was found). It is a list of stations names.

    Preconditions:
        - event.type == pygame.MOUSEBUTTONDOWN
        - len(selected_stations) <= 2
    """
    shortest_path = path

    # Check if user left-clicked, if the GO! button is allowed to be pressed
    # and if the user actually pressed the GO! button
    if event.button == 1 and buttons.get_button_colour('go') == 'blue' and \
            buttons.was_pressed('go', event.pos):
        shortest_path = subway.shortest_path(selected_stations[0],
                                             selected_stations[1],
                                             removed_stations)

        # User can no longer press the GO! and RESET button
        buttons.update_button('go', 'grey')
        buttons.update_button('reset', 'grey')
        buttons.draw_buttons()
        pygame_visualization.draw_button_text(screen)

        if shortest_path == []:
            # No path was found between the two stations, display message
            pygame_visualization.draw_no_path_found_message(screen, True)
        else:
            # Initiate and load sounds
            pygame.mixer.init()
            path_sound = pygame.mixer.Sound('sounds/path.mp3')          # From www.zapsplat.com
            complete_sound = pygame.mixer.Sound('sounds/complete.mp3')  # From www.zapsplat.com

            # Display the shortest path for the user
            for station_name in shortest_path:
                subway.update_selected_station(station_name, 'yellow')
                pygame.event.wait(350)  # Wait before drawing next station
                subway.draw_stations()
                path_sound.play()  # Play a sound when a station in the path is displayed
                pygame.display.flip()

            complete_sound.play()  # Play a sound when path is completed

            # User can now press the MAP VIEW button
            buttons.update_button('map view', 'blue')

        # User can now press the RESET button
        buttons.update_button('reset', 'blue')

    return shortest_path


def handle_click_map_view(subway: subway_system.Subway, buttons: pygame_buttons.Buttons,
                          event: pygame.event.Event, shortest_path: list[str]) -> None:
    """Handle the given mouse click event, checking if the user left-clicked and pressed the
     MAP VIEW button.

    subway is a Subway class representing the subway system being visualized.
    buttons are the group of buttons being used in this visualization.
    shortest_path is a list of station names that are the shortest path between the
    start and end station names in the list.

    Preconditions:
        - event.type == pygame.MOUSEBUTTONDOWN
    """
    # Check if user left-clicked, if the MAP VIEW button is allowed to be pressed
    # and if the user actually pressed the MAP VIEW button
    if event.button == 1 and buttons.get_button_colour('map view') == 'blue' and \
            buttons.was_pressed('map view', event.pos):
        # Get the locations of the stations in the shortest path
        locations = subway.get_locations(shortest_path)
        # Plot the shortest path on a map in plotly
        plotly_visualization.plot_shortest_path(shortest_path, locations)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(
        config={
            # The names (strs) of imported modules
            'extra-imports': ['python_ta.contracts', 'pygame', 'pygame.colordict',
                              'pygame_visualization', 'pygame_buttons', 'subway_system',
                              'plotly_visualization'],
            # The names (strs) of functions that call print/open/input
            'allowed-io': [],
            'max-line-length': 100,
            'disable': ['E1136'],
            'max-args': 7
        }
    )
