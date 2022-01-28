# coding: utf-8
from sqlite3.dbapi2 import enable_shared_cache
from flask import *
from flask import Blueprint, render_template, request, redirect, Response, session, url_for
from datetime import timedelta
import datetime
import models
import functools
import random
import control
import seguretat
import dateControl

Control_inteligent = control.Control()
apirest = Blueprint('apirest',__name__)
WiFi_maquines = {}

#===========================
#ROUTES APIREST PER LA WEB
#===========================


@apirest.route("/api/aforament", methods = ["GET"])
def aforament():
    """
    Retorna el % d'ocupació del TechLab.
    """
    max_aforament, aforament = models.check_aforament()
    content = {"Missatge": [max_aforament,aforament]}
    return content, 200


@apirest.route("/api/hist/maquina/<string:maquinaX>/last/<int:n>", methods = ["GET"])
def maquinaHist(maquinaX, n):
    """
    Retorna l'historial de les ultimes 'n' mostres de la màquina X
    """

    Reserva,hora,id_maquina,Data = consultaReserva(maquinaX)
    Reserva_feta = models.get_entra_reserva(id_maquina,Data,hora)

    if Reserva is not(None) and Reserva != -1 and Reserva_feta==1:
        historial = models.consum_hist_maq(id_maquina,Data,hora,15)  
        graf1 = historial[0]
        graf2 = historial[1]

        content = {"valors":[i*230 for i in graf1[::-1]],
                   "hores":graf2[::-1]
                }
    else:
        graf1 = [0 for i in range(n)]
        graf2 = [0 for i in range(n)]
        content = {"valors":graf1,
                   "hores":graf2
                }
    return content, 200


@apirest.route("/api/potencies/maquines",methods = ["GET"])
def historial_potencies():

    content = {}
    maquines = models.get_all_machines_name()
    content["noms"] = maquines
    for maquina in maquines:
        Reserva, hora, id_maquina, Data = consultaReserva(maquina[0])

        if Reserva is not(None) and Reserva != -1:
            if models.get_entra_reserva(id_maquina,Data,hora) == 1:
                valors = models.consum_hist_maq(id_maquina,Data,hora,15)           
                content[maquina[0]] = [i*230 for i in valors[0][::-1]]
                content["hores"] = valors[1][::-1]
            else:
                content[maquina[0]] = [0 for i in range(15)]
        else:
            content[maquina[0]] = [0 for i in range(15)]
    
    return content,200



@apirest.route("/api/maquina/<string:maquinaX>/estat/<string:value>", methods = ["PUT"])
def canviaValorActuador(maquinaX, value):
    """
    Canvia el valor de l'actuador
    """

    if value == "on":
        arg = 3
    elif value == "off":
        arg = 4
    else:
        arg= 2

    models.canvia_estat_maquina(maquinaX,arg)
    content = {"msg": "ok"}
    return content, 200


@apirest.route("/api/maquina/<string:maquinaX>/estat", methods = ["GET"])
def consultaEstatMaquina(maquinaX):
    """
    Retorna l'estat de la màquinaX.
    """
    estat = models.consulta_estat_maquina(maquinaX)
    if estat[0] == 4:
        value ="OFF"
    elif estat[0] == 3:
        value = "ON"
    else:
        value = "emergencia"
    content = {"estat": value}
    return content, 200


@apirest.route("/api/maquines/estat", methods = ["GET"])
def consultaEstatMaquines():
    """
    Retorna l'estat de les Maquines
    """
    estat = models.get_state_machines(None)
    content = {}
    maquines = [i[0] for i in models.get_all_machines_name()]
    content["maquines"] = maquines

    for i in estat:
        if i[2] == 4:
            content[i[1]] =  ["OFF",i[0]]
        elif i[2] == 3:
            content[i[1]] = ["ON",i[0]]
        else:
            content[i[1]] = ["EMERGENCIA",i[0]]

    return content, 200


