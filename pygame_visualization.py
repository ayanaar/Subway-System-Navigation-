"""CSC111 Project 2021: The Pygame Visualization of the Project

Description
===========
This file is where the pygame visualization of this project occurs. It contains a function
that run the pygame visualization and functions that help run the visualization. This file
contains adapted code from the University of Toronto, Department of Computer Science,
CSC111 Assignment 1, 2021:
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
import pygame_buttons
import pygame_mouse_click_handling
import subway_system


def initialize_screen(screen_size: tuple[int, int], allowed: list, colour: str) -> pygame.Surface:
    """Initialize pygame and return the screen (pygame Surface the pygame visualization
    will be displayed on).

    allowed is a list of pygame event types that should be listened for while pygame is running.
    colour is the colour of the background of the screen (pygame Surface) returned.

    Preconditions:
        - colour in THECOLORS
    """
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(THECOLORS[colour])
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT] + allowed)

    return screen


def run_visualization(screen: pygame.Surface, subway: subway_system.Subway,
                      subway_image_filename: str) -> None:
    """Run the subway system visualization with the given subway system
    on the given screen.

    subway_image_filename is the filepath for the image of the subway system.
    """
    # Initiate and load music and sound
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/background_music.mp3")  # From www.bensound.com
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)  # Loop music
    click_sound = pygame.mixer.Sound('sounds/click.mp3')  # Sound from www.zapsplat.com

    # Draw the background on the given screen and assign 'buttons' the return group
    # of Buttons for this visualization
    buttons = draw_background(screen, subway_image_filename)

    # Set up initial variables needed for this visualization
    clock = pygame.time.Clock()
    is_running = True
    selected_stations = []
    removed_stations = set()
    shortest_path = []

    while is_running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # X button was pressed, stop running pygame (quit)
                pygame.mixer.music.fadeout(700)  # Fadeout music
                is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Play a clicking sound
                click_sound.play()

                # User clicked the mouse, call handle_mouse_click
                shortest_path = pygame_mouse_click_handling.handle_mouse_click(
                    screen, subway, buttons, event,
                    selected_stations, removed_stations, shortest_path)

        # Display changes
        subway.draw_stations()
        buttons.draw_buttons()
        draw_button_text(screen)
        pygame.display.flip()

    pygame.display.quit()


def draw_background(screen: pygame.Surface, subway_image_filename: str) -> pygame_buttons.Buttons:
    """Draw the background with the given filename onto the given screen.

    Return a pygame_buttons.Buttons class containing all the buttons needed for
    this visualization.
    """
    # Load the image of the subway system
    subway_background = pygame.image.load(subway_image_filename)
    # Convert the image into the same pixel format as the screen
    subway_background = subway_background.convert_alpha()
    # Draw the background on the screen
    screen.blit(subway_background, (0, 0))

    # Draw the sidebar on the screen and assign 'buttons' the group of Buttons on the sidebar
    buttons = draw_sidebar(screen)

    width, height = screen.get_size()
    # Draw a vertical line between the subway system and the sidebar
    pygame.draw.line(screen, THECOLORS['black'], (width - 300, 0), (width - 300, height), 2)

    return buttons


def draw_sidebar(screen: pygame.Surface) -> pygame_buttons.Buttons:
    """Draw the sidebar for the subway system visualization on the given screen.

    Return a pygame_buttons.Buttons class containing all the buttons needed for
    this visualization.
    """
    width = screen.get_width()

    draw_text(screen, 'Welcome!', 30, 'black', (width - 220, 30))

    draw_text(screen, 'Left click the stations', 18, 'black', (width - 245, 100))
    draw_text(screen, 'to select your start', 18, 'black', (width - 233, 125))
    draw_text(screen, 'and end destination.', 18, 'black', (width - 240, 150))

    draw_text(screen, 'Right click the stations', 18, 'black', (width - 250, 210))
    draw_text(screen, 'you want to avoid.', 18, 'black', (width - 235, 235))

    # Create a Buttons class to store all the buttons: GO!, RESET, and MAP VIEW
    # Initial colour of the buttons are grey so the user cannot press them yet
    buttons = pygame_buttons.Buttons(screen)
    buttons.add_button('go', 'grey', (width - 150, 330))
    buttons.add_button('reset', 'grey', (width - 150, 430))
    buttons.add_button('map view', 'grey', (width - 150, 530))

    return buttons


def draw_button_text(screen: pygame.Surface) -> None:
    """Draw the text for the buttons on the given pygame screen.
    """
    width = screen.get_width()

    # Draw the text for the GO! button
    draw_text(screen, 'GO!', 30, 'black', (width - 178, 310))
    # Draw the text for the  RESET button
    draw_text(screen, 'RESET', 25, 'black', (width - 190, 413))
    # Draw the text for the MAP VIEW button
    draw_text(screen, 'MAP VIEW', 25, 'black', (width - 215, 514))


def draw_no_path_found_message(screen: pygame.Surface, should_draw: bool) -> None:
    """Draw the text 'Sorry, no path was found.' on the given pygame screen when no
    path can be found between two stations (i.e., when should_draw is True).

    Otherwise, if should_draw is False, draw a rectangle the colour of the screen
    to cover the message (if necessary).
    """
    if should_draw:
        width = screen.get_width()
        # Draw a message that says 'Sorry, no path was found.'
        draw_text(screen, 'Sorry, no path', 23, 'darkred', (width - 230, 600))
        draw_text(screen, 'was found.', 23, 'darkred', (width - 210, 630))
    else:
        width, height = screen.get_size()
        # Draw a rectangle that is the colour of the screen to cover
        # the 'Sorry, no path was found' message (if necessary)
        screen_colour = screen.get_at((width - 1, height - 1))
        pygame.draw.rect(screen, screen_colour, pygame.Rect(905, 590, width - 1, height - 1))


def draw_text(screen: pygame.Surface, text: str, font_size: int,
              colour: str, pos: tuple[int, int]) -> None:
    """Draw the given text to the pygame screen at the given position.

    font_size is the font size of the text.
    colour is the colour of the text.
    pos represents the *upper-left corner* of the text.

    Preconditions:
        - colour in THECOLORS
    """
    font = pygame.font.SysFont('verdana', font_size)
    text_surface = font.render(text, True, THECOLORS[colour])
    width, height = text_surface.get_size()
    screen.blit(text_surface, pygame.Rect(pos, (pos[0] + width, pos[1] + height)))


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
                              'pygame_buttons', 'pygame_mouse_click_handling', 'subway_system'],
            # The names (strs) of functions that call print/open/input
            'allowed-io': [],
            'max-line-length': 100,
            'disable': ['E1136'],
            'generated-members': ['pygame.*']
        }
    )
