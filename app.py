import streamlit as st
import sectionproperties.pre.library.steel_sections as steel_geom
import plotly.graph_objects as go
import built_up_beam as bub
import ui_functions as ui
import pandas as pd


STREAMLIT_FUNCTION = st
PLOTLY_GRAPH_OBJECTS = go
SECTION_PROPS__STEEL_SECTIONS = steel_geom
NONE_CHOSEN = '[none]'

STREAMLIT_FUNCTION.session_state ['form_phase'] = 'start'

comment='''
next:
    use the y_values an orientation to change the plots
    verify I'm using the correct orientation options for angles
'''

def calculate()->None:

    # STREAMLIT_FUNCTION.write (f"Y value is {ui_text_y_hss}")
    # STREAMLIT_FUNCTION.write (f"mPa is {ui_radio_Fy}")
    # STREAMLIT_FUNCTION.write ("or, mPa is" + eval ('ui_radio' + '_Fy'))
    if (ui_selectbox_sections_i == NONE_CHOSEN 
            and ui_selectbox_sections_channel == NONE_CHOSEN 
            and ui_selectbox_sections_hss == NONE_CHOSEN 
            and ui_selectbox_sections_angle == NONE_CHOSEN):
        STREAMLIT_FUNCTION.write ("NO MEMBERS SELECTED!")
        return None
        
    sections_to_plot = []
    if ui_selectbox_sections_i != NONE_CHOSEN:
        sections_to_plot.append (process_input_data ('i'))

    if ui_selectbox_sections_channel != NONE_CHOSEN:
        sections_to_plot.append (process_input_data ('channel'))

    if ui_selectbox_sections_hss != NONE_CHOSEN:
        sections_to_plot.append (process_input_data ('hss'))

    if ui_selectbox_sections_angle != NONE_CHOSEN:
        sections_to_plot.append (process_input_data ('angle'))
    
    plot_sections (sections_to_plot)
    # plot_sections ()

   
def load_and_format_data ()->pd:
    #section_data_angle = pd.read_excel ("JH-UNPROTECTED-SST92.xlsx", sheet_name='L', header=0).drop (index=[0,1])


    # I sections
    section_data_i = pd.read_excel ("JH-UNPROTECTED-SST92.xlsx", sheet_name='W', header=0).drop (index=[0,1])
    section_data_i ['Formatted name'] = section_data_i["Ds_i"] + ' / ' + section_data_i["Dsg"]
    # section_data_i.loc[len(section_data_i)] = pd.Series(dtype='str')
    section_data_i.at [2, 'Formatted name'] = NONE_CHOSEN # NO IDEA WHY THIS NEEDS TO BE AT INDEX 2, *AFTER* I have already dropped two rows!
    section_data_i = section_data_i.set_index ('Dsg')
    # STREAMLIT_FUNCTION.write ("len is " + str(len (section_data_i["Ds_i"])))

    # channels
    section_data_channel = pd.read_excel ("JH-UNPROTECTED-SST92.xlsx", sheet_name='C', header=0).drop (index=[0,1])
    section_data_channel ['Formatted name'] = section_data_channel["Ds_i"] + ' / ' + section_data_channel["Dsg"]
    section_data_channel.at [2, 'Formatted name'] = NONE_CHOSEN
    section_data_channel = section_data_channel.set_index ('Dsg')

    # HSS
    section_data_hss = pd.read_excel ("JH-UNPROTECTED-SST92.xlsx", sheet_name='HSS-G40', header=0).drop (index=[0,1,2]) # HSS sheet contains one extra header row!
    section_data_hss ['Formatted name'] = section_data_hss["Ds_i"] + ' / ' + section_data_hss["Dsg"]
    section_data_hss.at [3, 'Formatted name'] = NONE_CHOSEN
    section_data_hss = section_data_hss.set_index ('Dsg')

    # angles
    section_data_angle = pd.read_excel ("JH-UNPROTECTED-SST92.xlsx", sheet_name='L', header=0).drop (index=[0,1])
    section_data_angle ['Formatted name'] = section_data_angle["Ds_i"] + ' / ' + section_data_angle["Dsg"]
    section_data_angle.at [2, 'Formatted name'] = NONE_CHOSEN
    section_data_angle = section_data_angle.set_index ('Dsg')

    return section_data_i, section_data_channel, section_data_hss, section_data_angle


