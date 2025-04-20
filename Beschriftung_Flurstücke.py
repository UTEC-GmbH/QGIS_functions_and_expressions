from qgis.core import qgsfunction


@qgsfunction(args="auto", group="Benutzerausdrücke", usesGeometry=False)
def beschriftung_flurstuecke(
    nur_flurst: bool = False,
    spalten: dict[str, str] | None = None,
    feature=None,
    parent=None,
) -> str:
    """Erstellt eine Beschriftung für Flurstücke basierend auf verfügbaren Attributen.
    Setzt die Teile mit Zeilenumbruch und korrekten Trennern zusammen.<br><br>

    <H1>Parameter:</H1><br>
    <ul>
        <li><b>nur_flurst</b> (bool): Wenn True, wird nur die Flurstücksnummer
            (Zähler[/Nenner]) zurückgegeben. Standard: False.</li>
        <li><b>spalten</b> (dict): Ein Dictionary, das die Standard-Schlüssel
            ('landkreis', 'gemarkung', 'flur', 'zaehler', 'nenner') auf die
            tatsächlichen Spaltennamen in der Attributtabelle abbildet.
            Wenn eine Spalte nicht verwendet werden soll, kann ihr Wert im
            Dictionary auf eine leere Zeichenkette ('') gesetzt oder der
            entsprechende Schlüssel weggelassen werden.<br>
            Standardmäßig werden folgende Spaltennamen verwendet:
            <pre><code>{
    "landkreis": "kreis",
    "gemarkung": "gemarkung",
    "flur": "flur",
    "zaehler": "flstnrzae",
    "nenner": "flstnrnen"
    }</code></pre>
        </li>
    </ul>

    <H1>Beispiele im QGIS Ausdruckseditor:</H1><br>

    Volle Beschriftung mit Standard-Spaltennamen:<br>
    <code>beschriftung_flurstuecke()</code><br>
    <i>oder</i><br>
    <code>beschriftung_flurstuecke(nur_flurst:=False)</code><br><br>

    Nur Flurstücksnummer mit Standard-Spaltennamen:<br>
    <code>beschriftung_flurstuecke(nur_flurst:=True)</code><br><br>

    Volle Beschriftung, aber ohne Landkreis und Gemarkung (Standard-Spaltennamen):<br>
    <code>beschriftung_flurstuecke(spalten:=map('landkreis', '', 'gemarkung', ''))</code>
    <br><i>(Beachten Sie: Die restlichen Standardspalten werden weiterhin verwendet)</i><br><br>

    Volle Beschriftung mit abweichenden Spaltennamen für Flur, Zähler, Nenner
    und ohne Gemarkung:<br>
    <code>beschriftung_flurstuecke(
        spalten:=map(
            'gemarkung', '',
            'flur', 'FlurNr',
            'zaehler', 'Flurst_Z',
            'nenner', 'Flurst_N'
        )
    )</code><br>
    <i>(Beachten Sie: 'landkreis' verwendet weiterhin den Standard 'kreis')</i><br><br>

    Nur Flurstücksnummer mit abweichenden Spaltennamen:<br>
    <code>beschriftung_flurstuecke(
        nur_flurst:=True,
        spalten:=map('zaehler', 'NrZaehler', 'nenner', 'NrNenner')
    )</code><br><br>

    """
    if feature is None:
        return "Fehler: Kein Feature übergeben."

    default_columns: dict[str, str] = {
        "landkreis": "kreis",
        "gemarkung": "gemarkung",
        "flur": "flur",
        "zaehler": "flstnrzae",
        "nenner": "flstnrnen",
    }

    # Starte mit den Standardwerten
    cols: dict[str, str] = default_columns.copy()
    # Überschreibe/Ergänze mit den übergebenen Spalten, falls vorhanden
    if spalten:
        cols.update(spalten)

    def col_value(key: str) -> str | None:
        """Holt den Wert sicher aus dem Feature anhand des Dictionary-Schlüssels."""
        col_name = cols.get(key)
        if col_name and col_name in feature.fields().names():
            val = feature[col_name]
            # Prüfe auf None und leere Strings nach dem Strippen
            if val is not None:
                str_val = str(val).strip()
                if str_val and str_val.upper() != "NULL":
                    return str_val
        return None

    zael_val: str | None = col_value("zaehler")
    nenner_val: str | None = col_value("nenner")

    # Flurstücksteil zusammenbauen
    flurst_teil: str = ""
    if zael_val:
        flurst_teil = zael_val
        if nenner_val:
            flurst_teil += f"/{nenner_val}"

    if nur_flurst:
        return flurst_teil  # Nur Zähler[/Nenner] zurückgeben

    # Komplette Beschriftung zusammenbauen
    lk_val: str | None = col_value("landkreis")
    gem_val: str | None = col_value("gemarkung")
    flur_val: str | None = col_value("flur")

    teile: list[str] = []
    if lk_val:
        teile.append(lk_val)
    if gem_val:
        teile.append(gem_val)

    flur_prefix: str = "Flur " if flur_val else ""
    flurst_prefix: str = "Flurstück " if flurst_teil and not nur_flurst else ""

    # Kombiniere Flur und Flurstück für die letzte Zeile
    letzte_zeile: str = (
        f"{flur_prefix}{flur_val or ''} {flurst_prefix}{flurst_teil}".strip()
    )
    if letzte_zeile:
        teile.append(letzte_zeile)

    return " \n".join(
        teile
    )  # Fügt Zeilenumbruch nur hinzu, wenn mehrere Teile existieren