@apirest.route("/api/reserves/maquina/<string:maquinaX>", methods = ["GET"])
def checkReserva(maquinaX):
    """
    Retorna el nom de l'usuari de la reserva.
    """

    Reserva, hora, id_maquina, Data = consultaReserva(maquinaX)
    if Reserva is not(None) and Reserva != -1:
        Reserva_feta = models.get_entra_reserva(id_maquina, Data,hora)
        if Reserva_feta == 1:
            nom = models.get_nameComplete(Reserva[0])
            content = {
            "msg": "nextReserva",
            "usr": nom[0] + " " + nom[1] + " " + nom[2]
            }
        else:
            content ={"msg": "noReserva"}
    else:
        content ={"msg": "noReserva"}

    return content, 200


def consultaReserva(maquinaX):
    """
    Consulta una reserva d'una màquina concreta en una hora concreta.
    """
    Data = datetime.datetime.now().strftime("%Y-%m-%d")
    hora = datetime.datetime.now().strftime("%H:%M")
    id_maquina = models.get_maquina_id(maquinaX)
    Reserva = models.consulta_reserves(id_maquina,Data,hora)
    return Reserva,hora,id_maquina,Data



@apirest.route("/api/wifi/maquina/<string:maquinaX>", methods =["GET"])
def checkWifi(maquinaX):
    """
    Consulta el ssid del wifi de la màquina
    """
    wifi=models.get_ssid_wifi(maquinaX)
    if wifi != -1:
        content={
            "msg": wifi
        }
    else:
        content={
            "msg" : "No Wifi"
        }
        
    return content, 200

#===========================
#ROUTES APIREST PER HARDWARE
#===========================

def check_wifi(maquinaX,estat):

    if maquinaX not in WiFi_maquines:
        WiFi_maquines[maquinaX] = [models.get_ssid_wifi(maquinaX),models.get_password_wiffi(maquinaX)]

    else: 
        if estat:  # No s'ha pogut connectar al Wifi recupera el WiFi anterior que funcionava correctament.
            if '@'+maquinaX in WiFi_maquines:
                del WiFi_maquines['@'+maquinaX]

            password = WiFi_maquines[maquinaX][1]
            ssid = WiFi_maquines[maquinaX][0]
            models.change_pswd_machine(maquinaX,password)
            models.change_wifi_machine(maquinaX,ssid)
            WiFi_maquines[maquinaX] = [models.get_ssid_wifi(maquinaX),models.get_password_wiffi(maquinaX)]
        
        else:
            if WiFi_maquines[maquinaX][0] != models.get_ssid_wifi(maquinaX) and '@'+maquinaX not in(WiFi_maquines): # Añadir un nuevo Wifi

                WiFi_maquines['@'+maquinaX] = [models.get_ssid_wifi(maquinaX),models.get_password_wiffi(maquinaX),0]

            elif maquinaX in WiFi_maquines and '@'+maquinaX in WiFi_maquines:

                if WiFi_maquines['@'+maquinaX][2] <3:
                    WiFi_maquines['@'+maquinaX][2] = WiFi_maquines['@'+maquinaX][2]+1

                elif WiFi_maquines['@'+maquinaX][2] == 3:
                    del WiFi_maquines['@'+maquinaX]
                    WiFi_maquines[maquinaX] = [models.get_ssid_wifi(maquinaX),models.get_password_wiffi(maquinaX)] 


@apirest.route("/handshaking/maquina/<string:maquinaX>", methods =["GET"])
def handShaking(maquinaX):
    """
    Si existeix la màquina permet envia 'handshaking OK' per poder començar a enviar dades.
    Si la màquina no existeix, retorna 'NACK handshaking' de tal manera que no podrà enviar dades.
    """
    content = {}
    id_maquina = models.get_maquina_id(maquinaX)
    Control_inteligent.cancel_timeout_emergency_comm(id_maquina)
    Control_inteligent.set_comm_timeout(maquinaX)

    if id_maquina == -1:
        content["msg"] = "NACK handshaking"

    else:
        content["msg"] = "ACK handshaking"
        content["factor_calibracio"] = models.get_factor_calibracio(maquinaX)

    
    return content, 200


