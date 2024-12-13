import streamlit as st
from streamlit import session_state as ss


@st.dialog('Turnier und User auswählen')
def login():
    ss['tournament'] = st.selectbox('Turnier auswählen', ['Adventturnier 2024'])
    ss['user'] = st.selectbox('User auswählen', ['Turnierleitung', 'Turnierhelfer', 'Trainer', 'Turnierteilnehmer'])
    if st.button('Anmelden', type='primary', use_container_width=True):
        ss.tournament_date = "2024-12-15"
        ss.logged_in = True
        st.rerun()
    # todo: anmeldung hinzufügen
    # todo: Turnierauswahl automatisch mit Daten aus xml


st.set_page_config(page_title='UJZ Turniermanager', layout="wide", page_icon='images/UJZ_Logo.jpg')#"🏆")
#st.logo(image='images/UJZ_Logo_large.jpg', icon_image='images/UJZ_Logo.jpg', size='large')
c1, c2 = st.columns([25, 3], vertical_alignment="center")
with c1:
    st.markdown("## UJZ Turniermanager")
with c2:
    st.image('images/UJZ_Logo.jpg', use_container_width=True)

if "logged_in" not in ss:
    ss.logged_in = False
login_page = st.Page(login, title="Log in", icon="🔒")
overview_page = st.Page("Pages/overview.py", title="Turnierübersicht", icon="🏠", default=True)
fighter_import_page = st.Page("Pages/fighter_import.py", title="Kämpfer anlegen", icon="🔺")
generate_classes_page = st.Page("Pages/generate_classes.py", title="Gewichtsklassen definieren", icon="🤼")
scoreboard_page = st.Page("Pages/scoreboard.py", title="Scoreboard", icon="🕐")
fighter_page = st.Page("Pages/fighter.py", title="Teilnehmer", icon="🤼")
results_page = st.Page("Pages/results.py", title="Ergebnisse", icon="🏆")

# todo: trainer kann bis 1 Tag vor Start Kämpfer anmelden, dann wird das uploaden gesperrt
if ss.logged_in and ss.user == "Turnierleitung":
    pg = st.navigation(
        {
            "": [overview_page],
            "Verwaltung": [fighter_import_page, generate_classes_page],
            "Wettkampftisch": [scoreboard_page],
            "Turnier": [fighter_page, results_page],
        }
    )
elif ss.logged_in and ss.user == "Turnierhelfer":
    pg = st.navigation(
        {
            "": [overview_page],
            "Wettkampftisch": [scoreboard_page],
            "Turnier": [fighter_page, results_page],
        }
    )
elif ss.logged_in and ss.user == "Turnierteilnehmer":
    pg = st.navigation(
        {
            "": [overview_page],
            "Turnier": [fighter_page, results_page],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()

st.divider()
c1, c2 = st.columns([5, 1], vertical_alignment='center')
with c1:
    st.markdown(f'Version: V1.0 | Releasedatum: 01.01.2025')
with c2:
    st.image('images/UJZ_Logo_large.jpg', use_container_width=True)
