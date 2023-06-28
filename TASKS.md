## Hands-On 1 Docker Installation überprüfen oder herstellen

Helft bitte euren Nachbarn, falls eure Installation schon läuft

1. Wir empfehlen: arbeitet zusammen mit euren direkten Nachbarn
1. Stellt sicher, dass zumindest einer eurer Rechner eine lauffähige Installation hat 
1. Sagt kurz Hallo
1. Installieren (falls noch nicht passiert)
   1. Git : https://git-scm.com/downloads
   1. Docker: https://docs.docker.com/get-docker/
1. Beispiel-Image ausführen
    * `docker run -it -p 8088:80 --name welcome-to-docker docker/welcome-to-docker`
1. Nachdem Docker den Container gestartet hat überprüfen, folgendes im Browser aufrufen: http://localhost:8088/

## Hands-On 2 Projekt vorbereiten

1. Installieren (falls noch nicht passiert)
   1. Git : https://git-scm.com/downloads
1. Projekt klonen
   * https://github.com/openknowledge/mlops-m3
   * `git clone git@github.com:openknowledge/mlops-m3.git`
1. Docker images bauen
   * Im Projekt-Verzeichnis unter `insurance-prediction`:
     * `docker build -t insurance_prediction_interactive -f interactive.Dockerfile .`
     * `docker build -t insurance-prediction .`
   * Das kann (gerade bei überlastetem Netz) lange dauern
   * Wir müssen jetzt noch nicht bis zum Abschluss warten 

## Hands-On 3 Training und Validierung

* Entwicklungsumgebung über Docker starten

```sh
cd insurance-prediction
```

```
# Linux/Mac/WSL-Shell
docker run -v "$(pwd)/output:/output" --rm -it insurance_prediction_interactive

# Windows-Cmd
docker run -v "%cd%/output:/output" --rm -it insurance_prediction_interactive

# Powershell
docker run -v "$(Get-Location)/output:/output" --rm -it insurance_prediction_interactive
```

*Aufgabe:* Was ist passiert, was ist zu sehen?

## Hands-On 4 Training und Validierung

* Training und Validierung im interaktiven Container durchführen

```
poetry run train --dataset ./datasets/insurance_prediction --model /output/model.h5
poetry run validate --dataset ./datasets/insurance_prediction/ --model /output/model.h5
```
## Hands-On 5 Wie wollen wir das Modell validieren?

* bei automatisiertem Training können wir ein erfolgreiches Training nicht mehr manuell überwachen
* wie könnten automatisierte Tests auf dem Modell aussehen?
* Diskutiert mit euren Nachbarn und schreibt eure Vorschläge auf
* Inspiration: https://storage.googleapis.com/pub-tools-public-publication-data/pdf/45742.pdf


### Hands-On 6 ML-Service

```sh
cd insurance-prediction

docker run --rm -p 8080:80 insurance-prediction
```

*Aufgabe 1:* Was ist im dazugehörigen Dockerfile passiert? 

*Aufgabe 2:* Rufe `http://localhost:8080/` im Browser auf

*Aufgabe 3:* Führe dort eine Prediction durch


