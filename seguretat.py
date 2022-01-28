# coding: utf-8
# #!/usr/bin/python

from cryptography.fernet import Fernet
import time,string,random

"""
SEGURETAT APLICACIÓ GRAFICA
"""

def carrega_clau():
    return open("clave.key","r").read()


def encripta(missatge):

    clau = carrega_clau()
    f = Fernet(clau)   
    encrypted = f.encrypt(missatge.encode("utf-8"))
    return encrypted
    
   
def desencripta(missatge):

    clau = carrega_clau()
    f = Fernet(clau)
    text = f.decrypt(missatge)
    return text.decode("utf-8")


