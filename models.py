
# coding: utf-8
# #!/usr/bin/python


import sqlite3
import hashlib # sha256() returns a SHA-256 object. hexdigest() returns data in hexa format.
import datetime
import random
import string
database ="/home/manu/Documentos/INT-SIS/is-ivan-alejandro-manu/FlaskApp/DATABASE/intsis.db"

###Funcions generiques admin i user
def check_email(u_email):
    """
    Retorna True si u_email existeix a Usuari

    Parameters
    --------
    u_email : str
        email de l'usuari
    """

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT email FROM USUARI WHERE email = (?)", (u_email,))
    email = cur.fetchall()
    conn.close()
    if email == []:
        return False
    else:
        return True


def check_password(u_email,u_password):
    """
    Retorna True si la pw_hash del usuari amb correu u_email es igual que la u_password
    TODO: millor passar la password amb hash ja?

    Parameters
    --------
    u_email : str
        email de l'usuari
    u_password: str
        password de l'usuari sense hash
    """

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT pw_hash FROM USUARI WHERE email = (?)", (u_email,))
    password = cur.fetchone()
    conn.close()
    password_hash = hashlib.sha256(str(u_password).encode('utf-8')).hexdigest()
    if(password[0] == password_hash):
        return True
    else:
        return False


def get_rol(u_email):
    """
    Retorna el rol de l'usuari amb email -> u_email

    Parameters
    --------
    u_email : str
        email de l'usuari
    """

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT rol FROM USUARI WHERE email = (?)", (u_email,))
    rol = cur.fetchone()
    conn.close()
    return rol[0]


def get_name(u_email):
    """
    Retorna el nom de l'usuari amb email -> u_email

    Parameters
    --------
    u_email : str
        email de l'usuari
    """

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT nom FROM USUARI WHERE email = (?)", (u_email,))
    username = cur.fetchone()
    conn.close()
    return username[0]


