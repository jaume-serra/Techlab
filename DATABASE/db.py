#!/usr/bin/python
# -*- coding: utf-8 -*-


import sqlite3 as lite

def setup():
    con = lite.connect('intsis.db')
    cur = con.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS USUARI;
    DROP TABLE IF EXISTS TECHLAB;
    DROP TABLE IF EXISTS MAQUINA;
    DROP TABLE IF EXISTS RESERVES;
    DROP TABLE IF EXISTS PERMISOS;
    DROP TABLE IF EXISTS HISTORIAL;
    DROP TABLE IF EXISTS CONFIGMAQUINES;

    CREATE TABLE USUARI
        (
        email CHAR[30] NOT NULL PRIMARY KEY,
        nom CHAR[30] NOT NULL,
        cognom1 CHAR[30] NOT NULL,
        cognom2 CHAR[30],
        pw_hash CHAR[32] NOT NULL, -- Contindrà el hash de la contrasenya de l'usuari. No salt. Sha(256) s'espera.
        rol CHAR[30] NOT NULL,
        id CHAR[8] NOT NULL
	);

    CREATE TABLE TECHLAB
        (id_techlab INTEGER PRIMARY KEY,
        aforament_max INTEGER NOT NULL,
        aforament_actual INTEGER NOT NULL,
        maquines_numero INTEGER NOT NULL,
        maquines_ocupades INTEGER NOT NULL
    );

    CREATE TABLE MAQUINA
        (id_maquina INTEGER NOT NULL,
        nom_maquina CHAR[30] NOT NULL,
        descripcio CHAR[120],
        estat INTEGER NOT NULL, --2 apagada, 3 encesa, 4 fora de servei
        email CHAR[30] NOT NULL,
        calibracio REAL,
        PRIMARY KEY (id_maquina)
    );

    CREATE TABLE RESERVES
        (email CHAR[30] NOT NULL,
        id_maquina INTEGER NOT NULL,
        hora_entrada DATE NOT NULL,
        hora_sortida DATE NOT NULL,
        data DATE NOT NULL,
        reserva_feta INT NOT NULL, --0 RESERVA SENSE ENCARA USUARI 1 RESERVA AMB USUARI, 2 HA ACABAT LA RESERVA
        PRIMARY KEY (email,id_maquina,hora_entrada,data),
        FOREIGN KEY (email) REFERENCES USUARI(email) ON DELETE CASCADE,
        FOREIGN KEY (id_maquina) REFERENCES MAQUINA(id_maquina) ON DELETE CASCADE
    );

    CREATE TABLE PERMISOS
        (email CHAR[30] NOT NULL,
        id_maquina INTEGER NOT NULL,
        permis BOOL NOT NULL,
        utilitzacio BOOL NOT NULL,

        PRIMARY KEY (email, id_maquina),
        FOREIGN KEY (email) REFERENCES USUARI(email) ON DELETE CASCADE,
        FOREIGN KEY (id_maquina) REFERENCES MAQUINA(id_maquina) ON DELETE CASCADE
    );

    CREATE TABLE HISTORIAL
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_maquina INTEGER NOT NULL,
        email CHAR[30] NOT NULL,
        hora_entrada DATE NOT NULL,
        hora_sortida DATE NOT NULL,
        hora_consum DATE NOT NULL,
        data DATE NOT NULL,
        consum INTEGER NOT NULL,
        FOREIGN KEY (id_maquina) REFERENCES MAQUINA(id_maquina) ON DELETE CASCADE,
        FOREIGN KEY (email) REFERENCES USUARI(email) ON DELETE CASCADE

    );

    CREATE TABLE CONFIGMAQUINES
        (nom_maquina CHAR[30] NOT NULL,
        ssid_wifi CHAR[30] NOT NULL,
        pswd_wifi CHAR[30] NOT NULL,
        PRIMARY KEY (nom_maquina)
        );


    PRAGMA foreign_keys = ON;
    INSERT INTO USUARI (email,nom,cognom1,cognom2,pw_hash,rol,id) VALUES ('jaume.serra.badia@estudiantat.upc.edu','Jaume','Serra','Badia','b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79','Administrador',"c6888a9b");
    INSERT INTO USUARI (email,nom,cognom1,cognom2,pw_hash,rol,id) VALUES ('ivan.chamero@estudiantat.upc.edu','Ivan','Chamero','De La Rosa','b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79','Administrador',"bd95aff6");
    INSERT INTO USUARI (email,nom,cognom1,cognom2,pw_hash,rol,id) VALUES ('manuel.angel.roman@estudiantat.upc.edu','Manuel Angel','Roman','Ramos','b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79','Administrador',"86c719bf");
    INSERT INTO USUARI (email,nom,cognom1,cognom2,pw_hash,rol,id) VALUES ('alejandro.prieto@estudiantat.upc.edu','Alejandro','Prieto','Monfort','b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79','Administrador',"4bcbf095");


    INSERT INTO MAQUINA (id_maquina,nom_maquina,descripcio,estat,email,calibracio) VALUES (1,'Maquina1', 'Maquina del laboratori amb tensions molt altes',4,"",0.725);
    INSERT INTO MAQUINA (id_maquina,nom_maquina,descripcio,estat,email) VALUES (2,'Oscil·loscopi', 'Maquina del laboratori amb tensions molt altes',4,"");
    INSERT INTO MAQUINA (id_maquina,nom_maquina,descripcio,estat,email) VALUES (3,'Tester', 'Maquina del laboratori amb tensions molt altes',4,"");
    INSERT INTO MAQUINA (id_maquina,nom_maquina,descripcio,estat,email) VALUES (4,'Pc', 'Maquina del laboratori amb tensions molt altes',4,"");
    INSERT INTO MAQUINA (id_maquina,nom_maquina,descripcio,estat,email) VALUES (5,'Pantalla', 'Maquina del laboratori amb tensions molt altes',4,"");


    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("jaume.serra.badia@estudiantat.upc.edu",1,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("jaume.serra.badia@estudiantat.upc.edu",2,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("jaume.serra.badia@estudiantat.upc.edu",3,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("jaume.serra.badia@estudiantat.upc.edu",4,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("jaume.serra.badia@estudiantat.upc.edu",5,1,1);

    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("ivan.chamero@estudiantat.upc.edu",1,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("ivan.chamero@estudiantat.upc.edu",2,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("ivan.chamero@estudiantat.upc.edu",3,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("ivan.chamero@estudiantat.upc.edu",4,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("ivan.chamero@estudiantat.upc.edu",5,1,1);

    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("manuel.angel.roman@estudiantat.upc.edu",1,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("manuel.angel.roman@estudiantat.upc.edu",2,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("manuel.angel.roman@estudiantat.upc.edu",3,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("manuel.angel.roman@estudiantat.upc.edu",4,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("manuel.angel.roman@estudiantat.upc.edu",5,1,1);

    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("alejandro.prieto@estudiantat.upc.edu",1,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("alejandro.prieto@estudiantat.upc.edu",2,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("alejandro.prieto@estudiantat.upc.edu",3,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("alejandro.prieto@estudiantat.upc.edu",4,1,1);
    INSERT INTO PERMISOS (email, id_maquina,permis,utilitzacio) VALUES ("alejandro.prieto@estudiantat.upc.edu",5,1,1);


    INSERT INTO TECHLAB (id_techlab, aforament_max, aforament_actual, maquines_numero, maquines_ocupades) VALUES (1,30,0,10,0);


    INSERT INTO CONFIGMAQUINES (nom_maquina,ssid_wifi,pswd_wifi) VALUES ("Maquina1","Prieto","12345678");
    INSERT INTO CONFIGMAQUINES (nom_maquina,ssid_wifi,pswd_wifi) VALUES ("Oscil·loscopi","Prieto","12345678");
    INSERT INTO CONFIGMAQUINES (nom_maquina,ssid_wifi,pswd_wifi) VALUES ("Tester","Prieto","12345678");
    INSERT INTO CONFIGMAQUINES (nom_maquina,ssid_wifi,pswd_wifi) VALUES ("Pc","Prieto","12345678");
    INSERT INTO CONFIGMAQUINES (nom_maquina,ssid_wifi,pswd_wifi) VALUES ("Pantalla","Prieto","12345678");

    """)
    con.commit()

setup()
