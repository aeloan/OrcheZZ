# Orchezz

Projet nommé Orchezz réalisé dans le cadre du cours de Programmation Réseau Sécurisée

Trois niveaux : 
Musique + Partition avec nom note
Que la partition sans aide de note
Que la musique => Oreille musicale

Filtres : 
Musique classique
Musique rock
Musique jeu vidéo
Musique animé
…

Trois difficultés : 
Notes qui se suivent
Notes disjointes
Accords

On se connecte à une salle avec d’autres gens
La partie commence
A chaque fois => une partition est envoyé
Le client doit le jouer et la piste est envoyé (on lui laisse peu de temps)
Le serveur vérifie puis joue toutes les pistes en même temps

Il faut un maitre du jeu (lancer la partie, choisir les filtres, créer la salle, …)


## Installation et lancement

Le projet a été développé sous Windows, il n'a jamais été testé sur d'autres OS.
Cette documentation va donc se concentrer sur une installation sur cet OS.

## 1. Prérequis

```bash
winget install "FFmpeg (Essentials Build)"
```

## 2. Créer l'environnement virtuel

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1 
```

## 3. Installer les dépendances

```bash
cd back && pip install -r requirements.txt
cd ../front && pip install -r requirements.txt
cd ..
```

## 4. Lancer Orchezz

Pour lancer ce jeu, vous aurez besoin de lancer deux terminaux.
Il ne faudra pas les fermer avant la fin de la partie.

**Terminal 1 - Backend :**
```bash
cd back
python main.py
```

**Terminal 2 - Frontend :**
```bash
cd front
python app.py
```

**Navigateur :**
```
http://localhost:5000
```


## Auteurs
Eloan ANDRE et Anna BOUDOUL (FISA2)

