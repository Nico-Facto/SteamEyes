import streamlit as st
from PIL import Image
from joblib import load
from Iajob import Iajob

import matplotlib.pyplot as plt
import seaborn as sns

import time

def display_ui():
    st.text("""
    TEST""")
    im_1 = Image.open('ress/Capture7456.PNG')
    st.image(im_1,use_column_width=True)
    st.subheader("Artificial intelligence try to predict user interaction with your app on the store")
    im_2 = Image.open('ress/scr.PNG')
    st.image(im_2,use_column_width=True)


def canvas_button():
    global ai_button
    ai_button = st.button("Ai Job")
    global dash_button
    dash_button = st.button("Dashboard Data ")
    global info_button
    info_button = st.button("Information")

def set_databrick():
    global df
    df = load('Model/databrick_v1.joblib')
    global nb_data
    nb_data = len(df['Dev_team'])

def display_dahboard():
    st.subheader(f"Some observations on {nb_data} applications")

    graph1 = df.App_cat.value_counts().sort_values(ascending=False)
    st.bar_chart(graph1, use_container_width=True)

    graph2 = df.Prymary_genre.value_counts().sort_values(ascending=False)
    st.bar_chart(graph2, use_container_width=True)

    st.subheader("Top 20 develop presence")
    st.write(df.Dev_team.value_counts().head(20))

    st.subheader("Top 20 publisher presence")
    st.write(df.Publisher_team.value_counts().head(20))

    col_bool = ['Controller_support', 'Is_free_app',
       'Workshop_visible', 'Only_vr_support', 'Vr_support',
       'Has_adult_content', 'Single_player', 'Coop_player',
       'Multi_player','Early_Access']

    for i in col_bool:
        sns.countplot(df[i])
        st.pyplot(figsize=(5,5))     

def display_info():
    st.title("Information")
    st.subheader("AI build with Datascience !")
    st.text(f"""
    For build this app, {nb_data} applications datas was collected from steam.""")
    st.text("""
    This application only takes the categorical data of the applications 
    and ignores all the graphic elements that can be put on the store page.""")
    st.text("""
    No data is recovered while you use the application""")
    st.text("""
    ! This application is not affilied with Steam !""")

def input_output():
    app_ = st.radio("What's kind of application ?",
                    ('Game', 'Legacy Media', 'Application', 'Demo', 'Config','Downloadable Content', 'Tool', 'Music', 'Video','Series', 'Hardware','Unknown'))

    dev_ = st.text_area('Set your developer Name (Use the same name as it usually appears on steam)')
    publisher_ = st.text_area('Set the publisher Name (Use the same name as it usually appears on steam)')

    os_ = st.multiselect('What operating systems are supported',
                            ['Windows', 'Linux', 'Mac', 'Steam Remote'],
                            ['Windows','Linux', 'Mac', 'Steam Remote'])

    Prymary_ = st.radio("What's prymary genre you will selected on steam ?",
                    ('Action', 'Free to Play', 'Strategy', 'Indie', 'RPG',
        'Video Production', 'Casual', 'Simulation',
        'Racing', 'Adventure', 'Sports', 'Massively Multiplayer',
        'Animation & Modeling', 'Early Access', 'Utilities',
        'Audio Production', 'Design & Illustration', 'Photo Editing',
        'Violent', 'Web Publishing', 'Education', 'Game Development',
        'Software Training', 'Accounting', 'Gore','Nudity'
        'Sexual Content','Unknown Genre'))

    language_ = st.text_area('How many language your application support ? (Example : English Interface + Audio + Sub-titles = 3)')
    achiev_ = st.text_area('How many achievements your application has ? (Example : 17)')

    st.subheader('Check the boxes that your application contains')

    Controller_support = st.checkbox("Controller support")
    if Controller_support:
        Controller_ = 1
    else:
        Controller_ = 0

    Is_free_app = st.checkbox("Free to play")
    if Is_free_app:
        Is_free_ = 1
    else:
        Is_free_ = 0

    Workshop_visible = st.checkbox("Workshop visible")
    if Workshop_visible:
        Workshop_ = 1
    else:
        Workshop_ = 0  

    Only_vr_support = st.checkbox("Only vr support")
    if Only_vr_support:
        Only_vr_ = 1
    else:
        Only_vr_ = 0  

    Vr_support = st.checkbox("Vr support")
    if Vr_support:
        supportVr_ = 1
    else:
        supportVr_ = 0  

    Has_adult_content = st.checkbox("Has adult content")
    if Has_adult_content:
        adult_ = 1
    else:
        adult_ = 0  

    Single_player = st.checkbox("Single player")
    if Single_player:
        Single_ = 1
    else:
        Single_ = 0  

    Coop_player = st.checkbox("Coop player")
    if Coop_player:
        Coop_ = 1
    else:
        Coop_ = 0  

    Multi_player = st.checkbox("Multi player")
    if Multi_player:
        Multy_ = 1
    else:
        Multy_ = 0  

    Early_Access = st.checkbox("Early Access")
    if Early_Access:
        Early_ = 1
    else:
        Early_ = 0  

    if st.button('Predict'):

        try:
            input_data = {
            "App_cat": [f'{app_}'],
            "Dev_team": [f'{dev_}'],
            "Publisher_team": [f'{publisher_}'],
            "Os_supported": [len(os_)],
            "Prymary_genre": [f'{Prymary_}'],
            "Controller_support": [Controller_],
            "Is_free_app": [Is_free_],
            "Nb_language": [int(language_)],
            "Workshop_visible": [Workshop_],
            "Only_vr_support": [Only_vr_],
            "Vr_support": [supportVr_],
            "Has_adult_content": [adult_],
            "Nb_achievements": [int(achiev_)],
            "Single_player": [Single_],
            "Coop_player": [Coop_],
            "Multi_player": [Multy_],
            "Early_Access": [Early_],
            }

            job = Iajob(input_data)
            job.predict_job()

            try:
                ph1_succes, probas_disp_f1, ph2_succes, probas_disp_f2, res= job.display_on_app()
                ph1_succes = ph1_succes ## just for clean linter in vscode
                st.write("Review = Yes", " -- Trust : ", probas_disp_f1, " %")
                if ph2_succes:
                    st.write("Positive", " -- Trust : ", probas_disp_f2, " %")
                else:
                    st.write("Negative", " -- Trust : ", probas_disp_f2, " %")    
                st.write("Number of review estimated : ",res)
            except : 
                ph1_succes, probas_disp_f1 = job.display_on_app()
                st.write("Review = No" , " -- Trust : ", probas_disp_f1, " %")

        except ValueError as identifier:
            st.warning("Error in your input : ")
            st.warning(identifier)



def void_update():
    display_ui()
    canvas_button()
    set_databrick()

    if info_button:
        display_info()
    elif dash_button:
        display_dahboard()    
    else: 
        input_output()


void_update()