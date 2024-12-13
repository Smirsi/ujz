from Pages.fighter_import import xml_to_dataframe
import streamlit as st
from streamlit import session_state as ss


st.title("Teilnehmer")
xml_tournament_file = "tournaments.xml"
ss.df_fighter = xml_to_dataframe(xml_tournament_file, ss.tournament_date)
if not ss.df_fighter.empty:
    edited_dataframe = st.dataframe(ss.df_fighter, use_container_width=True, hide_index=True,
                                    column_config={
                                        "Jahrgang": st.column_config.NumberColumn(
                                            "Jahrgang",
                                            min_value=1900,
                                            max_value=2025,
                                            step=1,
                                            format="%d",
                                        ),
                                        "Gewicht": st.column_config.NumberColumn(
                                            "Gewicht",
                                            min_value=0,
                                            max_value=200,
                                            step=0.1,
                                            format="%.1f kg",
                                        ),
                                    },
                                    )