def plot_sections (sections_to_plot:list[dict])->None:
# def plot_sections ()->None:
    figures_to_plot = []
    num_nodes_for_radii = 12
    k = 23

    largest_width:float = 0.0 # since we're not concerned with x-axis values, for presentation purposes we'll try to centre everything about the y-axis
    for section in sections_to_plot:
        largest_width = max (largest_width, section ['section data'] ['B'])

    for section in sections_to_plot:
        this_section_type = section ['section type']
        this_section_data = section ['section data']
        this_y = section ['y']
        this_orientation = section ['orientation']

        this_width = this_section_data ['B']

        try:
            t_w=this_section_data ['W']
        except:
            t_w=this_section_data ['T'] # for angles, there is no 'thickness of web'; in this case, t_f will be ignored by bub.plot_section()

        try:
            r_out=this_section_data ['RO'] # only for HSS
        except:
            r_out=1
        geometry_shape = bub.plot_section(
            f"steel_{ui_radio_Fy}",
            this_section_type,
            d=this_section_data ['D'],
            b=this_width,
            t_f=this_section_data ['T'],
            t_w=t_w,
            r_out=r_out,
            n_r=num_nodes_for_radii,
            k=k,
            )
        

        
        num_figures_so_far = len(figures_to_plot)
        if this_section_type == 'hss':
            if this_orientation [0:4] != 'Vert':
                geometry_shape = geometry_shape.rotate_section (angle=90, rot_point = (0,0)).shift_section ()
        if num_figures_so_far > 0:
            # STREAMLIT_FUNCTION.write (f"{num_figures_so_far=}")
            geometry_shape = geometry_shape.align_center(align_to=figures_to_plot [num_figures_so_far - 1])


        # now centre the object
        # if this_width < largest_width:
        #     geometry_shape = geometry_shape.shift_section (x_offset=(largest_width - this_width)/2)
        
        # don't append anything until we've rotated/shifted/flipped the geometry, and then only append the transformed geometry


        # shift it by the specified Y-value
        if this_section_type != 'i':
            geometry_shape = geometry_shape.shift_section (y_offset=this_y)


        # if this_section_type == 'channel':
        #     geometry_shape = geometry_shape.shift_section (y_offset=this_y)

        # now centre each shape about the y-axis
        # for geometry in geometry_shape:
        #     STREAMLIT_FUNCTION.write (geometry)
        figures_to_plot.append (geometry_shape)


    # mirrored_angle = (
    #     temp_angle_geometry
    #     .mirror_section(axis='x')
    #     .align_to(temp_channel_geometry, on="top", inner=True)
    #     .align_to(temp_channel_geometry, on="right")
    #     .shift_section(y_offset=-63.5)
            
    # )

    fig = ui.fig_init("", 400)
    for figure in figures_to_plot:
        ui.fig_add_member (fig, figure)

    # st.write (fig.layout.title.text)
    STREAMLIT_FUNCTION.plotly_chart(fig)


def process_input_data (section_type:str = 'i')->dict:
    the_selectbox = eval (f'ui_selectbox_sections_{section_type}')
    the_section_data = eval (f'section_data_{section_type}')

    # need to try/except this in case this selectbox has been reset to NONE_CHOSEN
    try:
        chosen_index = the_selectbox.split(' ')[2]
        chosen_row = the_section_data.loc [chosen_index]
        
        # set default values for the I section (which will be ignored)
        y_value = 0
        orientation = 'Vertical' 
        if section_type != 'i':
            y_value = eval (f'ui_text_y_{section_type}')
            orientation = eval (f'ui_radio_orientation_{section_type}')
        # ui_text_y_channel = STREAMLIT_FUNCTION.text_input ("Y-value (mm)", value="0", key='y_channel')
        # ui_radio_orientation_channel = STREAMLIT_FUNCTION.radio ("Orientation of strong axis", ("Vertical", "Horizontal"), key='o_channel')
        return ({
            'section type' : section_type, 
            'section data' : chosen_row,
            'y' : y_value,
            'orientation' : orientation})
    except:
        return ({'section data' : {'D': 0}})