def get_nameComplete(u_email):
    """
    Retorna el nom de l'usuari amb email -> u_email

    Parameters
    --------
    u_email : str
        email de l'usuari
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("SELECT nom, cognom1, cognom2 FROM USUARI WHERE email = (?)", (u_email,))
        username = cur.fetchone()
        conn.close()
        return username

    except Exception as e:
        print (e)
        return -1


def get_user_name(u_email):
    """
    Retorna una llista amb el nom, cognom1 i cognom2 de l'usuari amb email -> u_email

    Parameters
    --------
    u_email : str
        email de l'usuari
    """
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT nom,cognom1,cognom2 FROM USUARI WHERE email = (?)", (u_email,))
    user = cur.fetchone()
    conn.close()
    return user


def check_date(u_data,u_data_inici,u_data_final):
    """
    Retrona True si la u_data + u_data_inici és més gran o igual a la data actual i si la u_data_final és més gran que la data u_data_inici

    Parameters
    --------
    u_data : str
        data en format %Y-%m-%d
    u_data_inici: str
        data en format %H:%M
    u_data_final: str
        data en format %H:%M
    """

    data = u_data +" "+u_data_inici
    data = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M")
    hora_in = datetime.datetime.strptime(u_data_inici, "%H:%M")
    hora_out = datetime.datetime.strptime(u_data_final, "%H:%M")

    if(datetime.datetime.now() <= data and hora_out >= hora_in):
        return True
    else:
        return False

def update_email(old_email,new_email):
    """
    Update old_email per new_email

    Parameters
    --------
    old_email : str
        email de l'usuari antic
    new_email: str
        email de l'usuari nou
    """

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("UPDATE USUARI SET email = (?) WHERE email = (?)", (new_email,old_email))
    conn.commit()
    conn.close()
    return

def update_password(u_email, new_password):
    """
    Update passwor de l'usuari

    Parameters
    --------
    u_email : str
        email de l'usuari
    new_password: str
        password nova de l'usuari
    """

    password_hash = hashlib.sha256(str(new_password).encode('utf-8')).hexdigest()
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("UPDATE USUARI SET pw_hash = (?)  WHERE email = (?)", (password_hash,u_email,))
    conn.commit()
    conn.close()
    return


def check_reserve(maquina_id,date,time_in,time_out):
    """
    Retorna True si ja esta reservat
    Parameters
    --------
    maquina_id : str
        id de la maquina a reservar
    date : str
        data en format %Y-%m-%d
    time_in: str
        data en format %H:%M
    time_out: str
        data en format %H:%M
    """

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT email FROM RESERVES WHERE  id_maquina = (?) AND data = (?) AND ((hora_entrada >= (?) AND hora_entrada <= (?)) OR (hora_sortida >= (?) AND hora_sortida <= (?)) OR (hora_entrada <= (?) AND hora_sortida >= (?))  )", (maquina_id,date,time_in,time_out,time_in,time_out,time_in,time_out))
    email_user = cur.fetchone()
    conn.close()
    if(email_user == None):
        return True
    else:
        return False


def reserve(email,date,time_in,time_out,maquina_id):
    """
    Insereix a la taula reserves una reserva nova amb els parametres

    Parameters
    --------
    email : str
        email de l'usuari
    date : str
        data en format %Y-%m-%d
    time_in: str
        data en format %H:%M
    time_out: str
        data en format %H:%M
    maquina_id:
        identificador de la màquina
    """

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("INSERT INTO RESERVES (email,id_maquina,hora_entrada,hora_sortida,data,reserva_feta) VALUES ((?),(?),(?),(?),(?),0)", (email,maquina_id,time_in,time_out,date,))
    conn.commit()
    conn.close()
    return


def get_reserve(user,data_inici,data_final):
    """
    Retorna una llista amb totes les reserves entre data_inici i data_final de lusuari. Si lusuari es None retorna tots els usuaris

    Parameters
    --------
    user: str o None
        email de lusuari
    data_inici : str
        data inici de reserva format %YYYY-%mm-%dd
    data_inici : str
        data final de reserva format %YYYY-%mm-%dd
    """

    conn = sqlite3.connect(database)
    cur = conn.cursor()

    if(user == None): #Historial de tots els usuaris entre data_inici i data_fi
        cur.execute("SELECT data, hora_entrada, hora_sortida, email, id_maquina FROM RESERVES WHERE data >= (?) AND data <= (?) ORDER BY hora_entrada ASC ", (data_inici,data_final,))

    elif (data_inici == None or data_final == None): #Historial complert del user
        cur.execute("SELECT data, hora_entrada, hora_sortida, email, id_maquina FROM RESERVES WHERE email = (?)", (user,))

    else: #Historial del user entre data_inici i data_fi
        cur.execute("SELECT data, hora_entrada, hora_sortida, email, id_maquina FROM RESERVES WHERE data >= (?) AND data <= (?) AND email = (?)", (data_inici,data_final,user,))

    reserves = cur.fetchall()
    items = []
    for reserva in reserves:
        item =  [datetime.datetime.strptime(reserva[0],"%Y-%m-%d").strftime("%d-%m-%y")] + list(reserva[1:4]) + [get_maquina_name(reserva[4])]
        items += [item]
    conn.close()
    return items


def cancel_reserve(maquina_id,date,time):
    """
    Elimina la reserva de l'usuari
    """
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT email FROM RESERVES WHERE id_maquina=(?) AND data = (?) AND (hora_entrada <= (?) AND hora_sortida >= (?))",(maquina_id,date,time,time,))
    user = cur.fetchone()[0]
    cur.execute("DELETE FROM RESERVES WHERE id_maquina = (?) AND data = (?) AND (hora_entrada <= (?) AND hora_sortida >= (?))",(maquina_id,date,time,time,))
    conn.commit()
    conn.close()
    return user


def add_permision(user,id_maquina,type):
    """
    Parametres user, id_maquina, permis/utilització
    """
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    if(user == "Tots"):
        if(type == "utilitzacio"):
            cur.execute("UPDATE PERMISOS SET utilitzacio = TRUE WHERE id_maquina = (?)",(id_maquina,))
        else:
            cur.execute("UPDATE PERMISOS SET permis = TRUE WHERE id_maquina = (?)",(id_maquina,))
    else:
        if(type == "utilitzacio"):
            cur.execute("UPDATE PERMISOS SET utilitzacio = TRUE WHERE email = (?) AND id_maquina = (?)",(user,id_maquina,))
        else:
            cur.execute("UPDATE PERMISOS SET permis = TRUE WHERE email = (?) AND id_maquina = (?)",(user,id_maquina,))

    conn.commit()
    conn.close()
    return


def afegir_user_permisos(email, id_maquina, permis, utilitzacio):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("INSERT INTO PERMISOS (email, id_maquina, permis, utilitzacio) VALUES ((?),(?),(?),(?))",(email, id_maquina, permis, utilitzacio,))
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        return -1


def delete_all_permisions(user):
    """
    Elimina tots els permisos
    """
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    if(user == "Tots"):
        cur.execute("UPDATE PERMISOS SET utilitzacio = FALSE")
        cur.execute("UPDATE PERMISOS SET permis = FALSE")

    else:
        cur.execute("UPDATE PERMISOS SET utilitzacio = FALSE  WHERE email=(?)",(user,))
        cur.execute("UPDATE PERMISOS SET permis = FALSE  WHERE email=(?)",(user,))

    conn.commit()
    conn.close()
    return

def get_maquina_id(maquina_name):
    """
    Retorna el id de la maquina a partir del seu nom.  Si no existeix la maquina retorna -1.

    Parameters
    --------
    maquina_name : str
        nom de la maquina
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("SELECT id_maquina FROM MAQUINA WHERE nom_maquina = (?)", (maquina_name,))
        id_maquina = cur.fetchone()
        conn.close()
        return id_maquina[0]

    except Exception as e:
        print (e)
        return -1

