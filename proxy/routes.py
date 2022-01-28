# -*- coding: utf-8 -*-
from flask import *
from flask import Blueprint, render_template, request, redirect, Response, session, url_for
import json, requests


Server_Name = "https://epsemtechlab.ddns.net/"

app = Flask(__name__)

@app.route("/handshaking/maquina/<string:maquina>",methods=["GET"])
def handshaking(maquina):
    http=requests.get(Server_Name+"handshaking/maquina/"+maquina)
    msg=json.loads(http.content)
    return msg,200


@app.route("/reserves/maquina/<string:maquina>/<string:estat>", methods = ["GET"])
def nextReserva(maquina,estat):
    http=requests.get(Server_Name+"reserves/maquina/"+maquina+'/'+estat)
    msg=json.loads(http.content)
    return msg,200


@app.route("/nfc-in/maquina/<string:maquina>/<string:estat>",methods=["PUT"])
def nfc_in(maquina,estat):
    http=requests.put(Server_Name+"nfc-in/maquina/"+maquina+'/'+estat)
    msg=json.loads(http.content)
    return msg,200


@app.route("/nfc-out/maquina/<string:maquinaX>", methods =["PUT"])
def nfc_out(maquinaX):
    http=requests.put(Server_Name+"nfc-out/maquina/"+maquinaX)
    msg=json.loads(http.content)
    return msg,200

@app.route("/maquina/<string:maquinaX>/estat/<string:estat_actuador>/consum/<string:consum>/<string:estat>", methods = ["PUT"])
def gestioMaquina(maquinaX,estat_actuador,consum,estat):
    http=requests.put(Server_Name+"maquina/"+maquinaX+"/estat/"+estat_actuador+"/consum/"+consum+'/'+estat)
    msg=json.loads(http.content)
    return msg,200