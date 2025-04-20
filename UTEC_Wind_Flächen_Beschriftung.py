"""Beschriftung der Kranstellflächen und Zuwegungen."""

from qgis.core import QgsFeature
from qgis.gui import qgsfunction

DEFAULT_KSF_COLUMN_NAMES: dict[str, str] = {
    "dauerhaft": "UTEC - KSF dauerhaft",
    "temporär": "UTEC - KSF temporär",
    "Blattlager": "UTEC - KSF Blattlager",
    "Fundament": "UTEC - Fundament & Rampe",
}

DEFAULT_WEG_COLUMN_NAMES: dict[str, str] = {
    "dauerhaft": "UTEC - Zuwegung dauerhaft",
    "temporär": "UTEC - Zuwegung temporär",
}


@qgsfunction(args="auto", group="Benutzerdefinierte", usesGeometry=False)
def generiere_flaechen_beschriftung(
    feature: QgsFeature,
    bez_column: str = "UTEC - Bezeichnung",
    ksf_columns: dict[str, str] | None = None,
    weg_columns: dict[str, str] | None = None,
) -> str:
    """Generiert eine formatierte Beschriftung für Kranstellflächen und Zuwegung
    von Windparks basierend auf verschiedenen Attributen.

    Args:
        feature (QgsFeature): Das aktuelle Feature.
        bze_column (str): Der Name des Spalte in der Attributstabelle 
            mit der Bezeichnung (z.B. WEA-Nummer).
        ksf_columns (dict | None): Ein Dictionary mit den Spaltennamen 
            der Attributstabelle für die Kranstellflächen.
            Falls nicht gegeben, wird folgender Standardwert verwendet: {
                "dauerhaft": "UTEC - KSF dauerhaft",
                "temporär": "UTEC - KSF temporär",
                "Blattlager": "UTEC - KSF Blattlager",
                "Fundament": "UTEC - Fundament & Rampe"
            }
        weg_columns (dict | None): Ein Dictionary mit den Spaltennamen 
            der Attributstabelle für die Zuwegungen.
            Falls nicht gegeben, wird folgender Standardwert verwendet: {
                "dauerhaft": "UTEC - Zuwegung dauerhaft",
                "temporär": "UTEC - Zuwegung temporär"
            }

    Returns:
        str: Die formatierte Beschriftung als HTML-String.
    """
    ksf_layer_name: dict[str, str] = ksf_columns or DEFAULT_KSF_COLUMN_NAMES
    weg_layer_name: dict[str, str] = weg_columns or DEFAULT_WEG_COLUMN_NAMES

    dic_ksf: dict[str, float] = {
        "dauerhaft": feature[ksf_layer_name["dauerhaft"]],
        "temporär": feature[ksf_layer_name["temporär"]],
        "Blattlager": feature[ksf_layer_name["Blattlager"]],
        "Fundament": feature[ksf_layer_name["Fundament"]],
    }
    dic_weg: dict[str, float] = {
        "dauerhaft": feature[weg_layer_name["dauerhaft"]],
        "temporär": feature[weg_layer_name["temporär"]],
    }

    anzahl_ksf: int = sum(val > 0 for val in dic_ksf.values())
    anzahl_weg: int = sum(val > 0 for val in dic_weg.values())

    head: str = f"<p><b>{feature[bez_column]}</b></p>"

    if anzahl_ksf > 1:
        head_ksf: str = "<p><u> Kranstellfläche </u></p>"
        body_ksf: str = "<br>".join(
            [
                f"{key}: {val:,.0f} m²".replace(",", ".")
                for key, val in dic_ksf.items()
                if val > 0
            ]
        )
    elif anzahl_ksf == 1:
        head_ksf = ""
        body_ksf = next(
            (
                f"KSF {key}: {val:,.0f} m²".replace(",", ".")
                for key, val in dic_ksf.items()
                if val > 0
            )
        )

    else:
        head_ksf = ""
        body_ksf = ""

    if anzahl_weg > 1:
        head_weg: str = "<p><u> Zuwegung </u></p>"
        body_weg: str = "<br>".join(
            [
                f"{key}: {val:,.0f} m²".replace(",", ".")
                for key, val in dic_weg.items()
                if val > 0
            ]
        )
    elif anzahl_weg == 1:
        head_weg = ""
        body_weg = next(
            (
                f"{key}: {val:,.0f} m²".replace(",", ".")
                for key, val in dic_weg.items()
                if val > 0
            )
        )
    else:
        head_weg = ""
        body_weg = ""

    return f"{head}{head_ksf}{body_ksf}{head_weg}{body_weg}"
