# 1. Installer Docker Desktop

Docker permet de lancer des programmes (ici Postgres) dans un **conteneur** : une mini-machine isolée, déjà configurée. Tu n’installes pas Postgres sur ton Mac ou ton PC : Docker s’en occupe.

Docker Desktop est l’application qui fait tourner Docker sur ton ordinateur.

## Prérequis

- macOS récent, ou Windows 10/11
- au moins 4 Go de RAM
- une connexion internet pour télécharger Docker, puis l’image Postgres

## macOS

1. Va sur la page d’installation : [Install Docker Desktop on Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
2. Télécharge le bon fichier :
   - Mac **Apple silicon** (M1, M2, M3, M4) : bouton *Apple silicon*
   - Mac **Intel** : bouton *Intel chip*
3. Ouvre le fichier `Docker.dmg`
4. Glisse l’icône Docker dans le dossier **Applications**
5. Ouvre **Docker** depuis Applications
6. Accepte les conditions, puis choisis **Use recommended settings**
7. Attends que l’icône Docker (une baleine) dans la barre de menu soit **stable** : Docker est prêt

Pour savoir si tu as un Mac Apple silicon ou Intel : menu Pomme → **À propos de ce Mac**. Si tu vois « Puce Apple », c’est Apple silicon.

## Windows

1. Va sur la page d’installation : [Install Docker Desktop on Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
2. Télécharge **Docker Desktop Installer.exe**
3. Lance l’installateur et suis les étapes (laisse les options par défaut)
4. Redémarre l’ordinateur si l’installateur le demande
5. Ouvre **Docker Desktop**
6. Accepte les conditions et attends que Docker indique qu’il est en cours d’exécution

Si Windows propose d’activer WSL 2, accepte : Docker en a besoin.

## Vérifier que ça marche

Ouvre un terminal (Terminal sur Mac, PowerShell sur Windows) et tape :

```bash
docker version
```

Tu dois voir des informations sur le *Client* et le *Server*. Si le *Server* affiche une erreur, Docker Desktop n’est pas encore démarré : ouvre l’application et réessaie.

Ensuite :

```bash
docker compose version
```

Tu dois voir un numéro de version. C’est la commande qu’on utilisera pour lancer Postgres.
