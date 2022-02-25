DROP TABLE IF EXISTS avis;
DROP TABLE IF EXISTS ligne_de_commande;
DROP TABLE IF EXISTS panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS meubles;
DROP TABLE IF EXISTS materiaux;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS types_meubles;
DROP TABLE IF EXISTS fourniseur;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS etat;

CREATE TABLE IF NOT EXISTS types_meubles (
    id_type             INT UNSIGNED AUTO_INCREMENT,
    libelle_type        VARCHAR(50),
    PRIMARY KEY (id_type)
);

CREATE TABLE IF NOT EXISTS couleur (
    id_couleur         INT UNSIGNED AUTO_INCREMENT,
    libelle_couleur    VARCHAR (50),
    PRIMARY KEY (id_couleur)
);

CREATE TABLE IF NOT EXISTS materiaux (
    id_materiaux        INT UNSIGNED AUTO_INCREMENT,
    libelle_materiaux   VARCHAR(50),
    PRIMARY KEY (id_materiaux)
);

CREATE TABLE IF NOT EXISTS fourniseur(
   id_Fourniseur        INT UNSIGNED AUTO_INCREMENT,
   libelle_Fourniseur   VARCHAR(50),
   PRIMARY KEY(id_Fourniseur)
);

CREATE TABLE IF NOT EXISTS user (
    id_User             INT UNSIGNED AUTO_INCREMENT,
    username            VARCHAR(25),
    password            VARCHAR (255),
    role                VARCHAR (25),
    est_actif           VARCHAR (1),
    email               VARCHAR(50),
    PRIMARY KEY (id_User)
);

CREATE TABLE IF NOT EXISTS etat(
   id_etat              INT UNSIGNED AUTO_INCREMENT,
   libelle_etat         VARCHAR(50),
   PRIMARY KEY(id_etat)
);

