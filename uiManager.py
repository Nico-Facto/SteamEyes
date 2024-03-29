import streamlit as st
from PIL import Image
from joblib import load
from Iajob import Iajob
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px

import sys
import os

from lib.SqlCo import Sqldd

# st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="SteamEyes", layout="wide", page_icon ='ress/Favico.PNG', initial_sidebar_state="expanded")

st.markdown('<style>.css-1aumxhk {background: linear-gradient(to right, #ffffff, #C7E0F1);}</style>',unsafe_allow_html=True)
st.markdown('<style>h1{background: linear-gradient(to left, #ffffff, #C7E0F1);}</style>',unsafe_allow_html=True)
# st.markdown('<style>.css-j8zjtb<{color: #7B49BE);}</style>',unsafe_allow_html=True)

@st.cache
def get_data():
    my_bdd = Sqldd()
    cnx, cursor = my_bdd.get_bdd_co()
    # global df
    df = pd.read_sql('SELECT * FROM app_hover_public', con=cnx)
    cnx.close()
    cursor.close()
    # global nb_data
    nb_data = len(df['Dev_team'])
    return df, nb_data



def display_ui():
    im_1 = Image.open('ress/Capture7456.PNG')
    st.image(im_1,use_column_width=False, clamp=False)
    st.sidebar.title("Artificial Intelligence")
    st.sidebar.subheader("Predict user interaction with your application on Steam store")


def canvas_button():
    global ai_button
    ai_button = st.sidebar.button("Ai Job")
    global dash_button
    dash_button = st.sidebar.button("Dashboard Data ")
    global info_button
    info_button = st.sidebar.button("Information")

def set_databrick():
    global df
    df = load('Model/databrick_v2.joblib')
    global nb_data
    nb_data = len(df['Dev_team'])
   