def check_permision(email,maquina_id):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT permis, utilitzacio FROM PERMISOS WHERE email = (?) AND id_maquina = (?)", (email,maquina_id,))
    permis = cur.fetchone()
    conn.close()
    if(permis == None):
        return False
    elif((permis[0] == True) and (permis[1] == True)):
        return True
    else:
        return False


def get_maquina_name(maquina_id):
    """
    Retorna el nom de la maquina a partir del seu id

    Parameters
    --------
    maquina_id : str
        id de la maquina
    """

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT nom_maquina FROM MAQUINA WHERE id_maquina = (?)", (maquina_id,))
    nom_maquina = cur.fetchone()
    conn.close()
    return nom_maquina[0]


def get_hist_machines(maquina_id,data_inici,data_final):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    if(maquina_id == None):
        cur.execute("SELECT data, hora_entrada, hora_sortida, email, consum, id_maquina FROM HISTORIAL WHERE data >= (?) AND data <= (?)", (data_inici,data_final,))
    else:
        cur.execute("SELECT data, hora_entrada, hora_sortida, email, consum, id_maquina FROM HISTORIAL WHERE data >= (?) AND data <= (?) AND id_maquina = (?)", (data_inici,data_final,maquina_id,))

    historials = cur.fetchall()
    items = []
    for hist in historials:
        print(hist)
        item =  [datetime.datetime.strptime(hist[0],"%Y-%m-%d").strftime("%d-%m-%y")] + list(hist[1:4]) + [hist[4]] + [get_maquina_name(hist[5])]
        items += [item]
    conn.close()
    return items


def check_code(code):
    print(code)
    if(len(code) != 8):
        return False
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT id FROM USUARI WHERE id = (?)", (code,))
    id = cur.fetchone()
    conn.close()
    print(id)
    if(id == None):
        return True
    else:
        return False


