"""CSC111 Project 2021: The Plotly Visualization of the Project

Description
===========
This file is where the plotly visualization of this project occurs. It contains a function
that plots a map in plotly displaying the shortest path between the two subway stations
the user selected in the pygame visualization (while avoiding the stations they don't want
to visit).

Copyright and Usage Information
===============================
This file is for the personal and private use of Katherine Luo, Alissa Lozhkin,
Ayanaa Rahman, and Jennifer Cao. Any forms of distribution of this code, with or
without changes to this code, are prohibited.

This file is Copyright (c) 2021 Katherine Luo, Alissa Lozhkin, Ayanaa Rahman,
and Jennifer Cao.
"""
import plotly.graph_objects as go


def plot_shortest_path(stations: list[str], locations: dict[str, tuple[float, float]]) -> None:
    """Plot the given stations on a map using plotly, linking them in the order that
    they are given.

    locations is a dictionary mapping the station name to the location (latitude, longitude)
    of that station.

    Preconditions:
        - len(stations) > 0
        - all(station_name in locations for station_name in stations)
    """
    fig = go.Figure(
        go.Scattermapbox(
            mode='markers+lines',
            text=stations,
            lat=[locations[station_name][0] for station_name in stations],
            lon=[locations[station_name][1] for station_name in stations],
            marker={'size': 10})
    )

    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lat': locations[stations[0]][0],
                       'lon': locations[stations[0]][1]},
            'style': 'open-street-map',
            'zoom': 12}
    )

    fig.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(
        config={
            # The names (strs) of imported modules
            'extra-imports': ['python_ta.contracts', 'plotly.graph_objects'],
            # The names (strs) of functions that call print/open/input
            'allowed-io': [],
            'max-line-length': 100,
            'disable': ['E1136']
        }
    )