@apirest.route("/reserves/maquina/<string:maquinaX>/<string:estat>", methods = ["GET"])
def nextReserva(maquinaX,estat):
    """
    Retorna les reserves disponibles d'una màquina en una hora concreta. En cas que la reserva existeixi,
    retorna el UID de la targeta corresponent a la reserva. En cas contrari, retorna que no existeix reserva.
    """

    Data = datetime.datetime.now().strftime("%Y-%m-%d")
    hora = datetime.datetime.now().strftime("%H:%M")
    id_maquina = models.get_maquina_id(maquinaX)
    Control_inteligent.cancel_timeout_emergency_comm(id_maquina)
    Control_inteligent.set_comm_timeout(maquinaX)
    Reserva = models.consulta_reserves(id_maquina,Data,hora)
    check_wifi(maquinaX,int(estat))
    print(Data,hora,Reserva)
    if Reserva is not(None) and Reserva != -1:
        Reserva_feta = models.get_entra_reserva(id_maquina,Data,hora)
        if not(Reserva_feta) or Reserva_feta==1:
            content = {
            "msg": "nextReserva",
            "usr": models.get_nfc(Reserva[0]),
            "ssid_wifi": models.get_ssid_wifi(maquinaX),
            "password_wifi" : models.get_password_wiffi(maquinaX)
        }
        else:
            content = {"msg":"noReserva",
                       "ssid_wifi": models.get_ssid_wifi(maquinaX),
                       "password_wifi" : models.get_password_wiffi(maquinaX)
            }
    else:
        content = {    "msg":"noReserva",
                       "ssid_wifi": models.get_ssid_wifi(maquinaX),
                       "password_wifi" : models.get_password_wiffi(maquinaX)
                  }

    return content, 200


@apirest.route("/nfc-in/maquina/<string:maquinaX>/<string:estat>",methods=["PUT"])
def nfc_in(maquinaX,estat):

    max_aforament, aforament_actual = models.check_aforament()
    Reserva, hora, id_maquina,Data = consultaReserva(maquinaX)
    Reserva_feta = models.get_entra_reserva(id_maquina, Data,hora)
    check_wifi(maquinaX,int(estat))

    if aforament_actual<max_aforament and Reserva is not(None) and Reserva!=-1:
        print("SDII")
        Control_inteligent.cancel_timeout_emergency_comm(id_maquina)
        models.entra_reserva(id_maquina,Data,hora,1) 
        if not(Reserva_feta):
            models.update_aforament(aforament_actual+1)
        models.canvia_estat_maquina(maquinaX,3)
        Control_inteligent.cancel_timeout_reserva(id_maquina)
        time = dateControl.convert_second(Reserva[2],Reserva[3])
        Control_inteligent.set_timeout_fi_reserva(id_maquina,time) 
        content = {"msg":"ok"}
        content["ssid_wifi"] = models.get_ssid_wifi(maquinaX)
        content["password_wifi"] = models.get_password_wiffi(maquinaX)

    else:
        content = {"msg":"no ok"}
        content["ssid_wifi"] = models.get_ssid_wifi(maquinaX)
        content["password_wifi"] = models.get_password_wiffi(maquinaX)

    return content,200


