# Subway-System-Navigation-

**Introduction**

Subway systems are a very important mode of transportation. Subway systems provide many benefits, they are environmentally friendly, convenient, safer than other forms of transportation (e.g, cars) and cost effective (Silverwitz). People use the subway for one reason, and that is to get to another place. And the majority of people want to get to their final destination in the fastest time possible. People can achieve this by planning. There is a clear relationship between the population size of a city and the complexity of the city’s subway (Florida). Areas with larger populations tend to have a greater number of subway stations (Florida). And as the subway becomes more and more complex, the harder it is for a subway user to plan their subway journey quickly. With our project, people will be able to plan their subway trips with ease and efficiency. We will be doing this by examining two different subway systems. These subway systems will serve as a model for our reference when solving this problem, but our project is applicable to any other subway system. 
  
Finding the shortest path between subway stations is crucial to the overall experience of a subway user. Moreover, the complexity of large subway systems makes it difficult for the subway user to look at the system map and figure out the fastest route, especially if they want to avoid a station.  Our project aims to provide subway users with the most efficient routes. 
  
We chose to apply our project to the Vancouver SkyTrain subway system in British Columbia, Canada. We chose this system specifically because it is complicated enough to demonstrate our knowledge of graphs. Because there are many stations in the Vancouver SkyTrain subway system, we know it might be difficult for a user to plan their subway journey. By creating this project, we want to make the planning of a subway journey easier and more efficient. We also applied our project to the Kobe Subway system in Japan, solely to demonstrate how our project can be applicable to any subway system when given the appropriate dataset. 
  
Our research question is: **How can we simplify the subway trip planning process of a subway user?** We implemented our project with this question in mind, focusing primarily on finding the shortest path between two subway stations and providing the user with the option to avoid stations. To determine this shortest path, our project will take into account the number of stations travelled to get from one station to another.  
   
**Datasets**
  
The first dataset we used is from GitHub. The dataset was created by Dmitry Shkolnik and is a csv file called “skytrainstations.csv”. This dataset includes information about the SkyTrain subway system in Vancouver, BC, Canada. Information in this dataset includes the stop id, station stop names, the longitude and latitude of the stations, zone ids and the location (Shkolnik). Within this dataset, we only used the station names, latitudes and longitudes of the stations for this project. We altered this dataset by deleting every duplicate row that contained the same station name twice. We added columns for the x- and y-coordinates of where the stations are located in the pygame window as well as the neighbours of each station. We called this file ``vancouver_subway.csv”. Within this file, the neighbours are separated using a comma (no space in between).  
  
The second dataset is a csv file we created and called ``kobe_subway.csv”. We manually found the required data for this file, as we could not find it elsewhere. This dataset includes columns for the station names, the latitude and longitude of the stations, the x- and y- coordinates of where the stations are located in the pygame window, and the neighbours of each station.  We used Google Maps to find the longitude and latitude of each station (Google). 

**Computational Overview**

The ability to understand and visualize graphs was an integral part of our project. In our project, a graph represents a subway system (ex. the Vancouver SkyTrain subway system or the Kobe subway). The classes for the subway system are stored in the file ``subway_system.py”. Each vertex of the graph represents a subway station and each edge connects two neighbouring stations together. We created a private _Station class that stores the private instance attributes for the station. The ``major” attributes are the name (represented as a string), latitude and longitude location (represented as a tuple, storing coordinate points), and its neighbouring stations (represented as a set of strings). We also made a public graph class Subway that has private instance attributes to keep track of the stations in this metro system, mapping the station’s name to its corresponding _Station vertex.   
  
In the same ``subway_system.py” file, we created a method called shortest_path in the graph class Subway that determines the shortest path between station A and station B. It calls a method in the _Station class called possible_paths that determines all the possible paths from station A to station B using the graph traversal pattern taught in lecture (Liu). The shortest path was evaluated based on the least number of stations visited in the path. We also made sure not to visit any stations that a subway user wanted to avoid. If no path was found between station A and station B, an empty list is returned. 
  