CREATE TABLE IF NOT EXISTS meubles(
    id_meuble           INT UNSIGNED AUTO_INCREMENT,
    nom                 VARCHAR(50),
    prix                NUMERIC(12,2),
    dateFabrication     DATE,
    id_MeubleCouleur    INT UNSIGNED,
    id_MeubleMateriaux  INT UNSIGNED,
    id_MeubleType       INT UNSIGNED,
    id_MeubleFourniseur INT UNSIGNED,
    nbStock             INT,
    image               VARCHAR(255),
    PRIMARY KEY (id_meuble),
    CONSTRAINT fk_MeubleCouleur 
        FOREIGN KEY (id_MeubleCouleur) REFERENCES couleur(id_couleur) ON DELETE CASCADE,
    CONSTRAINT fk_MeubleMateriaux 
        FOREIGN KEY (id_MeubleMateriaux) REFERENCES materiaux(id_materiaux) ON DELETE CASCADE,
    CONSTRAINT fk_MeubleType 
        FOREIGN KEY (id_MeubleType) REFERENCES types_meubles(id_type) ON DELETE CASCADE,
    CONSTRAINT fk_MeubleFournisseur 
        FOREIGN KEY(id_MeubleFourniseur) REFERENCES fourniseur(id_Fourniseur) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS commande(
   id_cmd           INT UNSIGNED AUTO_INCREMENT,
   date_achat       DATE,
   id_CmdEtat       INT UNSIGNED,
   id_CmdUser       INT UNSIGNED,
   PRIMARY KEY(id_cmd),
   CONSTRAINT fk_CommandeEtat
       FOREIGN KEY(id_CmdEtat) REFERENCES etat(id_etat),
   CONSTRAINT fk_CommandeUser
       FOREIGN KEY(id_CmdUser) REFERENCES user(id_User)
);

CREATE TABLE IF NOT EXISTS panier(
   id_ajout         INT UNSIGNED AUTO_INCREMENT,
   date_ajout       DATE,
   panier_quantite         INT,
   id_PanierUser    INT UNSIGNED,
   id_PanierMeuble  INT UNSIGNED,
   PRIMARY KEY(id_ajout),
   CONSTRAINT fk_idPanierUser
       FOREIGN KEY(id_PanierUser) REFERENCES user(id_User) ON DELETE CASCADE,
   CONSTRAINT fk_idPanierMeuble
       FOREIGN KEY(id_PanierMeuble) REFERENCES meubles(id_meuble) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ligne_de_commande(
   id_LigneMeuble   INT UNSIGNED,
   id_LigneCmd      INT UNSIGNED,
   prix_unit        NUMERIC(12,2),
   quantite         INT,
   PRIMARY KEY(id_LigneMeuble, id_LigneCmd),
   CONSTRAINT fk_idLigneMeuble
       FOREIGN KEY(id_LigneMeuble) REFERENCES meubles(id_meuble),
   CONSTRAINT fk_idLigneCmd
       FOREIGN KEY(id_LigneCmd) REFERENCES commande(id_cmd)
);

CREATE TABLE IF NOT EXISTS avis(
    id_avis                     INT UNSIGNED AUTO_INCREMENT,
    libelle_avis                varchar(500),
    note                        NUMERIC(2,1),
    id_AvisUser                 INT UNSIGNED,
    id_AvisMeuble               INT UNSIGNED,
    PRIMARY KEY (id_avis),
    CONSTRAINT fk_id_AvisUser FOREIGN KEY (id_AvisUser) REFERENCES user(id_User),
    CONSTRAINT fk_id_AvisMeuble FOREIGN KEY (id_AvisMeuble) REFERENCES meubles(id_meuble)
);


INSERT INTO types_meubles (libelle_type) VALUES
    ('canape'),
    ('lit'),
    ('commode'),
    ('armoire'),
    ('table'),
    ('cabinet');
SELECT * FROM types_meubles;

INSERT INTO couleur(libelle_couleur) VALUES
    ('rouge'),
    ('vert'),
    ('jaune'),
    ('bleu'),
    ('ebene'),
    ('magenta'),
    ('violet'),
    ('gris'),
    ('satin');
SELECT * FROM couleur;

INSERT INTO materiaux(libelle_materiaux) VALUES
    ('bois'),
    ('acier'),
    ('verre'),
    ('aluminium'),
    ('marbre'),
    ('porcelaine');
SELECT * FROM materiaux;

INSERT INTO fourniseur (libelle_Fourniseur) VALUES
    ('ikea'),
    ('Lapeyre'),
    ('But'),
    ('Conforama'),
    ('Alinea'),
    ('Roche Bobois'),
    ('PerrotConception');

INSERT INTO user (username, password, role, est_actif, email) VALUES
    ('admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1, 'admin@admin.fr'),
    ('client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client', 1, 'client@client.fr'),
    ('client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client', 1, 'client2@client2.fr'),
    ('Mafuo', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client', 1, 'Mafuo@gmail.com');

INSERT INTO etat (libelle_etat) VALUES
    ('en attente'),
    ('expedier'),
    ('valider'),
    ('confirmer');

INSERT INTO meubles (nom,prix,dateFabrication,id_MeubleCouleur,id_MeubleMateriaux,id_MeubleType,id_MeubleFourniseur,nbStock,image) VALUES
    ('klippan', '50.20', '2020-06-06', 1, 1, 1, 3, 10, 'klippan.png'),
    ('malm', '12.00', '2020-06-06', 2, 2, 2, 5, 100, 'malm.png'),
    ('besta', '14.36', '2020-06-06', 3, 1, 3, 6, 50, 'besta.jpg'),
    ('billy', '24.59', '2020-06-06', 4, 3, 4, 2, 75, 'billy.png'),
    ('friheten', '42.21', '2020-06-06', 5, 2, 1, 5, 25, 'friheten.png'),
    ('brimnes', '11.11', '2019-06-06', 6, 4, 2, 5, 50, 'brimnes.png'),
    ('la commode du luxe', '35.21', '2019-06-06', 7, 5, 3, 1, 0,'commodeLuxe.jpg'),
    ('lack', '32.25', '2019-12-06', 8, 2, 4, 7, 1,'lack.png'),
    ('toilette','800','2020-12-15',9, 6, 6, 3, 5, 'toilette.jpg'),
    ('vilme', '52.36', '2019-12-26', 9, 1, 1, 4, 80, 'vilme.png');

INSERT INTO commande (date_achat, id_CmdEtat, id_CmdUser) VALUES
    ('2003-01-01',4,4),
    ('2015-08-15',2,2),
    ('2020-07-20',3,3),
    ('2021-02-01',1,4);

INSERT INTO panier (date_ajout, panier_quantite, id_PanierUser, id_PanierMeuble) VALUES
    ('2003-01-01',2,4,8),
    ('2015-08-15',5,2,1),
    ('2020-07-20',10,3,5),
    ('2021-02-01',1,1,3);

INSERT INTO ligne_de_commande (id_LigneMeuble, id_LigneCmd, prix_unit, quantite) VALUES
    (8,1,'800',2),
    (3,2,'14.36',1),
    (1,3,'50.20',2),
    (9,4,'52.36',5);

INSERT INTO avis(libelle_avis, note, id_AvisUser, id_AvisMeuble) VALUES
    ('Très contente de ce produit, la qualité est au rendez-vous pour un prix dérisoire.', '4.8', 2, 1);

select * from avis;

/*select nom,prix,dateFabrication,C.libelle_couleur,M.libelle_materiaux,T.libelle_type,nbStock,image
from meubles
inner join couleur C on C.id_couleur = id_MeubleCouleur
inner join materiaux M on M.id_materiaux = id_MeubleMateriaux
inner join types_meubles T on T.id_type = id_MeubleType
order by nom;*/