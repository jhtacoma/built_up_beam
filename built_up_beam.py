import streamlit as st
import sectionproperties.pre.library.steel_sections as steel_geom
from sectionproperties.pre.pre import Material
from sectionproperties.analysis.section import Section


steel_300 = Material(
    "300 MPa Steel", 
    elastic_modulus=200e3,
    poissons_ratio=0.3, 
    yield_strength=300, 
    density=7.7,
    color="teal"
)

steel_350 = Material(
    "350 MPa Steel", 
    elastic_modulus=200e3,
    poissons_ratio=0.3, 
    yield_strength=350, 
    density=7.7,
    color="goldenrod"
)

def plot_section (
        material:Material,
        section_type:str='channel',
        d:float=1,
        b:float=1,
        t:float=1,
        t_f:float=1,
        t_w:float=1,
        r_out:float=1,
        n_r:int=1,
        k:float=1
        ) -> steel_geom:


    if section_type == 'angle':

        section = steel_geom.angle_section(
            d=d,
            b=b,
            t=t_f,
            r_r = t_f/2,
            r_t = t_f/2,
            n_r=n_r,
            material=material
        )

    elif section_type == 'channel':

        section = steel_geom.channel_section(
            d=d,
            b=b,
            t_f=t_f,
            t_w=t_w,
            r= t_f - t_w,
            n_r=n_r,
            material=material
        )

    elif section_type == 'hss':

        section = steel_geom.rectangular_hollow_section(
            d=d,
            b=b,
            t=t_f,
            r_out=r_out,
            n_r=n_r,
            material=material
        )
    
    elif section_type == 'i':

        section = steel_geom.i_section(
            d=d,
            b=b,
            t_f=t_f,
            t_w=t_w,
            r= t_f - t_w,
            n_r=n_r,
            material=material
        )

    return section


# main()


