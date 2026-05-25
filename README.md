# 📄 Document Manager - Dein persönlicher Dokumentenverwaltungstool

Ein benutzerfreundliches Desktop-Programm zur Verwaltung, Erstellung und Bearbeitung von Word- und PDF-Dokumenten mit organisierten Arbeitsbereichen.

## ✨ Features

- 📚 **Arbeitsbereiche** - Organisiere deine Dokumente nach Themen
- 📝 **Dokumentenverwaltung** - Erstelle, öffne und bearbeite Word- und PDF-Dateien
- 📖 **Word-Unterstützung** - Vollständige Unterstützung für `.docx` Dateien
- 📕 **PDF-Unterstützung** - Lese und erstelle PDF-Dateien
- 💾 **Speicherfunktion** - Sichere deine Änderungen lokal
- 🎨 **Benutzerfreundliche GUI** - Moderne, intuitive Oberfläche mit PyQt6

## 🚀 Installation & Erste Schritte

### Voraussetzungen

- Python 3.9 oder höher
- pip (Python Package Manager)

### Installation

1. **Repository klonen:**
```bash
git clone https://github.com/xdndbh5h8d-lab/Document-manager.git
cd Document-manager
```

2. **Virtuelle Umgebung erstellen (optional aber empfohlen):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Abhängigkeiten installieren:**
```bash
pip install -r requirements.txt
```

### Starten des Programs

```bash
python main.py
```

Die Anwendung wird sich öffnen und du kannst sofort mit der Verwaltung deiner Dokumente beginnen.

## 📖 Verwendung

### Arbeitsbereiche navigieren
- Links in der Seitenleiste siehst du deine Arbeitsbereiche
- Klicke auf einen Arbeitsbereich um diesen auszuwählen

### Dokumente öffnen
- **Word-Datei öffnen**: Klicke auf "Word öffnen" um eine `.docx` Datei zu laden
- **PDF-Datei öffnen**: Klicke auf "PDF öffnen" um eine `.pdf` Datei zu laden

### Neue Dokumente erstellen
- **Neue Word-Datei**: Klicke auf "Neue Word-Datei" um ein leeres Word-Dokument zu erstellen
- **Neue PDF-Datei**: Klicke auf "Neue PDF-Datei" um ein leeres PDF-Dokument zu erstellen

### Dokumente bearbeiten und speichern
1. Gib deinen Text in den Editor ein
2. Klicke auf "Speichern" um das Dokument zu sichern
3. Wähle einen Speicherort und einen Dateityp aus

## 🛠️ Technologie Stack

| Technologie | Zweck |
|-----------|-------|
| **PyQt6** | Grafische Benutzeroberfläche |
| **python-docx** | Word-Dokumentverarbeitung |
| **PyPDF2** | PDF-Verarbeitung (Lesen) |
| **ReportLab** | PDF-Generierung (Erstellen) |
| **Python** | Programmiersprache |

## 📋 Abhängigkeiten

Alle erforderlichen Pakete sind in `requirements.txt` aufgelistet:

```
PyQt6==6.6.1
python-docx==0.8.11
PyPDF2==3.0.1
reportlab==4.0.7
```

## 🏗️ Projektstruktur

```
Document-manager/
├── main.py                 # Haupteinstiegspunkt der Anwendung
├── requirements.txt        # Python-Abhängigkeiten
├── README.md              # Dieses Dokument
└── .gitignore             # Git-Konfiguration
```

## 🎯 Geplante Features

- [ ] Persistente Speicherung von Arbeitsbereichen
- [ ] Suchfunktion für Dokumente
- [ ] Favoriten-System
- [ ] Tag-System für Dokumentenkategorisierung
- [ ] Zuletzt verwendete Dokumente
- [ ] Dark Mode
- [ ] Export-Optionen (verschiedene Formate)

## 🐛 Bekannte Probleme

Aktuell keine bekannten Probleme. Bitte erstelle ein [Issue](https://github.com/xdndbh5h8d-lab/Document-manager/issues) wenn du ein Problem findest.

## 🤝 Beitragen

Beiträge sind willkommen! So kannst du beitragen:

1. Forke das Projekt
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📜 Lizenz

Dieses Projekt ist aktuell nicht unter einer spezifischen Lizenz lizenziert. Für weitere Informationen siehe [LICENSE](LICENSE) (falls vorhanden).

## 👨‍💻 Autor

**xdndbh5h8d-lab** - [GitHub Profil](https://github.com/xdndbh5h8d-lab)

## 📞 Support & Kontakt

Hast du Fragen oder brauchst Hilfe?

- 📧 Erstelle ein [Issue](https://github.com/xdndbh5h8d-lab/Document-manager/issues)
- 💬 Starte eine [Discussion](https://github.com/xdndbh5h8d-lab/Document-manager/discussions)

## 🙏 Danksagungen

- PyQt6 Team für die großartige GUI-Bibliothek
- python-docx Contributors
- PyPDF2 Maintainer
- ReportLab Team
