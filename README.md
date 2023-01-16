# podcast-manager

Progetto d'esame per "Introduzione alle Applicazioni Web" @ Politecnico di Torino

## Target dispositivi

Questa applicazione web è stata sviluppata per essere eseguita su desktop. Sarà comunque eseguibile, anche se non progettata appositamente per questi dispositivi, su tablet e smartphone

# Getting Started

## Pre-requisiti

Per eseguire questa repository è necessario avere installato sul dispositivo `Python 3.10.2` (versioni precedenti potrebbero funzionare ugualmente)

## Server

Per avviare il server è necessario eseguire il seguente comando da terminale.
Assicuratevi di essere nella directory del progetto prima di eseguire il comando

```
flask run
```

per avviare il server in modalità debug aggiungere `--debug` prima di `run`; per rendere il server visibile esternamente aggiungere invece `--host=0.0.0.0`; se si intende avviare il server su una porta personalizzata e non utilizzare la porta di default (5000) `--port=3000`

Si puo anche avviare il server in maniera alternativa eseguendo

```
python3 app.py
```

Questo comando avvierà il server il modalità debug sulla porta 3000
