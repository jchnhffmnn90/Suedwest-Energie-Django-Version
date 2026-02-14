# Südwest Energie

Moderne Unternehmenswebsite für Energieberatung und -beschaffung, entwickelt mit Django.

## 🚀 Features

*   **Responsive Design:** Optimiert für Desktop, Tablet und Mobile (Bootstrap 5).
*   **Kontaktformular:** Mit E-Mail-Versand und Validierung.
*   **System Status Dashboard:** Interne Überwachung von Datenbank, Serverzeit und Besucherstatistiken (`/status/`).
*   **Besucher-Analytics:** DSGVO-konforme Erfassung von Zugriffen (anonymisierte IP).
*   **SEO-Optimiert:** Semantisches HTML5 und schnelle Ladezeiten.

## 🛠️ Technologie-Stack

*   **Backend:** Python 3.14, Django 6.0
*   **Frontend:** HTML5, CSS3, Bootstrap 5, FontAwesome
*   **Datenbank:** SQLite (Entwicklung), austauschbar durch PostgreSQL
*   **Server:** Gunicorn / Whitenoise (für Static Files)

## 📦 Installation & Entwicklung

### Voraussetzungen
*   Python 3.10+
*   pip

### Setup

1.  **Repository klonen:**
    ```bash
    git clone <repository-url>
    cd suedwest_energie
    ```

2.  **Virtuelle Umgebung erstellen & aktivieren:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    ```

3.  **Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Umgebungsvariablen konfigurieren:**
    Erstelle eine `.env` Datei im Hauptverzeichnis (basierend auf `.env.example`):
    ```bash
    cp .env.example .env
    ```
    Stelle sicher, dass `DJANGO_DEBUG=True` für die lokale Entwicklung gesetzt ist.

5.  **Datenbank migrieren:**
    ```bash
    python manage.py migrate
    ```

6.  **Server starten:**
    ```bash
    python manage.py runserver
    ```
    Die Website ist nun unter `http://127.0.0.1:8000` erreichbar.

## 🔑 Admin & Zugangsdaten

Ein Superuser für den Administrationsbereich (`/admin/`) und die Statusseite (`/status/`) ist vorkonfiguriert (nur für Entwicklung!):

*   **URL:** `/admin/`
*   **User:** `admin`
*   **Passwort:** `adminpassword123`

**Wichtig:** Ändern Sie das Passwort sofort, wenn Sie die Anwendung deployen!

## ✅ Tests

Das Projekt verfügt über eine umfassende Testabdeckung (Views, Forms, Security).

Tests ausführen:
```bash
python manage.py test pages
```

## 🔒 Sicherheitshinweise

*   **Debug Mode:** In der Produktion (`.env`) muss `DJANGO_DEBUG=False` gesetzt werden.
*   **Secret Key:** Generieren Sie einen neuen `DJANGO_SECRET_KEY` für die Produktion.
*   **HTTPS:** In Produktion wird HTTPS durch `SECURE_SSL_REDIRECT=True` erzwungen (automatisch aktiv, wenn Debug=False).

## 📂 Projektstruktur

```
suedwest_energie/
├── manage.py           # Django CLI
├── pages/              # Haupt-App (Views, Models, Tests)
├── static/             # CSS, Bilder, JS
├── templates/          # HTML Templates (Base, Home, etc.)
├── suedwest_project/   # Projekt-Konfiguration (Settings, URLs)
└── requirements.txt    # Python Pakete
```
