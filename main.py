"""CSC111 Project 2021: The Main File of the Project

Description
===========
This is the main file of the CSC111 project. This project runs a pygame visualization
of a subway system. As a specific example, this project will visualize the Vancouver
SkyTrain subway system in Canada and the Kobe subway system in Japan. The user can select two
stations and the stations they want to avoid. We will find the shortest path between those two
stations while avoiding the stations they don't want to visit. There is also a "Map View" option
available for the user to see a plotly map visualization of their selected stations and the
shortest path between them.

Copyright and Usage Information
===============================
This file is for the personal and private use of Katherine Luo, Alissa Lozhkin,
Ayanaa Rahman, and Jennifer Cao. Any forms of distribution of this code, with or
without changes to this code, are prohibited.

This file is Copyright (c) 2021 Katherine Luo, Alissa Lozhkin, Ayanaa Rahman,
and Jennifer Cao.
"""
import pygame
import data_wrangling
import pygame_visualization


SCREEN_SIZE = (1200, 700)  # (width, height)


if __name__ == '__main__':
    # Initialize the pygame screen, allowing for mouse click events
    screen = pygame_visualization.initialize_screen(SCREEN_SIZE, [pygame.MOUSEBUTTONDOWN],
                                                    'lightblue')

    # Create a Subway class of the Vancouver subway system
    # and run the pygame visualization of the Vancouver subway system
    vancouver_subway = data_wrangling.read_csv_data('data/vancouver_subway.csv', screen)
    pygame_visualization.run_visualization(screen, vancouver_subway,
                                           'images/vancouver_subway_system.png')

    # Create a Subway class of the Kobe subway system
    # and run the pygame visualization of the Kobe subway system
    # UNCOMMENT THE TWO LINES BELOW AND COMMENT OUT THE THREE UNCOMMENTED LINES ABOVE
    # kobe_subway = data_wrangling.read_csv_data('data/kobe_subway.csv', screen)
    # pygame_visualization.run_visualization(screen, kobe_subway, 'images/kobe_subway_system.png')
