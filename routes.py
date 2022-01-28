# -*- coding: utf-8 -*-
from flask import *
from flask import Blueprint, render_template, request, redirect, Response, session, url_for
from datetime import timedelta
import datetime
import models
import functools
import random
import dateControl
import send_email



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if not session:
            return redirect(url_for("login", next=request.url))
        return func()
    return secure_function

def admin_required(func):
    @functools.wraps(func)
    def secure_function_admin():
        if session:
            if (session["rol"]) != "Administrador":
                return redirect(url_for("index"))
            return func()
        else:
            return(redirect(url_for("login",next=request.url)))
    return secure_function_admin

def not_logged(func):
    @functools.wraps(func)
    def secure_function_logged():
        #TODO: Mirar de loggegar des de diferents dispositius
        if(session["rol"] == "Administrador"):
            return redirect(url_for("admin"))
        elif(session["rol"] == "Client"):
            return redirect(url_for("client"))
        return func()
    return secure_function_logged

@app.route("/")
def index():
    return render_template('base/index.html')

@app.route("/index")
def index_bar():
    return redirect(url_for('index'))

@app.route("/about")
def about():
    return render_template('base/about.html')

@app.route("/contact", methods = ["GET", "POST"])
def contact():
    if(request.method == "GET"):
        return render_template('base/contact.html')

    elif(request.method == "POST"):
        nom = request.form["name"]
        email = request.form["email"]
        subj = request.form["subject"]
        text = request.form["message"]
        send_email.email_contact(nom,email,subj,text)
        return render_template('base/contact.html', msg="Valid_form")

@app.route("/privacitat")
def privacitat():
    return render_template('base/privacitat.html')

