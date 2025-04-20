from typing import Any

from qgis.core import qgsfunction


@qgsfunction(args="auto", group="Benutzerausdrücke")
def beschriftung_flurstuecke(
    spalte_landkreis: str | None = "kreis",
    spalte_gemarkung: str | None = "gemarkung",
    spalte_flur: str | None = "flur",
    spalte_zaehler: str | None = "flstnrzae",
    spalte_nenner: str | None = "flstnrnen",
    feature=None,
    parent=None,
):
    """
    Erstellt eine Beschriftung für Flurstücke basierend auf verfügbaren Attributen.
    Setzt die Teile mit Zeilenumbruch und korrekten Trennern zusammen.<br><br>

    <H1>Hinweis:</H1><br>
    Die Spaltennamen müssen als Text 
    (mit einfachen Anführungszeichen 'Spaltenname')
    in folgender Reihenfolge angegeben werden:<br><br>

    1. Spaltenname für <b>Landkreis</b> (Standard: 'kreis')<br>
    2. Spaltenname für <b>Gemarkung</b> (Standard: 'gemarkung')<br>
    3. Spaltenname für <b>Flur</b> (Standard: 'flur')<br>
    4. Spaltenname für <b>Flurstück - Zähler</b> (Standard: 'flstnrzae')<br>
    5. Spaltenname für <b>Flurstück - Nenner</b> (Standard: 'flstnrnen')<br><br>

    Spalten, die nicht angezeigt werden sollen, 
    müssen als leere Zeichenkette ('') übergeben werden.<br><br>


    <H1>Beispiele:</H1><br>

    ...volle Beschriftung mit Standardwerten:<br>
    <i>beschriftung_flurstuecke()</i><br><br>
    
    ...Beschriftung mit Standardwerten ohne Landkreis und Gemarkung:<br>
    <i>beschriftung_flurstuecke('', '')</i><br><br>
    
    ...Beschriftung mit Standardwerten ohne Gemarkung:<br>
    <i>beschriftung_flurstuecke('kreis', '')</i><br><br>
   
    ...anderen Spaltennamen und ohne Landkreis und Gemarkung:<br>
    <i>beschriftung_flurstuecke('', '', 'Flur', 'Flurstück-Z', 'Flurstück-N')</i><br><br>

    
    """

    def col_value(col_name: str | None) -> str | None:
        if col_name and col_name in feature.fields().names():
            val = feature[col_name]
            return str(val).strip() if val not in [None, "NULL"] else None
        return None

    lk: str = (
        f"{col_value(spalte_landkreis)} \n" if col_value(spalte_landkreis) else ''
    )
    gem: str | None = (
        f"{col_value(spalte_gemarkung)} \n" if col_value(spalte_gemarkung) else ''
    )
    flur: str | None = (
        f"Flur {col_value(spalte_flur)} " if col_value(spalte_flur) else ''
    )
    zael: str | None = (
        f"Flurstück {col_value(spalte_zaehler)}" if col_value(spalte_zaehler) else ''
    )
    nenner: str | None = (
        f"/{col_value(spalte_nenner)}" if col_value(spalte_nenner) else ''
    )

    return f"{lk}{gem}{flur}{zael}{nenner}"
