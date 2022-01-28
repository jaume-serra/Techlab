import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_address = 'techlabepsem21@gmail.com'
sender_pass = 'Integracio'


def mail_reserva(nom,email,date,time_in,time_out,maquina_name):
    """Envia un email a tots els usuaris al realitzar una reserva
    Parameters
    ----------
    email: str
        email de l'usuari
    date : str
        data en format %Y-%m-%d
    time_in: str
        data en format %H:%M
    time_out: str
        data en format %H:%M
    maquina_id: int
        identificador de la màquina

    """

    receiver_address = email
    try:
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        mail_content = "Hola {}, s'acaba de realitzar correctament una reserva per la màquina {} el dia {}.\n\nHora d'entrada: {}\nHora sortida: {} \n\n\nTechLab EPSEM"
        mail_content = mail_content.format(nom,maquina_name,date,time_in,time_out)
        message['Subject'] = 'Reserva TechLab'   #The subject line
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
        return
    except Exception as e:
        print(e)
        return


def email_contact(nom,email,subj,text_email):
    """
    Envia un email a tots els usuaris al realitzar una reserva
    Parameters
    ----------
    nom: str
        nom de l'usuari
    email: str
        email de l'usuari
    subj: str
        subjecte del email
    text_email: str
        missatge del email
    """

    receiver_address = email
    try:
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address

        mail_content = text_email + "\nEmail enviat per: {}\nEmail: {}"
        mail_content = mail_content.format(nom,email)
        message['Subject'] = subj   #The subject line
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, sender_address, text)
        session.quit()
        print('Mail Sent')
        return
    except Exception as e:
        print(e)
        return


def cancel_email(user,name,maquina_name,date,time):
    """
    Envia un email a l'usuari quan cancela una reserva
    Parameters
    ----------
    user: str
        email de l'usuari
    nom: str
        nom de l'usuari
    maquina_name: str
        nom de la màquina
    date : str
        data en format %Y-%m-%d
    time: str
        data en format %H:%M
    """

    receiver_address = user
    try:
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        mail_content = "Hola {}, s'acaba de cancelar una reserva per la màquina {} el dia {}.\n\nHora: {}\n\nTechLab EPSEM"
        mail_content = mail_content.format(name,maquina_name,date,time)
        message['Subject'] = 'Reserva TechLab'   #The subject line
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
        return
    except Exception as e:
        print(e)
        return


def new_pw(user,name,pw):
    """
    Envia la nova contrasenya de l'usuari
    Parameters
    ----------
    user: str
        email de l'usuari
    pw: str
        nova contrasenya de l'usuari
    """

    receiver_address = user
    try:
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        mail_content = "Hola {},\nAquesta és la nova contrasenya: {}\nRecorda de canviar-la un cop entris.\n\nTechLab EPSEM"
        mail_content = mail_content.format(name,pw)
        message['Subject'] = 'Reserva TechLab'   #The subject line
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
        return
    except Exception as e:
        print(e)
        return
