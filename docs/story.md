# Story

## Intro
1. Problemstellung: innovative Kfz-Versicherungsgesellschaft
1. Ausgangspunkt mit Colab: notebooks/exploration.ipynb
   1. Features
   1. Was wollen wir vorhersagen?
   1. Tests, Training, 
1. Modelle vergammeln in Prod, Grafiken dazu
1. Wann sollte man ein neues Modell bringen?


## Monitoring

### Hands-On: Produktion simulieren
1. Projekt auf Gitpod mit dem Link im Readme des Repos starten: https://gitpod.io/#https://github.com/DJCordhose/mlops-drift
1. Gestartete Services inspizieren
   1. Die App auf Port 8080
      1. Einen Request über die Swagger API abfeuern
      1. Einen Request über ein curl
      1. /metrics 
   1. Prometheus auf Port 9090
   1. Grafana auf Port 3000
   1. `./scripts/curl-drift.sh <URL app server>`

1. Drift auf Gitpod dauert echt lange
   - Ein Jahr nach ca. 20 min durch
   - Drift nach ca. 20-25 min getektiert
1. Drift in der Reihenfolge 
   1. miles (ca. 15 min auf Gitpod)
   1. emergency_braking (ca. 18 min auf Gitpod)
   1. age (ca. 20 min auf Gitpod)

   1. Story:
     1. die Performance des Modells degradiert
	  1. aber wir haben erst nach Jahren eine Ground Truth, die uns das anhand der Metrik zeigt
	  1. wir simulieren 3 Jahre Betrieb mit
         1. Leute werden immer Älter, das passiert aber langsam (age)
	     1. Es wird immer weniger Auto gefahren, Leute steigen um auf die Bahn und öffentliche Verkehrsmittel (miles)
	     1. Die Sicherheit der Autos wird immer besser und der Einfluss der individuellen Fahrleistung wird verringert (emergency_braking, pred)  



# TODO
1. Kann man noch die Vorhersage mit in den Drift nehmen?
1. Gibt es mehr sinnvolle Hands-On-Teile?
1. Was tut man wenn man den Verdacht hat, dass das Modell nicht mehr passt?