def add_user(email,nom,cognom1,cognom2,password,rol,codi):
    """
    Afegeix un usuari a USUARI amb els parametres

    Parameters
    --------
    email : str
        email de l'usuari
    nom: str
        nom de l'usuari
    cognom1: str
        primer cognom de l'usuari
    cgonom2: str
        segon cognom de l'usuari
    password: str
        password de l'usuari sense hash
    rol: str
        rol de l'usuari
    codi: str
        codi de la tarjeta de l'usuari
    """
    password_hash = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("INSERT INTO USUARI (email,nom,cognom1,cognom2,pw_hash,rol,id) VALUES ((?),(?),(?),(?),(?),(?),(?))", (email,nom,cognom1,cognom2,password_hash,rol,codi,))
    conn.commit()
    conn.close()
    return


def get_all_users():
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT email FROM USUARI")
    users = cur.fetchall()
    conn.close()
    return users


def get_all_machines_name():
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT nom_maquina FROM MAQUINA")
    maquines = cur.fetchall()
    conn.close()
    return maquines

def get_all_machines_id():
    """
    Retorna l'estat de totes les maquines si id = None o d'una en concret
    Parameters
    --------
    id : str
        identificador de la maquina
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""SELECT id_maquina FROM MAQUINA""")
        ids = cur.fetchall()
        conn.close()
        return ids

    except Exception as e:
        print (e)
        return -1

def get_state_machines(id):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    if(id == None):
        cur.execute("SELECT id_maquina,nom_maquina,estat,email FROM MAQUINA")
    else:
        cur.execute("SELECT id_maquina,nom_maquina,estat,email FROM MAQUINA WHERE id_maquina = (?)",(id,))
    items = cur.fetchall()
    conn.close()
    return items

def get_mail(id_targeta):
    """
    Retorna l'email d'un usuari amb un id_targeta
    Parameters
    --------
    id_targeta : str
        identificador de la targeta d'usuari
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""SELECT email FROM USUARI WHERE id = (?) """,(id_targeta,))
        email = cur.fetchone()
        conn.close()
        return email[0]

    except Exception as e:
        print(e)
        return -1


def check_aforament():
    """
    Retorna l'aforament actual del TechLab i el màxim. En cas d'error retorna -1.
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""SELECT aforament_max, aforament_actual FROM TECHLAB """)
        aforament = cur.fetchone()
        conn.close()
        return aforament

    except Exception as e:
        print (e)
        return -1


def consulta_estat_maquina(maquina):
    """
    Retorna l'estat d'una màquina. En cas d'error retorna -1
    Parameters
    --------
    maquina : str
        nom de la maquina
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""SELECT estat FROM MAQUINA WHERE nom_maquina = (?) """,(maquina,))
        estat = cur.fetchone()
        conn.close()
        return estat

    except Exception as e:
        print (e)
        return -1


def update_aforament(nou_aforament):
    """
    Actualitza en 1 l'aforament cada cop que s'ocupi/desocupi una màquina.
    Parameters
    --------
    nou_aforament : str
        aforament del techlab
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""UPDATE TECHLAB SET aforament_actual = (?)""",(nou_aforament,))
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)


def canvia_estat_maquina(maquina,estat):
    """
    Canvia l'estat d'una màquina. Si ocurreix un error retorna -1.
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""UPDATE MAQUINA SET estat = (?) WHERE nom_maquina = (?)""",(estat,maquina))
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        return -1