def set_session_state_for_details (which_details:str = 'i')->None:
    if f'details_{which_details}' not in STREAMLIT_FUNCTION.session_state:
        # STREAMLIT_FUNCTION.write ("details_i hasn't been defined yet!")
        STREAMLIT_FUNCTION.session_state [f'details_{which_details}'] = '(nothing selected)'
    else:
        actual_height = process_input_data (which_details) ['section data'] ['D']
        if actual_height > 0:
            STREAMLIT_FUNCTION.session_state [f'details_{which_details}'] = f"actual height (d) is {actual_height}mm"
        else:
            STREAMLIT_FUNCTION.session_state [f'details_{which_details}'] = '(nothing selected)'
    eval (f'details_{which_details}').text (STREAMLIT_FUNCTION.session_state [f'details_{which_details}'])
    return



def create_input_ui_for_member (member_type:str)->None:
    # I sections
    # STREAMLIT_FUNCTION.markdown ("# :blue[W-Section]")
    # ui_selectbox_sections_i = STREAMLIT_FUNCTION.selectbox ('', section_data_i["Formatted name"])
    # details_i = STREAMLIT_FUNCTION.empty ()
    # STREAMLIT_FUNCTION.markdown ("---") 
    for ui_element in ui_elements_current:
        ui_element.empty()
    pass

def get_member_code_from_string (s:str)->str:
    '''
    Converts 'W section' to 'i', and 'HSS' to 'hss', etc. for ease of use in later functions
    '''
    s = s.lower()
    if s [0:1] == 'w':
        return 'i'
    else:
        return s
    
def submit_members ()->None:
    chosen_member_types= []
    for idx in range (1,2):#6):
        if eval (f'ui_selectbox_members_{idx}') != NONE_CHOSEN:
            STREAMLIT_FUNCTION.write ("SELECTED " + eval (f'ui_selectbox_members_{idx}') + ' or ' + get_member_code_from_string (eval (f'ui_selectbox_members_{idx}')))
            chosen_member_types.append (get_member_code_from_string (eval (f'ui_selectbox_members_{idx}')))
    if len (chosen_member_types) == 0:
        STREAMLIT_FUNCTION.write ("NO MEMBERS SELECTED!")
    else:
        for member_type in chosen_member_types:
            create_input_ui_for_member (member_type)
    # STREAMLIT_FUNCTION.write ()
    with STREAMLIT_FUNCTION.sidebar:
        STREAMLIT_FUNCTION.session_state ['form_phase'] = 'just_submitted_members'
        STREAMLIT_FUNCTION.write ('form_phase is NOW ' + STREAMLIT_FUNCTION.session_state ['form_phase'])


# LOAD THE BEAM DATA FROM EXCEL
section_data_i, section_data_channel, section_data_hss, section_data_angle = load_and_format_data ()


STREAMLIT_FUNCTION.markdown ("# BUILT-UP-BEAM")


possible_members_list = ['[none]', 'W section', 'channel', 'hss', 'angle']
ui_elements_current = [] # so we'll know what to clear ('empty') when changing the UI
STREAMLIT_FUNCTION.write ('form_phase is ' + STREAMLIT_FUNCTION.session_state ['form_phase'])
with STREAMLIT_FUNCTION.sidebar:
    if STREAMLIT_FUNCTION.session_state ['form_phase'] == 'just_submitted_members':
        STREAMLIT_FUNCTION.write ("now we'll ask you to spec")
    else:
        with STREAMLIT_FUNCTION.form ('choose_members'):
            STREAMLIT_FUNCTION.markdown (("##### Select up to 5 members that will comprise the built-up beam. Start with 1 (the top-most member) and work your way lower for as many members as required. Anything with [none] will be ignored."))
            STREAMLIT_FUNCTION.markdown ("---")
            STREAMLIT_FUNCTION.markdown ("# :blue[1) top-most]")
            ui_selectbox_members_1 = STREAMLIT_FUNCTION.selectbox ('', possible_members_list, key=1)
            submitted_members = STREAMLIT_FUNCTION.form_submit_button ("Continue!")
            if submitted_members:
                submit_members()
        # STREAMLIT_FUNCTION.markdown ("---")
        # STREAMLIT_FUNCTION.markdown ("# :blue[2) 2nd from top]")
        # ui_selectbox_members_2 = STREAMLIT_FUNCTION.selectbox ('', possible_members_list, key=2)
        # STREAMLIT_FUNCTION.markdown ("---")
        # STREAMLIT_FUNCTION.markdown ("# :blue[3) 3rd from top]")
        # ui_selectbox_members_3 = STREAMLIT_FUNCTION.selectbox ('', possible_members_list, key=3)
        # STREAMLIT_FUNCTION.markdown ("---")
        # STREAMLIT_FUNCTION.markdown ("# :blue[4) 4th from top]")
        # ui_selectbox_members_4= STREAMLIT_FUNCTION.selectbox ('', possible_members_list, key=4)
        # STREAMLIT_FUNCTION.markdown ("---")
        # STREAMLIT_FUNCTION.markdown ("# :blue[5) 5th from top]")
        # ui_selectbox_members_5 = STREAMLIT_FUNCTION.selectbox ('', possible_members_list, key=5)

        # ui_button = STREAMLIT_FUNCTION.button('Continue', on_click=submit_members)


