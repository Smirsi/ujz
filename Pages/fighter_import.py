import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from io import BytesIO


# todo: upload der csv Dateien
# todo: export in xml Datei
# todo: import in df
# todo: Darstellung inklusive Bearbeitung (und sortieren, nach w/m, Verein)
# todo: manuelle kämpfereingabe
# todo: beispiel .csv downloaden


# Funktion, um eine XML-Datei zu formatieren
def prettify_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = parseString(rough_string)
    return reparsed.toprettyxml(indent="", newl="")


# Funktion, um die CSV-Datei in XML zu konvertieren und zu aktualisieren
def csv_to_xml(csv_data, xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    tournament = root.find(f"tournament[@date='{ss.tournament_date}']")

    for _, row in csv_data.iterrows():
        existing_fighter = tournament.find(f"fighter[@firstname='{row['Vorname']}'][@lastname='{row['Nachname']}']")
        if existing_fighter is None:
            fighter = ET.SubElement(tournament, "fighter", firstname=row['Vorname'], lastname=row['Nachname'])
            ET.SubElement(fighter, "club").text = row['Verein/Sektion']
            ET.SubElement(fighter, "birthyear").text = str(row['Jahrgang'])
            ET.SubElement(fighter, "weight").text = str(row['Gewicht'])
            ET.SubElement(fighter, "note").text = row['Bemerkung']
        else:
            existing_fighter.find("club").text = row['Verein/Sektion']
            existing_fighter.find("birthyear").text = str(row['Jahrgang'])
            existing_fighter.find("weight").text = str(row['Gewicht'])
            existing_fighter.find("note").text = row['Bemerkung']

    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(prettify_xml(root))


# Funktion, um die XML-Datei in einen DataFrame zu konvertieren
def xml_to_dataframe(xml_file, tournament_date):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    tournament = root.find(f"tournament[@date='{tournament_date}']")
    if tournament is None:
        return pd.DataFrame([])

    fighters = []
    for fighter in root.find("tournament").findall("fighter"):
        fighters.append({
            "Vorname": fighter.attrib["firstname"],
            "Nachname": fighter.attrib["lastname"],
            "Verein/Sektion": fighter.find("club").text,
            "Jahrgang": int(fighter.find("birthyear").text),
            "Gewicht": float(fighter.find("weight").text),
            "Bemerkung": fighter.find("note").text
        })

    return pd.DataFrame(fighters)


# Funktion, um Änderungen im DataFrame wieder in die XML-Datei zu schreiben
def dataframe_to_xml(dataframe, xml_file, tournament_date):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    tournament = root.find(f"tournament[@date='{tournament_date}']")

    for _, row in dataframe.iterrows():
        fighter = tournament.find(f"fighter[@firstname='{row['Vorname']}'][@lastname='{row['Nachname']}']")
        if fighter is not None:
            fighter.find("club").text = row['Verein/Sektion']
            fighter.find("birthyear").text = str(row['Jahrgang'])
            fighter.find("weight").text = str(row['Gewicht'])
            fighter.find("note").text = row['Bemerkung']

    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(prettify_xml(root))


@st.dialog('Einzelnen Kämpfer hinzufügen')
def add_new_fighter():
    vorname = st.text_input("Vorname")
    nachname = st.text_input("Nachname")
    verein = st.text_input("Verein/Sektion")
    jahrgang = st.number_input("Jahrgang", min_value=1900, max_value=2100, step=1, value=2014)
    gewicht = st.number_input("Gewicht", min_value=0.0, step=0.1, value=30.0)
    bemerkung = st.text_input("Bemerkung")
    if st.button('Kämpfer hinzufügen', type='primary', use_container_width=True):
        new_fighter = pd.DataFrame([{"Vorname": vorname, "Nachname": nachname, "Verein/Sektion": verein,
                                     "Jahrgang": int(jahrgang), "Gewicht": float(gewicht), "Bemerkung": bemerkung}])
        csv_to_xml(new_fighter, xml_tournament_file)
        st.rerun()


@st.dialog('CSV mit Kämpfer hochladen')
def add_multiple_fighters():
    csv_files = st.file_uploader("Kämpfer hochladen", type='.csv', accept_multiple_files=True)
    if st.button('Kämpfer hinzufügen', type='primary', use_container_width=True):
        if csv_files:
            for file in csv_files:
                csv = pd.read_csv(BytesIO(file.getvalue()), encoding="utf-8", delimiter=';', decimal=',')
                csv_to_xml(csv, xml_tournament_file)
                ss.df_fighter = xml_to_dataframe(xml_tournament_file, ss.tournament_date)
        st.rerun()


st.title("Kämpfer verwalten")
# Streamlit-Anwendung
xml_tournament_file = "tournaments.xml"
ss.df_fighter = xml_to_dataframe(xml_tournament_file, ss.tournament_date)
if not ss.df_fighter.empty:
    edited_dataframe = st.data_editor(ss.df_fighter, num_rows="dynamic", use_container_width=True, hide_index=True,
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
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('Einzelnen Kämpfer hinzufügen', type='primary', use_container_width=True):
        add_new_fighter()
with col2:
    if st.button('Mehrere Kämpfer hinzufügen', type='primary', use_container_width=True):
        add_multiple_fighters()
with col3:
    if st.button('Änderungen speichern', type='primary', use_container_width=True) and not ss.df_fighter.empty:
        dataframe_to_xml(edited_dataframe, xml_tournament_file, ss.tournament_date)
        st.toast("Änderungen wurden gespeichert.")