@apirest.route("/nfc-out/maquina/<string:maquinaX>", methods =["PUT"])
def nfc_out(maquinaX):
    """
    Finalitza la reserva de la màquina si existeix, apaga la màquina i decrementa en 1 l'aforament.
    En cas que no existeixi la reserva retorna el missatge 'no ok'.
    """
    Reserva,hora,id_maquina,Data = consultaReserva(maquinaX)
    Reserva_feta = models.get_entra_reserva(id_maquina, Data,hora)

    if Reserva is not(None) and Reserva != -1 and Reserva_feta==1:
        Control_inteligent.cancel_timeout_emergency(id_maquina)
        Control_inteligent.cancel_timeout_fi_reserva(id_maquina)
        Control_inteligent.cancel_timeout_emergency_comm(id_maquina)
        max_aforament, aforament_actual = models.check_aforament()
        models.entra_reserva(id_maquina,Data,hora,2) 
        models.update_aforament(aforament_actual-1)
        models.canvia_estat_maquina(maquinaX,4)
        models.fin_reserva(hora, id_maquina,Data)
    
        content = {"msg":"apaga"}

    else:
        content = {"msg":"apaga"}

    return content, 200


@apirest.route("/maquina/<string:maquinaX>/estat/<string:estat_actuador>/consum/<string:consum>/<string:estat>" , methods = ["PUT"])
def gestioMaquina(maquinaX,estat_actuador,consum,estat):
   
    content = {}
    Reserva,hora,id_maquina,Data = consultaReserva(maquinaX)
    check_wifi(maquinaX,int(estat))
    if Reserva is not(None) and Reserva != -1:
        Reserva_feta = models.get_entra_reserva(id_maquina, Data,hora)
        if Reserva_feta == 1:           
            estat = models.consulta_estat_maquina(maquinaX)
            Control_inteligent.cancel_timeout_emergency(id_maquina)
            Control_inteligent.set_emergency_timeout(maquinaX)
            hora_consum = hora +':' +str(datetime.datetime.now().second)
            models.insert_history_machines(id_maquina,Reserva[0],Reserva[2],Reserva[3],Data,float(consum),hora_consum)
            if estat[0] == 4:
                value ="OFF"
            elif estat[0] == 3:
                value = "ON"
            else:
                value = "---"

            if dateControl.avisador(hora,Reserva[3]):
                msg = "FINALITZANT"
            else:
                msg = "ACK"
            content={
                        "msg": msg,
                        "estat-actuador": value,
                        "ssid_wifi": models.get_ssid_wifi(maquinaX),
                        "password_wifi" : models.get_password_wiffi(maquinaX)
                    }
        else:
            content ["msg"] = "apaga"
            content["ssid_wifi"] = models.get_ssid_wifi(maquinaX)
            content["password_wifi"] = models.get_password_wiffi(maquinaX)
    else:
        content ["msg"] = "apaga"
        content["ssid_wifi"] = models.get_ssid_wifi(maquinaX)
        content["password_wifi"] = models.get_password_wiffi(maquinaX)
   
    return content,200



"""
APLICACIÓ GRÀFICA
"""


@apirest.route("/maquines/all", methods = ["GET"])
def nomMaquines():
    """
    Retorna el nom de tots les màquines.
    """
    content={ "maqs": models.get_all_machines_name() }
    return content, 200


@apirest.route("/config/maquina/<string:maquinaX>/<string:ssid>/<string:pswd>", methods = ["PUT"])
def config_maquina(maquinaX,ssid,pswd):
    
    ssid = seguretat.desencripta(ssid.encode('utf-8'))
    pswd = seguretat.desencripta(pswd.encode('utf-8'))
    password = models.change_pswd_machine(maquinaX,pswd)
    wiffi = models.change_wifi_machine(maquinaX,ssid)

    if password!=-1 and wiffi !=-1:
        content ={ "config": "OK" }
        
    else:
        content ={"config": "incorrecte"}

    return content, 200

@apirest.route("/api/maquina/<string:maquinaX>/<string:ssid>/<string:pswd>", methods = ["PUT"])
def config_maquina_admin(maquinaX,ssid,pswd):
    
    password = models.change_pswd_machine(maquinaX,pswd)
    wiffi = models.change_wifi_machine(maquinaX,ssid)

    if password!=-1 and wiffi !=-1:
        content ={ "config": "OK" }
        
    else:
        content ={"config": "incorrecte"}

    return content, 200