# Copyright Sigma Dimensions (TM)

import ifcopenshell
import streamlit as st
from ifctester import ids
from ifctester import reporter
import streamlit.components.v1 as components
import os

def html_report(reporter):
        import pystache
        cwd = os.path.dirname(os.path.realpath(__file__))
        print(cwd)
        with open(os.path.join(cwd, "templates", "report.html"), "r") as file:
            return pystache.render(file.read(), reporter.results)

def callback_model_upload():
    if "uploaded_model" in session and session["uploaded_model"]:
        session["array_buffer"] = session["uploaded_model"].getvalue()
        session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
        session["is_ifc_loaded"] = True

def callback_ids_upload():
    if "uploaded_ids" in session and session["uploaded_ids"]:
        session["ids_file"] = ids.open(session["uploaded_ids"])
        session["is_ids_loaded"] = True
        session["validated"] = False

def get_project_name():
    return session.ifc_file.by_type("IfcProject")[0].Name

def change_project_name():
    if session.project_name_input:
        session.ifc_file.by_type("IfcProject")[0].Name = session.project_name_input
        st.balloons()

def validate_ifc():
    session["ids_file"].validate(session["ifc_file"])
    session["engine"] = reporter.Html(session["ids_file"])
    session["engine"].report()
    session["validated"] = True

def main():      
    st.set_page_config(
        layout= "wide",
        page_title="Valitapp- IFC validator",
        page_icon="✔️"
    )
    st.title("Valitapp - validate IFC models against your IDS")
    st.markdown(
    """ 
    ###  📁 Click on Browse File in the Side Bar to start
    
    
    Start by uploading your IFC, then upload your IDS file to check against. 
    
    """
    )
    
    ## Add IFC file uploader to Side Bar Navigation
    st.sidebar.header('Model Loader')
    st.sidebar.file_uploader("Choose an IFC model", type=['ifc'], key="uploaded_model", on_change=callback_model_upload)

    ## Add IDS file uploader to Side Bar Navigation
    st.sidebar.header('IDS Loader')
    st.sidebar.file_uploader("Choose a Information Delivery Specification (IDS)", type=['.xml',".ids"], key="uploaded_ids", on_change=callback_ids_upload)

    ## Add File Name and Success Message
    if  "is_ifc_loaded" in session and session["is_ifc_loaded"] and \
        "is_ids_loaded" in session and session["is_ids_loaded"]:
        st.sidebar.success(f'Project successfuly loaded')
        st.sidebar.write("🔃 You can reload a new file  ")


        
        if ("is_ids_loaded" in session and session["is_ids_loaded"]):
            ## Validate Model with uploaded IDS
            col1, col2 = st.columns([2,1])
            col1.subheader(f'Start Validating Project "{get_project_name()}"')
            col2.button("✔️ Validate" ,on_click=validate_ifc)

        ### Add Space info for reference
        #st.write(get_space_info())
        if "validated" in session and session["validated"]:
            components.html(html_report(session["engine"]),width=1400,height=1400,scrolling=True)
   


    st.sidebar.info("""
    --------------
    ### Developed by

    #### [mok-see]

    Follow us [on LinkedIn](https://www.linkedin.com/company/mok-see/)

    #### Based on Ifcopenshell, IfcTester and Ifc101 course
    
    --------------
    Find the code [on Github](https://github.com/mok-see)

    License: [GPL-3.0 license](https://github.com/mok-see/valitapp/blob/main/LICENSE)
    
    """)
    st.write("")
    st.sidebar.write("")

if __name__ == "__main__":
    session = st.session_state
    main()