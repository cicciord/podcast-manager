# podcast-manager

Progetto d'esame per "Introduzione alle Applicazioni Web" @ Politecnico di Torino

## Target dispositivi

Questa applicazione web è stata sviluppata per essere eseguita su desktop. Sarà comunque eseguibile, anche se non progettata appositamente per questi dispositivi, su tablet e smartphone

# Getting Started

## Pre-requisiti

Per il corretto funzionamento di questa repository è necessario avere installato sul dispositivo `Python 3.10.2` o superiore (versioni precedenti potrebbero funzionare ugualmente)

Per seguire le istruzioni successive è necessario eseguire i comandi elencati da terminale.
Assicuratevi di essere nella directory del progetto

## Virtual enviroment

Per iniziare creare un virtual enviroment di python. Per farlo è necessario eseguire il comando

```
python3 -m venv venv
```

Dopo che la cartella `venv` è stata creata nella repository eseguire il seguente comando per attivare il virtual enviroment

```
. venv/bin/activate
```

## Intallare le dipendenze

Assicurarsi che il file `requirements.txt` è presente nella repository ed eseguire

```
pip install -r requirements.txt
```

## Server

Per avviare il server è necessario eseguire il seguente comando

```
flask run
```

per avviare il server in modalità debug aggiungere `--debug` prima di `run`; aggiungere dopo `run` per rendere il server visibile esternamente `--host=0.0.0.0`; se si intende avviare il server su una porta personalizzata e non utilizzare la porta di default (5000) `--port=3000`

Si puo anche avviare il server in maniera alternativa eseguendo

```
python3 app.py
```

Questo comando avvierà il server il modalità debug sulla porta 3000

## Credenziali utenti

Sono presenti già due utenti registrati che potranno essere usati per testare l'applicazione

- Creatore:
  - email: creator@email.com
  - password: password_creator
- Ascoltatore:
  - email: listener@email.com
  - password: password_listener

## Materiale di prova

All'interno del progetto è presente una cartella chiamata **_sample_assets_** al cui interno è possibile trovare materiale extra per creare nuovi contenuti