@app.route('/entrar', methods = ["GET","POST"])
def login():
    error = None
    session.permanent = True
    if(request.method == "POST"):
        try:
            email = request.form["email"]
            password = request.form["password"]


            if (models.check_email(email) and models.check_password(email,password)):
                session["name"] = models.get_name(email)
                session["rol"] = models.get_rol(email)
                session["email"] = email
                if(session["rol"]) == "Administrador":
                    return redirect(url_for("admin"))
                return redirect(url_for("client"))

            else:
                return render_template('base/entrar.html', error = "INVALID_FORM")
        except:
            user = request.form["usuari"]
            if models.check_email(user):
                print("Enviar correu")
                pw = models.generate_pw(user)
                name = models.get_name(user)
                send_email.new_pw(user,name,pw)
                return render_template('base/entrar.html',msg="CorreuEnviat")
            else:
                return render_template('base/entrar.html',msg="NoCorreuEnviat")

    else:
        return render_template('base/entrar.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/avis_legal")
def avis_legal():
    return render_template('base/avis_legal.html')


##### FUNCIONS ADMIN
@app.route("/admin/perfil",methods = ["GET","POST"])
@login_required
@admin_required
def adminPerfil():
    if(request.method == "GET"):
        user = models.get_user_name(session["email"])
        if(len(user) == 2):
            user_name = user[0].capitalize() + " " + user[1].capitalize()
        else:
            user_name = user[0].capitalize() + " " + user[1].capitalize() + " " + user[2].capitalize()
        session["fullname"] = user_name
        return render_template("admin/perfil.html")

    if(request.method == "POST"):
        new_password =  request.form['newpassword']
        new_email =  request.form['newemail']
        if(new_email !=""):
            if(models.check_email(new_email) == False):
                models.update_email(session["email"],new_email)
                session["email"] = new_email
                return render_template('admin/perfil.html',message = "EXIT")
            else:
                return render_template('admin/perfil.html',message = "emailJaExisteix")

        if(new_password != ""):
            models.update_password(session["email"],new_password)
            return render_template('admin/perfil.html',message = "EXIT")
            
        return render_template('admin/perfil.html',message = "introduceDatos") 

@app.route("/admin/reservar", methods = ["GET","POST"])
@login_required
@admin_required
def reservar():
    error = None
    if(request.method == "POST"):
        email = request.form['email']
        date = request.form['data']
        time_in = request.form['data_inici']
        time_out = request.form['data_final']
        maquina_name = request.form['maquines']
        maquines = [i[0] for i in models.get_all_machines_name()]
        for key in request.form:
            if request.form[key] == "":
                return render_template('admin/reservar.html',error= "Invalid_form")

        if(models.check_date(date,time_in,time_out) == False):
            return render_template('admin/reservar.html',error = "Invalid_data")

        #elif not(dateControl.check_hour(time_in,time_out,"admin")):
        #    return render_template('admin/reservar.html',error = "TempsMinim")

        elif maquina_name not in maquines:
            return render_template('admin/reservar.html',error = "MachineNoExist")

        elif models.consulta_estat_maquina(maquina_name)[0] == 2:
            return render_template('admin/reservar.html',error = "MaquinaAveriada")

        elif(models.check_email(email)== False):
            return render_template('admin/reservar.html',error = "Invalid_email")

        maquina_id = models.get_maquina_id(maquina_name)
        if(models.check_permision(email,maquina_id) == False):
            return render_template('admin/reservar.html',error = "Invalid_permision")

        if(models.check_reserve(maquina_id,date,time_in,time_out)== True):
            models.reserve(email,date,time_in,time_out,maquina_id)
            nom = models.get_name(email)
            maquina_name = models.get_maquina_name(maquina_id)
            send_email.mail_reserva(nom,email,date,time_in,time_out,maquina_name)
            return render_template('admin/reservar.html',msg = "Valid_form")
        else:
            return render_template("admin/reservar.html",error = "Invalid_reserved_already")
    elif (request.method == "GET"):
        maquines = models.get_all_machines_name()
        return render_template('admin/reservar.html',maquines = maquines)


@app.route("/admin/cancelar", methods = ["POST","GET"])
@login_required
@admin_required
def cancelar_reserva():
    error = None
    if (request.method == "POST"):
        maquina_name = request.form["maquina_name"]
        date = request.form["data"]
        time = request.form["time"]
        for key in request.form:
            if request.form[key] == "":
                return render_template("admin/cancelar.html",error = "Invalid_form")
        if(models.check_date(date,time,time) == False):
            return render_template("admin/cancelar.html",error = "Invalid_date")
        maquina_id = models.get_maquina_id(maquina_name)
        if(models.check_reserve(maquina_id,date,time,time)):
            return render_template("admin/cancelar.html",error = "Invalid_no_reserve")

        user = models.cancel_reserve(maquina_id,date,time)
        name = models.get_name(user)
        maquina_name = models.get_maquina_name(maquina_id)
        send_email.cancel_email(user,name,maquina_name,date,time)

        return render_template("admin/cancelar.html", msg = "Valid_form")
    elif(request.method == "GET"):
        maquines = models.get_all_machines_name()
    return render_template("admin/cancelar.html",maquines = maquines)

@app.route("/admin/inici", methods = ["GET"])
@admin_required
@login_required
def admin():
    date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    items = models.get_reserve(None,date,date)
    maquines = models.get_state_machines(None)
    return render_template('admin/admin.html',items=items, maquines = maquines[0:10],meitat = 5)

@app.route("/admin/maquines")
@login_required
@admin_required

def maquines():
    items = models.get_state_machines(None)
    taula_maquines = []
    for item in items:
        maquina = []
        maquina.append(item[0])
        maquina.append(item[1])
        estat = item[2]
        if estat == 3:
            maquina.append("Encés")
        elif estat == 4:
            maquina.append("Apagat")
        else:
            maquina.append("Emergencia")
        Reserva, hora, id_maquina, Data = consultaReserva(item[1])
        if Reserva is not(None) and Reserva != -1:
            nom = models.get_nameComplete(Reserva[0])
            maquina.append(nom[0] + " " + nom[1] + " " + nom[2])
        else:
            maquina.append("---")
        taula_maquines.append(maquina)

    mapa_maquines = models.get_state_machines(None)
    return render_template('admin/maquines.html',items=taula_maquines, maquines = mapa_maquines[0:10])


def consultaReserva(maquinaX):
    """
    Consulta una reserva d'una màquina concreta en una hora concreta.
    """
    Data = datetime.datetime.now().strftime("%Y-%m-%d")
    hora = datetime.datetime.now().strftime("%H:%M")
    id_maquina = models.get_maquina_id(maquinaX)
    Reserva = models.consulta_reserves(id_maquina,Data,hora)
    return Reserva,hora,id_maquina,Data

@app.route("/admin/redirect/<string:ruta>",methods = ["GET"])
def redirect_privacitat(ruta):
        return render_template('base/'+ruta+'.html')


@app.route("/admin/afegir_usuari",methods = ["GET","POST"])
@login_required
@admin_required
def afegir_usuari():

    if request.method=="GET":
        return render_template('admin/afegir_usuari.html')

    elif(request.method == "POST"):

        try:
            user = request.form['name'].split()
            email = request.form['email']
            password = request.form['password']
            password_repeat = request.form['password_repeat']
            rol = request.form['rol']
            codi = request.form['codi']

            id_maquines = models.get_all_machines_id()


            for key in request.form:
                if request.form[key] == "":
                    return render_template('admin/afegir_usuari.html',error= "Invalid_form")
            nom = user[0].capitalize()

            try:
                cognom1 = user[1].capitalize()
            except:
                cognom1=""
            try:
                cognom2 = user[2].capitalize()
            except:
                cognom2=""
            if(models.check_email(email) == False):
                if(password == password_repeat):
                    if(rol == "Administrador" or rol =="Usuari"):
                        if(models.check_code(codi)):
                            models.add_user(email,nom,cognom1,cognom2,password,rol,codi)
                            for maquina in id_maquines:
                                if rol == "Administrador":
                                    models.afegir_user_permisos(email, maquina[0], 1, 1)
                                else:
                                    models.afegir_user_permisos(email, maquina[0], 0, 0)
                            return render_template('admin/afegir_usuari.html',msg="Valid_form")
                        else:
                            return render_template('admin/afegir_usuari.html',error = "Invalid_code")
            return render_template('admin/afegir_usuari.html',error = "Invalid_form")

        except:
           email = request.form["mail"]
           if models.check_email(email):
               models.elimina_usuari(email)
               models.elimina_permisos_usuari(email)
               return render_template('admin/afegir_usuari.html',msg="eliminat")
           else:
               return render_template('admin/afegir_usuari.html',msg = "noEliminat")


@app.route("/admin/afegir_permisos",methods=["GET","POST"])
@login_required
@admin_required
def afegir_permisos():
    if(request.method == "GET"):
        return render_template('admin/permisos.html',taula=False,value="",msg=False,estatAnterior="")

    elif(request.method == "POST"):
        maquines_noms = models.get_all_machines_name()
        user = request.form['usuaris']
        maquines = []
        if not(models.check_email(user)):
                return render_template('admin/permisos.html', msg="NoExisteix",maquines=maquines,taula=False,valor=user,estatAnterior="")
        if request.form['boto-permis'] == 'afegir':
            for i in maquines_noms:
                permisos = models.check_permision(user,models.get_maquina_id(i[0]))
                if not(permisos):
                    maquines.append([models.get_maquina_id(i[0]),i[0]])

            if maquines == []:
                maquines.append(["---","---"])
            return render_template('admin/permisos.html', msg=False,maquines=maquines,taula=True, valor=user,estatAnterior="afegir")


        elif request.form['boto-permis'] == 'eliminar':
            maquines_noms = models.get_all_machines_name()
            user = request.form['usuaris']
            maquines = []
            if not(models.check_email(user)):
                return render_template('admin/permisos.html', msg="NoExisteix",maquines=maquines,taula=False,valor=user,estatAnterior="")
            for i in maquines_noms:
                permisos = models.check_permision(user,models.get_maquina_id(i[0]))
                if permisos:
                    maquines.append([models.get_maquina_id(i[0]),i[0]])

            if maquines == []:
                maquines.append(["---","---"])
            return render_template('admin/permisos.html', msg=False,maquines=maquines,taula=True,valor=user,estatAnterior="eliminar")

        elif request.form["boto-permis"] == "modificar":
            user = request.form['usuaris']
            estat_anterior = request.form['estatAnterior']
            if not(models.check_email(user)):
                return render_template('admin/permisos.html', msg="NoExisteix",maquines=maquines,taula=False,valor=user,estatAnterior="")
            for key in request.form:
                if(key != 'usuaris' and key!= 'boto-permis' and key!="estatAnterior"):
                    valor = key.split('_')
                    id_maquina = valor[0]
                    permis = valor[1]
                    check = models.check_permision_individual(user, id_maquina)
                    if permis == "permis" and estat_anterior=="afegir":
                        if check[1]:
                            models.update_user_permisos(user, id_maquina, 1, 1)
                        else:
                            models.update_user_permisos(user,id_maquina, 1, 0)

                    elif permis=="utilitzacio" and estat_anterior=="afegir":
                        if check[0]:
                            models.update_user_permisos(user, id_maquina, 1, 1)
                        else:
                            models.update_user_permisos(user,id_maquina, 0, 1)

                    elif permis=="permis" and estat_anterior=="eliminar":
                        if check[1]:
                            models.update_user_permisos(user, id_maquina, 0, 1)
                        else:
                            models.update_user_permisos(user,id_maquina, 0, 0)

                    elif permis=="utilitzacio" and estat_anterior=="eliminar":
                        if check[0]:
                            models.update_user_permisos(user, id_maquina, 1, 0)
                        else:
                            models.update_user_permisos(user,id_maquina, 0, 0)

            if maquines == []:
                maquines.append(["---","---"])
            return render_template('admin/permisos.html', msg="si",maquines=maquines,taula=False, valor="",estatAnterior="")



@app.route("/admin/histUsers", methods= ["GET","POST"])
@login_required
@admin_required
def historial_usuaris():
    if(request.method == "GET"):
        date_today =  datetime.date.today()
        date_last_week = date_today-timedelta(days=7)

        items = models.get_reserve(None,str(date_last_week),str(date_today))
        return render_template('admin/histUsers.html',items=items)

    if(request.method == "POST"):
        email  = request.form['usuari']
        data_inici = request.form['data_inici']
        data_final = request.form['data_final']
        for key in request.form:
            if request.form[key] == "":
                return render_template('admin/histUsers.html',error= "Invalid_form")
        if(email == "Tots"):
            items = models.get_reserve(None,data_inici,data_final)
            return render_template('admin/histUsers.html',search = True,items = items)
        else:
            items = models.get_reserve(email,data_inici,data_final)
            return render_template('admin/histUsers.html', search = True, items=items)

@app.route("/admin/histMaquines", methods= ["GET","POST"])
@login_required
@admin_required
def historial_maquines():
    if(request.method == "GET"):
        date_today =  datetime.date.today()
        date_last_week = date_today-timedelta(days=7)
        items = models.get_hist_machines(None,date_last_week,date_today)
        maquines = models.get_all_machines_name()
        return render_template('admin/histMaquines.html',items=items,maquines = maquines)
    if(request.method == "POST"):
        maquina_name  = request.form['maquina']
        data_inici = request.form['data_inici']
        data_final = request.form['data_final']
        for key in request.form:
            if request.form[key] == "":
                return render_template('admin/histMaquines.html',error= "Invalid_form")
        if(maquina_name == "Totes"):
            items = models.get_hist_machines(None,data_inici,data_final)
            return render_template('admin/histMaquines.html',search = True,items = items)
        else:
            maquina_id = models.get_maquina_id(maquina_name)
            items = models.get_hist_machines(maquina_id,data_inici,data_final)
            return render_template('admin/histMaquines.html', search = True, items=items)

@app.route("/admin/maquina/<int:id_maquina>")
def maquina(id_maquina):
    maquina = models.get_state_machines(id_maquina)[0]
    return render_template("admin/maquina.html", maquina = maquina)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("/base/error_404.html")

@app.route("/admin/afegir_maquina",methods = ["GET","POST"])
@login_required
@admin_required
def afegir_maquina():
    if(request.method == "GET"):
        return render_template("admin/afegir_maquina.html")

    elif(request.method == "POST"):

        try:
            if request.form["eliminar"]:
                maq = request.form["nom"]
                maquines = [i[0] for i in models.get_all_machines_name()]
                if maq in maquines:
                    models.elimina_maquina(maq)
                    id = models.get_maquina_id(maq)
                    models.elimina_permisos_maquina(id)
                    return render_template("/admin/afegir_maquina.html",msg="MàquinaEliminada")
                else:
                    return render_template("/admin/afegir_maquina.html",msg="MaquinaNOExisteix")

        except Exception as e:
            nom_maquina = request.form["nombre"]
            id_maquina = request.form["idMaquina"]
            descripcio = request.form["descripcio"]
            maquines = [i[0] for i in models.get_all_machines_name()]
            ids = [i[0] for i in models.get_all_machines_id()]

            all_users = models.get_all_users()
            for user in all_users:
                if models.get_rol(user[0]) == "Administrador":
                    models.afegir_user_permisos(user[0], id_maquina, 1, 1)
                else:
                    models.afegir_user_permisos(user[0], id_maquina, 0, 0)

            try:
                factor = request.form["factorCalibracio"]
                if factor == "":
                    factor = 1

                else:
                    factor = float(factor)

            except:
                factor = False

            if nom_maquina in maquines:
                return render_template("admin/afegir_maquina.html", msg="Maquinaexistent")

            elif int(id_maquina) in ids:
                return render_template("admin/afegir_maquina.html", msg="IDexistent")

            elif not(factor):
                return render_template("admin/afegir_maquina.html", msg="Factorerroni")

            else:
                if descripcio =="":
                    descripcio = ""

                models.crea_maquina(id_maquina,nom_maquina,factor,descripcio)
                models.insereix_wifi_creat(nom_maquina,"Prieto","12345678",) 
                return render_template("/admin/afegir_maquina.html",msg="Valid_form")




###FUNCIONS CLIENT

@app.route("/client/inici", methods = ["GET","POST"])
@login_required
def client():
    #TODO:ACABAR -> MIRAR QUE QUEDA MILLOR SI ULTIMA SETMANA O FUTURES RESERVES
    if(request.method == "GET"):
        date_today =  datetime.date.today()
        date_last_week = date_today-timedelta(days=7)
        items = models.get_reserve(session['email'],str(date_last_week),str(date_today))

        return render_template("client/client.html",items = items)



@app.route("/client/historial-client", methods = ["GET","POST"])
@login_required
def histClient():
    if(request.method == "GET"):
        date_today =  datetime.date.today()
        date_last_week = date_today-timedelta(days=7)

        items = models.get_reserve(None,str(date_last_week),str(date_today))
        return render_template('client/historial-client.html',items=items)

    if(request.method == "POST"):
        email = session["email"]
        data_inici = request.form['data_inici']
        data_final = request.form['data_final']
        for key in request.form:
            if request.form[key] == "":
                return render_template('client/historial-client.html',error= "Invalid_form")

        else:
            items = models.get_reserve(email,data_inici,data_final)
            return render_template('client/historial-client.html', search = True, items=items)



@app.route("/client/perfil",methods = ["GET","POST"])
@login_required
def perfil():

    if(request.method == "GET"):
        user = models.get_user_name(session["email"])
        if(len(user) == 2):
            user_name = user[0].capitalize() + " " + user[1].capitalize()
        else:
            user_name = user[0].capitalize() + " " + user[1].capitalize() + " " + user[2].capitalize()
        session["fullname"] = user_name
        return render_template("client/perfil.html")

    elif(request.method == "POST"):
        new_password =  request.form['newpassword']
        new_email =  request.form['newemail']
        if(new_email !=""):
            if(models.check_email(new_email) == False):
                models.update_email(session["email"],new_email)
                session["email"] = new_email
                return render_template('client/perfil.html',message = "EXIT")
            else:
                return render_template('client/perfil.html',message = "emailJaExisteix")

        if(new_password != ""):
            models.update_password(session["email"],new_password)
            return render_template('client/perfil.html',message = "EXIT")
            
        return render_template('client/perfil.html',message = "introduceDatos") 



@app.route("/reservar",methods=["GET","POST"])
@login_required
def redirigir_reserva():
    try:
        if(session["rol"]) == "Administrador":

            return redirect(url_for("reservar"))
        elif (session["rol"]) == "Usuari":
            return redirect(url_for("reservar_client"))
    except:
        return redirect(url_for("login"))



@app.route("/client/reservar-client", methods = ["GET","POST"])
@login_required
def reservar_client():
    if(request.method == "POST"):
        date = request.form['data']
        time_in = request.form['hora_inici']
        time_out = request.form['hora_final']
        maquina_name = request.form['maquina']
        maquines = [i[0] for i in models.get_all_machines_name()]
        for key in request.form:
            if request.form[key] == "":
                return render_template('client/reservar-client.html',error= "Invalid_form")
        if(models.check_date(date,time_in,time_out) == False):
            return render_template('client/reservar-client.html',error = "Invalid_data")

        maquina_id = models.get_maquina_id(maquina_name)

        if maquina_name not in maquines:
            return render_template('admin/reservar.html',error = "MachineNoExist")

        if models.consulta_estat_maquina(maquina_name)[0] == 2:
            return render_template('client/reservar-client.html',error = "MaquinaAveriada")

        if(models.check_permision(session['email'],maquina_id) == False):

            return render_template('client/reservar-client.html',error = "Invalid_permision")

        if not(dateControl.check_hour(time_in,time_out,"client")):
            print("Temps minim")
            return render_template('client/reservar-client.html',error = "TempsMinim")

        if models.reserva_avui_user(session["email"],date):
            return render_template('client/reservar-client.html',error = "ReservaON")


        if(models.check_reserve(maquina_id,date,time_in,time_out)== True):
            models.reserve(session['email'],date,time_in,time_out,maquina_id)
            return render_template('client/reservar-client.html',msg = "Valid_form")
        else:
            return render_template("client/reservar-client.html",error = "Invalid_reserved_already")
    elif(request.method == "GET"):
        maquines = models.get_all_machines_name()
        return render_template("client/reservar-client.html",maquines = maquines)



@app.route("/client/cancelar-client", methods = ["POST","GET"])
@login_required
def cancelar_reserva_client():
    if (request.method == "POST"):
        maquina_name = request.form["maquina_name"]
        date = request.form["data"]
        time = request.form["time"]
        for key in request.form:
            if request.form[key] == "":
                return render_template("client/cancelar-usuari.html",error = "Invalid_form")
        if(models.check_date(date,time,time) == False):
            return render_template("client/cancelar-client.html",error = "Invalid_date")

        maquina_id = models.get_maquina_id(maquina_name)
        if(models.check_reserve(maquina_id,date,time,time)):
            return render_template("client/cancelar-client.html",error = "Invalid_no_reserve")

        user = models.cancel_reserve(maquina_id,date,time)
        name = models.get_name(user)
        maquina_name = models.get_maquina_name(maquina_id)
        send_email.cancel_email(user,name,maquina_name,date,time)
        return render_template("client/cancelar-client.html", msg = "Valid_form")
    elif(request.method == "GET"):
        maquines = models.get_all_machines_name()
    return render_template("client/cancelar-client.html",maquines = maquines)
