import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from Pages.fighter_import import xml_to_dataframe

ss.df_fighter = xml_to_dataframe(ss.xml_tournament_file)

# todo: nach geschlecht splitten
# todo: nach jahrgang splitten
# todo: nach kilo sortieren


# Schritt 1: Nach Geschlecht aufteilen
df_m = ss.df_fighter[ss.df_fighter["Geschlecht"] == "m"].copy()
df_w = ss.df_fighter[ss.df_fighter["Geschlecht"] == "w"].copy()

# Schritt 2: Nach Jahrgang gruppieren
# Hier definieren wir die Gruppierung nach Jahrgängen
jahrgangsgruppen = {
    "2018": [2018],
    "2017": [2017],
    "2016/2015": [2016, 2015]
}


def split_by_jahrgang(df, gruppen):
    grouped_dfs = {}
    for group_name, jahrgaenge in gruppen.items():
        grouped_dfs[group_name] = df[df["Jahrgang"].isin(jahrgaenge)].copy()
    return grouped_dfs


df_m_grouped = split_by_jahrgang(df_m, jahrgangsgruppen)
df_w_grouped = split_by_jahrgang(df_w, jahrgangsgruppen)


# Schritt 3: Nach Gewicht sortieren
def sort_by_gewicht(grouped_dfs):
    for key, group_df in grouped_dfs.items():
        grouped_dfs[key] = group_df.sort_values(by="Gewicht", ascending=True)
    return grouped_dfs


df_m_grouped_sorted = sort_by_gewicht(df_m_grouped)
df_w_grouped_sorted = sort_by_gewicht(df_w_grouped)

# Ergebnisse anzeigen
for group_name, group_df in df_m_grouped_sorted.items():
    st.write(f"Männlich - Gruppe {group_name}:\n", group_df, "\n")

for group_name, group_df in df_w_grouped_sorted.items():
    st.write(f"Weiblich - Gruppe {group_name}:\n", group_df, "\n")