def insert_history_machines(id_maquina,email,hora_entrada,hora_sortida,data,consum,hora_consum):
    """
    Insereix en l'historial de màquines les dades de consum en un dia i hora concreta d'un usuari
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("INSERT INTO HISTORIAL (id_maquina,email,hora_entrada,hora_sortida,hora_consum,data,consum) VALUES ((?),(?),(?),(?),(?),(?),(?))",(id_maquina,email,hora_entrada,hora_sortida,hora_consum,data,consum,))
        conn.commit()
        conn.close()


    except Exception as e:
        print(e)
        return -1


def fin_reserva(hora_out,id_maquina,data):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""UPDATE RESERVES SET hora_sortida = (?) WHERE id_maquina = (?) AND data = (?)""",(hora_out,id_maquina,data))
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        return -1


def hist_maquina(id_maquina):
    """
    Retorna data i consum l'historial maquinaX
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""SELECT data,consum FROM HISTORIAL WHERE id_maquina = (?) """,(id_maquina,))
        estat = cur.fetchone()
        conn.close()
        return estat

    except Exception as e:
        print (e)
        return -1


def consulta_reserves(id_maquina,data,hora):
    """
    Retorna les reserves d'una maquina un dia i una hora concreta.Si no existeix retorna none. En cas d'error retorna -1.
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM RESERVES WHERE id_maquina= (?) AND data = (?) AND hora_entrada <= (?) AND hora_sortida>=(?)""",(id_maquina,data,hora,hora))
        reserva = cur.fetchone()
        conn.close()
        return reserva

    except Exception as e:
        #print (e)
        return -1


def entra_reserva(id_maquina,data,hora,valor):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""UPDATE RESERVES SET reserva_feta = (?) WHERE id_maquina= (?) AND data = (?) AND hora_entrada <= (?) AND hora_sortida>=(?)""",(valor,id_maquina,data,hora,hora))
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        return -1


def get_nfc(user):
    """
    Retorna l'uid de la targeta d'un usuari. En cas d'error retorna -1
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(""" SELECT id FROM USUARI WHERE email=(?)""",(user,))
        nfc = cur.fetchone()
        conn.close()
        return nfc[0]
    except Exception as e:
        print (e)
        return -1


def change_pswd_machine(maquina,pswd):
    """
    Canvia pswd wiffi d'una màquina
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""UPDATE CONFIGMAQUINES SET pswd_wifi = (?) WHERE nom_maquina = (?)""",(pswd,maquina))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        return -1


def change_wifi_machine(maquina,wifi):
    """
    Canvia wiffi d'una màquina
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""UPDATE CONFIGMAQUINES SET ssid_wifi = (?) WHERE nom_maquina = (?)""",(wifi,maquina))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        return -1


def get_ssid_wifi(maquina):
    """
    Retorna el nom del wifi al que la maquina està connectat
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""SELECT ssid_wifi FROM CONFIGMAQUINES WHERE nom_maquina = (?)""", (maquina,))
        wifi = cur.fetchone()
        conn.close()
        return wifi[0]

    except Exception as e:
        print(e)
        return -1


def get_password_wiffi(maquina):
    """
    Retorna el password wifi al que la maquina està connectat
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""SELECT pswd_wifi FROM CONFIGMAQUINES WHERE nom_maquina = (?)""", (maquina,))
        wifi = cur.fetchone()
        conn.close()
        return wifi[0]

    except Exception as e:
        print(e)
        return -1


