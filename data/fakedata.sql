-- ============================================================
-- NordCommerce - Script de création et peuplement de la BDD
-- PostgreSQL
-- ============================================================

DROP TABLE IF EXISTS ventes CASCADE;
DROP TABLE IF EXISTS vendeurs CASCADE;
DROP TABLE IF EXISTS produits CASCADE;
DROP TABLE IF EXISTS regions CASCADE;

-- ============================================================
-- Tables
-- ============================================================

CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE produits (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    categorie VARCHAR(50) NOT NULL,
    prix_unitaire NUMERIC(10, 2) NOT NULL CHECK (prix_unitaire > 0)
);

CREATE TABLE vendeurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    region_id INTEGER NOT NULL REFERENCES regions(id)
);

CREATE TABLE ventes (
    id SERIAL PRIMARY KEY,
    date_vente DATE NOT NULL,
    vendeur_id INTEGER NOT NULL REFERENCES vendeurs(id),
    produit_id INTEGER NOT NULL REFERENCES produits(id),
    quantite INTEGER NOT NULL CHECK (quantite > 0),
    montant_total NUMERIC(10, 2) NOT NULL CHECK (montant_total >= 0)
);

-- ============================================================
-- Régions
-- ============================================================

INSERT INTO regions (nom) VALUES
    ('Hauts-de-France'),
    ('Île-de-France'),
    ('Auvergne-Rhône-Alpes'),
    ('Nouvelle-Aquitaine'),
    ('Occitanie'),
    ('Bretagne'),
    ('Grand Est');

-- ============================================================
-- Produits
-- ============================================================

INSERT INTO produits (nom, categorie, prix_unitaire) VALUES
    ('Clavier mécanique', 'Informatique', 79.90),
    ('Souris sans fil', 'Informatique', 29.90),
    ('Écran 27 pouces', 'Informatique', 199.00),
    ('Casque audio', 'Audio', 59.90),
    ('Enceinte Bluetooth', 'Audio', 45.00),
    ('Chaise de bureau', 'Mobilier', 149.00),
    ('Bureau réglable', 'Mobilier', 289.00),
    ('Lampe de bureau LED', 'Mobilier', 34.90),
    ('Webcam HD', 'Informatique', 39.90),
    ('Disque SSD externe', 'Informatique', 89.00),
    ('Tapis de souris XXL', 'Accessoires', 14.90),
    ('Support ordinateur portable', 'Accessoires', 24.90);

-- ============================================================
-- Vendeurs (répartis dans les régions)
-- ============================================================

INSERT INTO vendeurs (nom, region_id) VALUES
    ('Camille Dubois', 1),
    ('Lucas Martin', 1),
    ('Sarah Bernard', 2),
    ('Nicolas Petit', 2),
    ('Julie Moreau', 3),
    ('Thomas Leroy', 3),
    ('Emma Simon', 4),
    ('Hugo Laurent', 4),
    ('Chloé Michel', 5),
    ('Maxime Garcia', 5),
    ('Léa Roux', 6),
    ('Antoine David', 7);

-- ============================================================
-- Ventes : génération aléatoire sur les 12 derniers mois
-- ============================================================

-- NB : on tire les IDs par arithmétique directement dans le SELECT (et non via
-- une sous-requête "ORDER BY random() LIMIT 1" en LATERAL). Cette dernière
-- n'étant pas corrélée à la ligne externe, PostgreSQL est libre de la
-- matérialiser une seule fois et de réutiliser le même résultat pour toutes
-- les lignes générées (même vendeur/produit partout) : c'est un piège classique.
INSERT INTO ventes (date_vente, vendeur_id, produit_id, quantite, montant_total)
SELECT
    (CURRENT_DATE - (random() * 365)::int) AS date_vente,
    t.vendeur_id,
    t.produit_id,
    t.quantite,
    ROUND((t.quantite * p.prix_unitaire)::numeric, 2) AS montant_total
FROM (
    SELECT
        (1 + floor(random() * (SELECT COUNT(*) FROM vendeurs)))::int AS vendeur_id,
        (1 + floor(random() * (SELECT COUNT(*) FROM produits)))::int AS produit_id,
        (1 + floor(random() * 5))::int AS quantite
    FROM generate_series(1, 800)
) AS t
JOIN produits p ON p.id = t.produit_id;

-- ============================================================
-- Vérification rapide
-- ============================================================

-- SELECT COUNT(*) FROM ventes;
-- SELECT r.nom, SUM(ve.montant_total) AS ca
-- FROM ventes ve
-- JOIN vendeurs v ON v.id = ve.vendeur_id
-- JOIN regions r ON r.id = v.region_id
-- GROUP BY r.nom
-- ORDER BY ca DESC;
