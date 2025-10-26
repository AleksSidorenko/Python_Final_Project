# ITCinema CLI 🎬

**ITCinema** — ein Konsolenprogramm in Python zur Filmsuche in Datenbanken (MySQL),
in denen Filme und Statistiken zu Benutzeranfragen gespeichert sind.
Der Benutzer kann Filme nach **Schlüsselwörtern**, **Genre** und **Jahr** suchen
und außerdem die beliebtesten Suchanfragen anzeigen.
Alle Aktionen werden in einer separaten Datenbank protokolliert.

## 📌 Ziel des Projekts

Bereitstellung einer benutzerfreundlichen Möglichkeit, über das Terminal
mit der Filmdatenbank zu interagieren:
Suche nach Genres und Schlüsselwörtern, Nachverfolgung beliebter Suchanfragen
und Anzeige detaillierter Informationen zu Filmen.

## 🛠️ Installation

### Anforderungen

* Python 3.8+
* Installierter MySQL-Server
* Vorhandene Datenbank mit Tabellen für Filme und Suchanfragen

### Installation der Abhängigkeiten

```bash
pip3 install -r requirements.txt
```

## ⚙️ Konfiguration

Die Datei `config.py` enthält die richtigen Einstellungen
für die Verbindung zu MySQL.

## 🚀 Start der Anwendung

```bash
python3 app.py
```

## 🧭 Hauptfunktionen

* 🔎 Filmsuche nach Schlüsselwörtern (mit Anzeige beliebter Suchanfragen)
* 🎭 Filmsuche nach Genre und Jahr oder Jahresbereich
* 📊 Anzeige der Top-5 der beliebtesten Suchanfragen und Genres
* 📋 Seitliche Ausgabe der Ergebnisse
* 📝 Anzeige detaillierter Filminformationen

## 💻 Beispielverwendung

```bash
python3 app.py
```

Willkommen bei ITCinema CLI!

> Wählen Sie eine Aktion:

* Suche nach Schlüsselwort
* Suche nach Genre und Jahr
* Top beliebte Suchanfragen
* Beenden

```

## 📁 Projektstruktur

```

├── app.py                 # Einstiegspunkt der Anwendung
├── config.py              # MySQL-Verbindungskonfiguration
├── db.py                  # Datenbankfunktionen
├── logic.py               # Hauptlogik für Suche und Anzeige
├── menu.py                # Navigationsmenü
├── logo.py                # Logo
├── requirements.txt       # Abhängigkeiten
└── README.md              # Diese Datei

```

**Autor:**  
Alex Sidorenko
