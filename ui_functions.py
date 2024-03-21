import built_up_beam as bub
import csv
import plotly.graph_objects as go
import sectionproperties.pre.library.steel_sections as steel_geom
import streamlit as st

STREAMLIT_FUNCTION = st
PLOTLY_GRAPH_OBJECTS = go
SECTION_PROPS__STEEL_SECTIONS = steel_geom


def convert_csv_to_list (unseparated_list:list[list[str]]) -> list:
    ret_list = []
    for outer_list in unseparated_list:
        ret_list.append (f'{outer_list [0]} (Imp) / {outer_list [1]} (SI)')
    return ret_list


def csv_read (the_filename:str) -> list[list[str]]:
    '''
    Takes a filename 'the_filename' as a parameter and reads it from the current working directory.
    Returns a list of beams, where each beam's data is its own list of strings containing the actual data.

    Data in the text file is expected in this format:
        Beam name
        Length,E,Iz,[Iy,A,J,nu,rho]
        support_loc:support_type,support_loc:support_type, ...
        POINT:load_direction,load_magnitude,load_location,case:load_case
        DIST:load_direction,load_start_magnitude,load_end_magnitude,load_start_location,load_end_location,case:load_case
        ... # more loads
    '''
    return_LIST = [] # File data goes here
    with open(the_filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            return_LIST.append(line)
    return (return_LIST)


def fig_add_member (the_fig:PLOTLY_GRAPH_OBJECTS.Figure, the_section)->None:
    x_values = []
    y_values = []
    for point in the_section.points:
        x, y = point
        x_values.append (x)
        y_values.append (y)

    # close the figure by adding the first point again to the end
    x_values.append (x_values [0])
    y_values.append (y_values [0]) 

    the_fig.add_trace (PLOTLY_GRAPH_OBJECTS.Scatter
        (
            x=x_values, 
            y=y_values, 
            mode='lines+markers', 
            marker_color='Red',
            # name=the_title,
            # text="abc"
        )
    )


def fig_init (title:str = '', width:int = 500)->PLOTLY_GRAPH_OBJECTS.Figure:
    fig = PLOTLY_GRAPH_OBJECTS.Figure(
        layout_title_text=title,
        layout_title_x=0, # 0 = left justified, 1 = right, .5 is centre
        layout_width=width,
        layout_showlegend=False,
        # layout_xaxis_title="hi there",
        layout_xaxis_scaleanchor='y',
        layout_xaxis_scaleratio=1
    )
    return fig


def plot_member (the_section)->PLOTLY_GRAPH_OBJECTS.Figure:
    x_values = []
    y_values = []
    for point in the_section.points:
        x, y = point
        x_values.append (x)
        y_values.append (y)

    # close the figure by adding the first point again to the end
    x_values.append (x_values [0])
    y_values.append (y_values [0]) 

    fig = PLOTLY_GRAPH_OBJECTS.Figure(
        data=PLOTLY_GRAPH_OBJECTS.Scatter
        (
            x=x_values, 
            y=y_values, 
            mode='lines+markers', 
            marker_color='Red',
            # name=the_title,
            # text="abc"
        ),
        layout_title_text="Jamie's channel",
        layout_title_x=0, # 0 = left justified, 1 = right, .5 is centre
        layout_width=400,
        layout_showlegend=False,
        # layout_xaxis_title="hi there",
        layout_xaxis_scaleanchor='y',
        layout_xaxis_scaleratio=1
    )
    return fig

