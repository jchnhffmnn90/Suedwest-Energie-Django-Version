# Release Notes - Version 0.0.1

**Datum:** 14. Februar 2026
**Status:** Initial Beta Release

Dies ist die erste Version der Unternehmenswebsite für Südwest Energie.

## 🚀 Neue Funktionen

### Frontend & Design
*   **Modernes UI:** Responsives Design basierend auf Bootstrap 5 mit angepasstem Farbschema (Slate/Emerald).
*   **Seitenstruktur:** Startseite, Über uns, Leistungen (mit 7 Fachgebieten), Ablauf, Kontakt.
*   **Kontaktformular:** Voll funktionsfähiges Formular mit Validierung und E-Mail-Versand (Console Backend für Dev).
*   **Mobile Optimierung:** Angepasste Navigation und Layouts für Smartphones und Tablets.

### Backend & Features
*   **System Status Dashboard:** Interne Überwachung (`/status/`) für Datenbank-Status, Debug-Modus und Git-Revision.
*   **Besucher-Analytics:** Integrierte, DSGVO-konforme Statistik (Anonymisierte IPs) zur Erfassung von Seitenaufrufen.
*   **Health Check:** API-Endpoint (`/health/`) für Monitoring-Tools.

### Technik & Qualität
*   **Tech Stack:** Update auf Python 3.14 und Django 6.0.2.
*   **Testabdeckung:** Umfassende Unit-Tests für Views, Formulare, Utilities und Security (Status-Page Schutz).
*   **Performance:** Datenbank-Indizierung für Statistik-Abfragen implementiert.
*   **Sicherheit:** Vorbereitung für HTTPS (lokal via `runserver_plus` möglich, Production-Settings vorbereitet).

## 🐛 Bekannte Einschränkungen (Dev)
*   Lokaler Server läuft standardmäßig auf HTTP (Port 8080 empfohlen, um HSTS-Probleme zu vermeiden).
*   E-Mails werden im Development-Modus nur in der Konsole ausgegeben.

## 📦 Installation
Siehe `README.md` für detaillierte Installationsanweisungen.