def get_factor_calibracio(maquina):
    """
    Retorna el factor de calibracio de la maquina
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("""SELECT calibracio FROM MAQUINA WHERE nom_maquina = (?)""", (maquina,))
        factor = cur.fetchone()
        conn.close()
        return factor[0]

    except Exception as e:
        print(e)
        return -1


def consum_hist_maq(id_maquina,data,hora,n):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        historial = []
        hores = []
        cur.execute("""SELECT consum,hora_consum FROM HISTORIAL WHERE id_maquina= (?) AND data = (?) AND hora_entrada <= (?) AND hora_sortida>=(?) ORDER BY id DESC LIMIT ?""",(id_maquina,data,hora,hora,n))

        for i in cur:
            historial.append(i[0])
            hores.append(i[1])

        return historial,hores

    except Exception as e:
        print (e)
        return -1


def get_entra_reserva(id_maquina,data,hora):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        historial = []
        cur.execute("""SELECT reserva_feta FROM RESERVES WHERE id_maquina= (?) AND data = (?) AND hora_entrada <= (?) AND hora_sortida>=(?)""",(id_maquina,data,hora,hora))
        reserva_feta = cur.fetchone()
        return reserva_feta[0]

    except Exception as e:
        #print (e)
        return -1


def crea_maquina(id_maquina,nom_maquina,factor,descripcio):
    """
    Insereix una maquina
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("INSERT INTO MAQUINA (id_maquina,nom_maquina,descripcio,estat,email,calibracio) VALUES ((?),(?),(?),(?),(?),(?))",(id_maquina,nom_maquina,descripcio,4,"",factor))
        conn.commit()
        conn.close()


    except Exception as e:
        print(e)
        return -1


def insereix_wifi_creat(nom_maquina,ssid_wifi,pswd_wifi):
    """
    Insereix els primers valors de wifi quan es crea la màquina
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("INSERT INTO CONFIGMAQUINES (nom_maquina,ssid_wifi,pswd_wifi) VALUES ((?),(?),(?))",(nom_maquina,ssid_wifi,pswd_wifi))
        conn.commit()
        conn.close()


    except Exception as e:
        print(e)
        return -1


def check_permision_individual(email, maquina_id):
    """
    Retorna els permisos de la maquina.
    Parameters
    ----------
    email: str
        email de l'usuari
    maquina_id: str
        identificador de la màquina
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("SELECT permis, utilitzacio FROM PERMISOS WHERE email = (?) AND id_maquina = (?)", (email, maquina_id,))
        permis = cur.fetchone()
        conn.close()
        return permis

    except Exception as e:
        print (e)
        return -1

def update_user_permisos(email, id_maquina, permis, utilitzacio):
    """
    actualitza permisos de l'usuari
    Parameters
    ----------
    email: str
        email de l'usuari
    maquina_id: str
        identificador de la màquina
    permis: int
        boolea permis
    utilitzacio: int
        boolea utilitzacio
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("UPDATE PERMISOS set permis = (?), utilitzacio = (?) WHERE email=(?) and id_maquina=(?)",(permis, utilitzacio,email, id_maquina))
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        return -1


def elimina_maquina(maquina):
    """
    Elimina una maquina
    Parameters
    ----------
    maquina: str
        nom de la màquina
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("DELETE FROM MAQUINA WHERE nom_maquina = (?)",(maquina,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return -1


def elimina_permisos_maquina(id_maquina):
    """
    Elimina permisos maquina
    Parameters
    ----------
    maquina_id: int
        identificador de la màquina
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("DELETE FROM PERMISOS WHERE id_maquina = (?)",(id_maquina,))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        return -1


def elimina_usuari(email):
    """
    Elimina usuari
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("DELETE FROM USUARI WHERE email = (?)",(email,))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        return -1


def elimina_permisos_usuari(email):
    """
    Elimina permisos maquina
    """
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("DELETE FROM PERMISOS WHERE email = (?)",(email,))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        return -1


def reserva_avui_user(user,data):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        historial = []
        cur.execute("""SELECT id_maquina FROM RESERVES WHERE email= (?) AND data = (?)""",(user,data))
        reserva_feta = cur.fetchall()
        if reserva_feta == []:
            return False
        else:
            return True
    except Exception as e:
        print (e)
        return -1


def generate_pw(user):
    pw = ''
    for i in range(8):
        pw += random.choice(string.ascii_lowercase + string.digits)
    pw_hash = hashlib.sha256(str(pw).encode('utf-8')).hexdigest()
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("UPDATE USUARI SET pw_hash = (?) WHERE email = (?)",(pw_hash,user))
        conn.commit()
        conn.close()
        return pw
    except Exception as e:
        print(e)
        return -1
