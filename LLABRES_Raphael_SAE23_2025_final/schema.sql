-- DogPedia - SQL Dump
-- Generated for SAE23 project

DROP TABLE IF EXISTS VOTER;
DROP TABLE IF EXISTS Utilisateur;
DROP TABLE IF EXISTS Race;

-- Création de la table Race
CREATE TABLE Race (
    IdRace      TEXT PRIMARY KEY,
    nomRace     TEXT NOT NULL,
    tailleMoy   REAL,
    dureeVie    INTEGER,
    paysOrigine TEXT,
    climat      TEXT,
    description TEXT
);

-- Création de la table Utilisateur
CREATE TABLE Utilisateur (
    idUser      TEXT PRIMARY KEY,
    mail        TEXT NOT NULL,
    age         INTEGER,
    sexe        TEXT,
    pseudo      TEXT,
    idRacePref  TEXT,
    FOREIGN KEY (idRacePref) REFERENCES Race(IdRace) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE
);

-- Création de la table de liaison VOTER
CREATE TABLE VOTER (
    idUser  TEXT NOT NULL,
    IdRace  TEXT NOT NULL,
    PRIMARY KEY (idUser, IdRace),
    FOREIGN KEY (idUser) REFERENCES Utilisateur(idUser) 
        ON DELETE CASCADE,
    FOREIGN KEY (IdRace) REFERENCES Race(IdRace) 
        ON DELETE CASCADE
);

-- Données table Race
INSERT INTO Race VALUES ('qapd3j5', 'Labrador Retriever', 57.0, 12, 'Canada', 'Tempéré', 'Chien de famille.');
INSERT INTO Race VALUES ('d1b2uu6', 'Husky Sibérien', 58.0, 13, 'Russie', 'Froid', 'Chien de traîneau.');
INSERT INTO Race VALUES ('28siks6', 'Chihuahua', 20.0, 15, 'Mexique', 'Chaud', 'Petit chien.');
INSERT INTO Race VALUES ('lvmmc2a', 'Berger Allemand', 63.0, 11, 'Allemagne', 'Tempéré', 'Chien de travail.');

-- Données table Utilisateur
INSERT INTO Utilisateur VALUES ('rj452tz', 'alice@mail.com', 25, 'F', 'Alice', 'qapd3j5');
INSERT INTO Utilisateur VALUES ('r51zucx', 'bob@mail.com', 30, 'M', 'Bob', 'd1b2uu6');
INSERT INTO Utilisateur VALUES ('51vw0zt', 'carol@mail.com', 22, 'F', 'Carol', '28siks6');
INSERT INTO Utilisateur VALUES ('h7ssmqt', 'dave@mail.com', 28, 'M', 'Dave', NULL);
