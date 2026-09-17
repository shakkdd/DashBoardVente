# 2. Lancer Postgres

On suppose que Docker Desktop est ouvert et prêt (voir [l’étape 1](01-installer-docker-desktop.md)).

## Fichiers du projet

À la racine du projet tu as :

| Fichier | Rôle |
| --- | --- |
| `docker-compose.yml` | Décrit le conteneur Postgres |
| `.env.example` | Modèle des identifiants |
| `.env` | Tes identifiants réels (à créer, ne se met pas sur Git) |

## Créer le fichier `.env`

Dans le terminal, place-toi dans le dossier du projet, puis copie le modèle :

```bash
cp .env.example .env
```

Sous Windows PowerShell :

```powershell
Copy-Item .env.example .env
```

Ouvre `.env` si tu veux changer le mot de passe. Pour un usage local, les valeurs du modèle suffisent.

Ces identifiants sont pour **ta machine uniquement**. Ne les utilise pas en production.

## Démarrer Postgres

Toujours dans le dossier du projet (là où se trouve `docker-compose.yml`) :

```bash
docker compose up -d
```

Que fait cette commande ?

- `docker compose` lit `docker-compose.yml`
- `up` crée et démarre le conteneur
- `-d` le lance en arrière-plan (tu récupères ton terminal)

La première fois, Docker télécharge l’image Postgres 18 (dernière version stable). Ça peut prendre une minute.

## Vérifier que le conteneur tourne

```bash
docker compose ps
```

La colonne *Status* doit indiquer `running` (parfois `healthy` un peu plus tard).

Pour voir les logs :

```bash
docker compose logs db
```

Quand Postgres est prêt, tu vois une ligne proche de :

```text
database system is ready to accept connections
```

## Tester une requête SQL

Cette commande ouvre `psql` (le client SQL) **dans** le conteneur :

```bash
docker compose exec db psql -U postgres -d dashboardvente
```

Tu dois arriver sur un prompt `dashboardvente=#`. Tape :

```sql
SELECT 1;
```

Si tu obtiens `1`, la base répond. Pour quitter :

```sql
\q
```

## Commandes utiles

Arrêter Postgres (les données sont conservées) :

```bash
docker compose stop
```

Le relancer :

```bash
docker compose start
```

Arrêter et supprimer le conteneur (les données restent dans le volume Docker) :

```bash
docker compose down
```

Tout supprimer, **y compris les données** de la base :

```bash
docker compose down -v
```

N’utilise `-v` que si tu veux vraiment repartir de zéro.

## En cas de problème

**Le port 5432 est déjà utilisé**  
Un autre Postgres tourne peut-être sur ta machine. Change `POSTGRES_PORT` dans `.env` (par exemple `5433`), mets à jour `DATABASE_URL` avec le même port, puis relance `docker compose up -d`.

**`docker compose` ne trouve pas le fichier**  
Vérifie que tu es bien dans le dossier du projet (`ls` doit afficher `docker-compose.yml`).

**Le mot de passe est refusé**  
Les identifiants `POSTGRES_*` ne s’appliquent qu’au **premier** démarrage, quand le volume est vide. Si tu as changé le mot de passe après coup, soit tu remets l’ancien, soit tu fais `docker compose down -v` puis `docker compose up -d` (ça efface les données).