comment= '''
# POPULATE THE SIDEBAR UI
with STREAMLIT_FUNCTION.sidebar:
    STREAMLIT_FUNCTION.markdown ("##### Note: this tool is only concerned with the strong-axis, and ignores an object's x-position, i.e. relative to the y-axis.")
    STREAMLIT_FUNCTION.markdown ("---")
    ui_radio_Fy = STREAMLIT_FUNCTION.radio ("Steel strength (mPa)", ("300", "350"))
    STREAMLIT_FUNCTION.markdown ("---")

    # I sections
    STREAMLIT_FUNCTION.markdown ("# :blue[W-Section]")
    ui_selectbox_sections_i = STREAMLIT_FUNCTION.selectbox ('', section_data_i["Formatted name"])
    details_i = STREAMLIT_FUNCTION.empty ()
    STREAMLIT_FUNCTION.markdown ("---")

    # channel sections
    STREAMLIT_FUNCTION.markdown ("# :blue[Channel Section]")
    ui_selectbox_sections_channel = STREAMLIT_FUNCTION.selectbox ('', section_data_channel["Formatted name"])
    details_channel = STREAMLIT_FUNCTION.empty ()
    ui_text_y_channel = STREAMLIT_FUNCTION.text_input ("Y-value (mm)", value="0", key='y_channel')
    ui_radio_orientation_channel = STREAMLIT_FUNCTION.radio ("Orientation of strong axis", ("Vertical", "Horizontal (opens down) ┏┓", "Horizontal (opens up) ┗┛"), key='o_channel')
    STREAMLIT_FUNCTION.markdown ("---")

    # HSS sections
    STREAMLIT_FUNCTION.markdown ("# :blue[HSS Section (rectangular)]")#, ] :red[rectangular]")
    ui_selectbox_sections_hss = STREAMLIT_FUNCTION.selectbox ('', section_data_hss["Formatted name"])
    details_hss = STREAMLIT_FUNCTION.empty ()
    ui_text_y_hss = STREAMLIT_FUNCTION.text_input ("Y-value (mm)", value="0", key='y_hss')
    ui_radio_orientation_hss = STREAMLIT_FUNCTION.radio ("Orientation of strong axis", ("Vertical │", "Horizontal ──"), key='o_hss')
    STREAMLIT_FUNCTION.markdown ("---")

    # Angle sections
    STREAMLIT_FUNCTION.markdown ("# :blue[Angle Section]")
    ui_selectbox_sections_angle = STREAMLIT_FUNCTION.selectbox ('', section_data_angle["Formatted name"])
    details_angle = STREAMLIT_FUNCTION.empty ()
    ui_text_y_angle = STREAMLIT_FUNCTION.text_input ("Y-value (mm) ", value="0", key='y_angle')
    ui_radio_orientation_angle = STREAMLIT_FUNCTION.radio ("Orientation of strong axis",
        (
        "Vertical (short leg at bottom) ┖",
        "Vertical (short leg at top) ┎",
        "Horizontal (long leg at bottom) ┕",
        "Horizontal (long leg at top) ┍",
        ), key='o_angle')
    STREAMLIT_FUNCTION.markdown ("---")

    ui_button = STREAMLIT_FUNCTION.button('Calculate', on_click=calculate)

    STREAMLIT_FUNCTION.markdown(css, unsafe_allow_html=True)
'''
css = '''
<style>
    [data-testid="stSidebar"]{
        min-width: 380px;
        max-width: 500px;
    }
</style>
'''

# remember, this gets called with every interaction with a streamlit element, so there's no need to invoke a on_change to handle this
# set_session_state_for_details ('i')
# set_session_state_for_details ('channel')
# set_session_state_for_details ('hss')
# set_session_state_for_details ('angle')