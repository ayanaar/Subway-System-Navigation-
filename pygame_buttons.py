"""CSC111 Project 2021: The Pygame Buttons of the Project

Description
===========
This file is where the classes for the buttons in the pygame visualization of the project are
found. It contains a private class representing a button in the pygame visualization and a
public class representing a group of buttons.

Copyright and Usage Information
===============================
This file is for the personal and private use of Katherine Luo, Alissa Lozhkin,
Ayanaa Rahman, and Jennifer Cao. Any forms of distribution of this code, with or
without changes to this code, are prohibited.

This file is Copyright (c) 2021 Katherine Luo, Alissa Lozhkin, Ayanaa Rahman,
and Jennifer Cao.
"""
import pygame


class _Button(pygame.sprite.Sprite):
    """A private sprite class representing a button in the pygame visualization of a
    subway system.

    Instance Attributes:
        - colour: The colour of the button.
        - image: The current image of the button (either a grey or blue button).
        - rect: The "rectangle" representation of the image of the button
                (mainly used to keep track of the button's coordinates in pygame).

    Representation Invariants:
        - self.colour in {'blue', 'grey'}
    """
    colour: str
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, colour: str, coordinates: tuple[int, int]) -> None:
        """Initialize the color of button (either blue or grey) as well as the image
        and "rectangle" representation of the button in pygame.

         Preconditions:
            - colour in {'blue', 'grey'}
            - coordinates[0] is the x-coordinate and coordinates[1] is the y-coordinate
        """
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        self.colour = colour

        # Initialize the image-representation of this button in pygame
        self.image = pygame.image.load(f'images/{self.colour}_button.png')
        # Convert the background into the same pixel format as the screen
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        # Place station in its correct location in pygame
        self.rect.center = coordinates

    def get_colour(self) -> str:
        """Return the current colour of this button.
        """
        return self.colour

    def update(self, colour: str) -> None:
        """Update the image-representation of button in pygame (change the colour of the button).

         Preconditions:
            - colour in {'blue', 'grey'}
        """
        self.colour = colour

        # Initiate the image-representation of this button in pygame
        self.image = pygame.image.load(f'images/{colour}_button.png')
        # Convert the background into the same pixel format as the screen
        self.image = self.image.convert_alpha()

    def was_pressed(self, mouse_position: tuple[int, int]) -> bool:
        """Return True if the user pressed this button (determined through the given mouse
        position) and False otherwise.
        """
        if self.rect.collidepoint(mouse_position):
            return True
        else:
            return False


class Buttons:
    """A class representing a group of buttons in pygame.
    """
    # Private Instance Attributes:
    #   - _screen:
    #       A pygame Surface that the buttons in this Buttons class will be displayed on.
    # 	- _buttons:
    # 		A dictionary of the buttons contained in this group of Buttons.
    # 		Maps the button's name to the corresponding _Button object.
    #   - _sprites:
    #       A pygame.sprite.Group whose purpose is to draw the buttons of
    #       this group of Buttons on the pygame screen.
    _screen: pygame.Surface
    _buttons: dict[str, _Button]
    _sprites: pygame.sprite.Group

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize an empty group of buttons.

        screen is the pygame Surface that the subway system will be displayed on.
        """
        self._screen = screen
        self._buttons = {}
        self._sprites = pygame.sprite.Group()

    def is_button_in_group(self, button_name: str) -> bool:
        """Return True if the given button name is in this group of Buttons
        and False otherwise.
        """
        return button_name in self._buttons

    def add_button(self, button_name: str, colour: str, coordinates: tuple[int, int]) -> None:
        """Add a button with the given button name, location, and its pygame coordinates.

        Preconditions:
            - self.is_button_in_group(button_name) is True
            - colour in {'blue', 'grey'}
            - coordinates[0] is the x-coordinate and coordinates[1] is the y-coordinate
        """
        button = _Button(colour, coordinates)
        self._buttons[button_name] = button
        self._sprites.add(button)

    def get_button_colour(self, button_name: str) -> str:
        """Return the colour of the button with the corresponding button name.

        Preconditions:
            - self.is_button_in_group(button_name) is True
        """
        return self._buttons[button_name].get_colour()

    def update_button(self, button_name: str, colour: str) -> None:
        """Update the image-representation of the button with the given name to
        the given colour.

        Preconditions:
            - self.is_button_in_group(button_name) is True
            - colour in {'blue', 'grey'}
        """
        self._buttons[button_name].update(colour)

    def draw_buttons(self) -> None:
        """Draw the buttons for the subway visualization onto the pygame screen.
        """
        self._sprites.draw(self._screen)

    def was_pressed(self, button_name: str, mouse_position: tuple[int, int]) -> bool:
        """Return True if the button with the given button name was pressed by
        the user and False otherwise.

        Preconditions:
            - self.is_button_in_group(button_name) is True
        """
        if self._buttons[button_name].was_pressed(mouse_position):
            return True
        else:
            return False


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
        }
    )