def parrallel_plot(df):
    pp_df = pd.DataFrame(df, columns=['status_reco','Price', 'Nb_language','Nb_achievements' ])

    pp_df = pp_df.drop(pp_df[pp_df.Price > 300].index)
    pp_df = pp_df.drop(pp_df[pp_df.Nb_achievements > 6000].index)
    fig = px.parallel_coordinates(pp_df, color="status_reco",
                                 color_continuous_scale="Inferno",
                                 color_continuous_midpoint=2)
    return fig


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

    st.subheader("Breakdown of categories by class")
    st.text("0 : No review")
    st.text("1 : Got review")

    fig = parrallel_plot(df)
    st.plotly_chart(fig)

    colA , colB, colC = st.beta_columns(3)
    count = 0
    for i in col_bool:
        fig, ax = plt.subplots()
        plt.title(f"Number of presence or not for {i}")
        sns.countplot(df[i], 
                   facecolor=(0.82, 0.82, 0.12, 0.33),
                   linewidth=5,
                   edgecolor=sns.color_palette("dark", 3),
                   )
        labels = ['Not Present', 'Present']
        ax.set_xticklabels(labels)
        if count % 2 == 0:
            colA.pyplot(fig)
        else:
            colB.pyplot(fig)
        count +=1     

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
    colA, colB, colC = st.beta_columns(3)

    app_ = colA.radio("What's kind of application ?",
                    ('Game', 'Demo','Downloadable Content'))

    dev_ = colA.number_input('Set number of game published on steam by developer team', min_value=1, value=1)
    publisher_ = colA.number_input('Set number of game published on steam by publisher team',min_value=1, value=1)

    Self_editor = colA.checkbox("Self Editor")
    if Self_editor:
        editor_self_ = 1
    else:
        editor_self_ = 0

    os_ = colA.multiselect('What operating systems are supported',
                            ['Windows', 'Linux', 'Mac', 'Steam Remote'],
                            ['Windows','Linux', 'Mac', 'Steam Remote'])

    price_ = colA.number_input("Previous Price")



    Prymary_ = colB.radio("What's prymary genre you will selected on steam ?",
                    ('Action', 'Free to Play', 'Strategy', 'Indie', 'RPG',
                    'Video Production', 'Casual', 'Simulation',
                    'Racing', 'Adventure', 'Sports', 'Massively Multiplayer',
                    'Animation & Modeling', 'Early Access', 'Utilities',
                    'Audio Production', 'Design & Illustration', 'Photo Editing',
                    'Violent', 'Web Publishing', 'Education', 'Game Development',
                    'Software Training', 'Accounting', 'Gore','Nudity'
                    'Sexual Content','Unknown Genre'))

    language_ = colC.number_input('How many language your application support ? (Example : English Interface + Audio + Sub-titles = 3)', min_value=1, value=1)
    achiev_ = colC.number_input('How many achievements your application has ? (Example : 17)', value=0)

    colC.subheader('Check the boxes that your application contains')

    Controller_support = colC.checkbox("Controller support")
    if Controller_support:
        Controller_ = 1
    else:
        Controller_ = 0

    Is_free_app = colC.checkbox("Free to play")
    if Is_free_app:
        Is_free_ = 1
    else:
        Is_free_ = 0

    Workshop_visible = colC.checkbox("Workshop visible")
    if Workshop_visible:
        Workshop_ = 1
    else:
        Workshop_ = 0  

    Only_vr_support = colC.checkbox("Only vr support")
    if Only_vr_support:
        Only_vr_ = 1
    else:
        Only_vr_ = 0  

    Vr_support = colC.checkbox("Vr support")
    if Vr_support:
        supportVr_ = 1
    else:
        supportVr_ = 0  

    Has_adult_content = colC.checkbox("Has adult content")
    if Has_adult_content:
        adult_ = 1
    else:
        adult_ = 0  

    Single_player = colC.checkbox("Single player")
    if Single_player:
        Single_ = 1
    else:
        Single_ = 0  

    Coop_player = colC.checkbox("Coop player")
    if Coop_player:
        Coop_ = 1
    else:
        Coop_ = 0  

    Multi_player = colC.checkbox("Multi player")
    if Multi_player:
        Multy_ = 1
    else:
        Multy_ = 0  

    Early_Access = colC.checkbox("Early Access")
    if Early_Access:
        Early_ = 1
    else:
        Early_ = 0  

    if st.button('Predict'):

        try:
            input_data = {
            "App_cat": [f'{app_}'],
            "Os_supported": [len(os_)],
            "Prymary_genre": [f'{Prymary_}'],
            "Controller_support": [Controller_],
            "Is_free_app": [Is_free_],
            "Nb_language": [int(language_)],
            "Only_vr_support": [Only_vr_],
            "Vr_support": [supportVr_],
            "Has_adult_content": [adult_],
            "Nb_achievements": [int(achiev_)],
            "Single_player": [Single_],
            "Coop_player": [Coop_],
            "Multi_player": [Multy_],
            "Early_Access": [Early_],
            "Price": [price_],
            "Workshop_visible": [Workshop_],
            "exp_dev_team": [f'{dev_}'],
            "exp_publish_team": [f'{publisher_}'],
            "Self_editor" : [editor_self_],
            }

            st.dataframe(input_data)
            job = Iajob(input_data)
            job.predict_job()

            colaf , colbf, colcf = st.beta_columns(3)
            try:
                ph1_succes, probas_disp_f1, ph2_succes, probas_disp_f2, res= job.display_on_app()
                colaf.write(f"Review = Yes  -- Trust : {probas_disp_f1} %")
                if ph2_succes:
                    colbf.write(f"Positive -- Trust : {probas_disp_f2} %")
                else:
                    colbf.write(f"Negative -- Trust : {probas_disp_f2} %")    
                colcf.write(f"Number of review estimated : {res}")
            except : 
                ph1_succes, probas_disp_f1 = job.display_on_app()
                colaf.write(f"Review = No  -- Trust : {probas_disp_f1} %")

        except ValueError as identifier:
            st.warning("Error in your input : ")
            st.warning(identifier)



def void_update():
    display_ui()
    canvas_button()

    # df, nb_data = get_data()
    set_databrick()

    if info_button:
        display_info()
    elif dash_button:
        display_dahboard()    
    else: 
        input_output()


void_update()