The ``subway_system.py” file also has a method in the Subway class called update_all_stations, which loops through all the stations, finding the station the user selected (mouse_position) and changing the station to its correct colour (yellow if it’s a station they want and red if it’s a station they want to avoid). The method update_selected_station does the same thing except for only one station and takes in a name parameter for the name of the station rather than the user’s mouse position. These methods call the update method in the _Station class that uses the pygame.Rect method .collidepoint to determine whether a station has ``collided” with the user’s mouse. In addition, there is also the draw_stations method that makes use of pygame.sprite. The _Station objects inherit from the pygame.sprite.Sprite class so that we can use the pygame.sprite.Group method .draw in the Subway class to draw the stations onto the pygame screen (Pygame). Note that a Subway class is created using the read_csv_data function found in the ``data_wrangling.py”. \\  
  
For visualization, we used the python library pygame and plotly. The file ``plotly_visualization.py” contains the function ``plot_shortest_path” that plots the shortest path between two station on a real world map using latitude and longitude locations of each station (Plotly). The pygame visualization is found in the file ``pygame_visualization”. The most ``important” function used in this file is the run_visualization function that calls helper functions in the same file (these functions draw on the pygame screen), and calls functions in the ``pygame_mouse_click_handling.py” file (but more on this file later). The original map was the canvas we operated on. Drawing the background involved drawing the sidebar and uploading the image of the subway system map using the pygame.image.load function (Pygame). Running the visualization brought all the pieces together, drawing all the buttons that are available to the user’s disposal (``GO!”, ``RESET”, and ``MAP VIEW” buttons), drawing all stations on the map, and drawing all required texts. A `Sorry, no path was found.’ text is drawn on the sidebar of the visualization when no path can be found between two subway stations. The local variables selected_stations (a list of length at most 2) and removed_stations (a set) keep track of the stations the user wants and the stations the user wants to avoid, respectively. This file uses adapted code from CSC111 Assignment 1 (CSC111 Department). \\  
  
In order for the user to click on subway stations, buttons needed to be incorporated into our project. Buttons were represented in a similar way as stations were and are found in the ``pygame_buttons.py” file. A private class _Button was created as a child of the pygame.sprite.Sprite class. A public class, Buttons, was created to keep track of all the buttons used in the pygame visualization. Each button has private instance attributes, including colour (represented as a string), image (represented as a pygame.Surface object), and pygame.Rect object, which represents the rectangular area that the button is enclosed in (Pygame). The public Buttons class contains a method called draw_buttons that draws the buttons onto the pygame screen using the .draw method of pygame.sprite.Group. There is also a method in the private _Button class called was_pressed that calls the pygame.Rect method .collidepoint to determine if the user pressed that button (Pygame). \\  
  
The ``pygame_mouse_click_handling.py” file contained functions that handle all mouse click events (i.e., when \texttt{event.type == pygame.MOUSEBUTTONDOWN}). The most ``important” function in this file is the handle_mouse_click} function, which calls helper functions to handle specific events depending on what/where the user pressed. The handle_left_click_station helper function checks whether the user left-clicked a station and ``lights up” that station, turning it from a grey colour to a yellow colour. This function will add the station to the local variable selected_stations of the ``pygame_visualization.py” file and remove it from the removed_stations if the station is in this set. It will also enable the ``GO!” button, turning it from a grey to a blue colour if the user has selected two stations they want to go to.  The handle_right_click_station helper function checks whether the user right-clicked a station and ``lights up” that station, turning it from a grey colour to a red colour. This function will add the station to removed_stations and remove all instances of it from the selected_stations if the station is in this list (once or twice). Note that this can happen because we allow the user to start and end at the same station. The function will also disable the ``GO!” button, turning it from a blue to a grey colour if the user has no longer selected two stations they want to go to. \\  
  
In the same ``pygame_mouse_click_handling.py” file, the handle_click_reset} function resets the pygame visualization if the user pressed ``RESET”, disabling all buttons (turning them grey), deselecting all the stations (turning them grey as well), and clearing selected_stations and removed_stations, and drawing a rectangle over the `Sorry, no path was found.’ message, if necessary. The handle_click_go determines the shortest path between two stations if the user pressed ``GO!”. It displays this path on the pygame screen and may enable the ``MAP VIEW” button if a path is found between the two stations. Finally, handle_click_map_view runs the plotly visualization of the shortest path when the user presses the ``MAP VIEW” button. Note that all these helper functions call the necessary ``update”- related methods of the Subway class and Buttons class to change the colour of the stations or buttons. The ``draw” methods of these classes are called to display these changes. The images for the stations and the buttons come from Game Art 2D (Game Art 2D).  

