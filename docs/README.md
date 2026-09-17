# Documentation Postgres + Docker

Ce dossier explique, étape par étape, comment installer Docker, lancer Postgres, puis le relier à FastAPI.

Tu n’as pas besoin de tout connaître. Suis les fichiers dans l’ordre :

1. [Installer Docker Desktop](01-installer-docker-desktop.md)
2. [Lancer Postgres](02-lancer-postgres.md)
3. [Relier FastAPI à Postgres](03-connecter-fastapi.md)

## Pourquoi pas de Dockerfile ?

Un Dockerfile sert à **construire** une image (par exemple ton application Python).

Ici, on utilise seulement Postgres. L’image officielle existe déjà, donc un fichier `docker-compose.yml` suffit : il dit à Docker « prends Postgres et lance-le avec ces réglages ».
