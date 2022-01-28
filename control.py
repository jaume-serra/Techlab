
# coding: utf-8
# #!/usr/bin/python

# Mòdul: Control
# Implementa la gestió intel·ligent per controlar les reserves, el seu timeout i si hi han emergències durant 
# una reserva.


"""
#######################################
           LLIBRERIES
#######################################
"""

from threading import Timer, Thread, Event
import models
import datetime 
import time


"""
#######################################
              CODI
#######################################
"""


class Scheduler():
    """
    Implementa un sheduler per software mitjançant threads de timer i executa un handler quan es dona l'event.
    """

    def __init__(self, t, hFunction, args = None, bucle = False):
        """
        Incialitza la classe Sheduler. 
        """
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)
        self.bucle = bucle
        self.args = args

    def handle_function(self):
        """
        Executa la funció/handle de manera infinita o un sol cop llençant un thread de timer.
        """
        if self.bucle:
            self.hFunction(self.args)
            self.thread = Timer(self.t, self.handle_function)
            self.thread.start()
        else:
            self.hFunction(self.args)

    def cancel(self):
        """
        Cancel·la l'execucció d'un thread de timer,i per tant, que no s'executi el handle.
        """
        self.thread.cancel()

    def start(self):
        """
        Inicialitza un thread de timer.
        """
        self.thread.start()



class Control(object):
    """
    Controla la gestió de reserves, el timeout i les emergències.
    """

    def __init__(self):
        self.reserves = {}                     # Clau: id_Maquina ; Valor: Thread
        self.time_reserva = 600                # Timeout reserva. Si en aquest temps(s) ve l'usuari es finalitza la reserva. 10 minuts sino es cancel·la
        self.emergencia = {}                   # Clau: id_maquina, Valor:Thread  
        self.timeout_emergencia = 20           # Timeout emergencia: Si en aquests temps(s) la màquina no envia dades s'activa emergencia
        self.fi_reserves = {}                  # Clau: id_maquina ; Valor: Thread
        self.emergencia_comm = {}
        self.time_emergencia_comm = 30
        sh = Scheduler(1,self.check_reserves,bucle = True) 
        sh.start()

    """
    #######################################
             CONTROL RESERVES
    #######################################
    """

    def check_reserves(self,args = None):
        """
        Comprova les reserves actives i llença el threads  de timeout per finalitzar la reserva si no ve ningú
        """
        time_now = day_hour()
        Data = time_now[0]
        hora = datetime.datetime.now().strftime("%H:%M")
        maquines = models.get_all_machines_name()
        for i in maquines:    
            id_maquina = models.get_maquina_id(i[0])
            reserva = models.consulta_reserves(id_maquina,Data,hora)
            if reserva is not(None) and reserva !=-1:
                dia = reserva[4]
                hora = reserva[2]
                Reserva_feta = models.get_entra_reserva(id_maquina, Data,hora)
                if id_maquina not in self.reserves and Reserva_feta!=2 and Reserva_feta is not(None):
                    print("Control reserva per la maquina:",i[0],"iniciat a la hora:",hora)
                    self.reserves[id_maquina] = Scheduler(self.time_reserva, self.timeout_reserva, args = id_maquina)
                    self.reserves[id_maquina].start()
                else:
                    pass  # Reserve exists and threads runs
            
            else:   # Machine is not reserved 
                pass


    def cancel_timeout_reserva(self,id_maquina):
        """
        Cancel·la el thread de timeout per una reserva. L'event es dona quan l'usuari pasa la targeta
        """

        self.reserves[id_maquina].cancel()
        del self.reserves[id_maquina]
        print("Timeout reserva maquina",id_maquina,"stop")


    def timeout_reserva(self,id_maquina):
        """
        Finalitza una reserva de la màquina amb id_maquina
        """

        print("Finalitza reserva per timeout",id_maquina)
        time_now = day_hour()
        Data = time_now[0]
        hora = time_now[1]
        models.fin_reserva(hora,id_maquina,Data)
        models.entra_reserva(id_maquina,Data,hora,2)
        del self.reserves[id_maquina]


    """
    #######################################
             CONTROL EMERGENCIA
    #######################################
    """
    
    def set_emergency_timeout(self,maquina):
        """
        Estableix un thread de timer que executarà l'event per indicar l'emergencia de la maquina = 'maquina'
        """
        print("Set timout emergencia maquina:",maquina)
        id_maquina = models.get_maquina_id(maquina)
        self.emergencia[id_maquina] = Scheduler(self.timeout_emergencia,self.handle_timeout_emergencia,args= maquina)
        self.emergencia[id_maquina].start()

    def cancel_timeout_emergency(self,id_maquina):
        """
        Cancel·la el thread de timer de la màquina amb id='id_maquina'
        """
        if id_maquina in self.emergencia:
            print("Cancel timeout emergencia per la id_maquina",id_maquina)
            self.emergencia[id_maquina].cancel()
            del self.emergencia[id_maquina]


    def handle_timeout_emergencia(self,maquina):
        """
        Funció que s'executa quan es dona el timeout d'emergencia. Posa en emergencia la maquina: 'maquina'
        """
        print("Emergencia en la",maquina)
        models.canvia_estat_maquina(maquina,2)
        id_maquina = models.get_maquina_id(maquina)
        del self.emergencia[id_maquina]


    """
    #######################################
             CONTROL FI_RESERVA
    #######################################
    """

    def set_timeout_fi_reserva(self,id_maquina,time_timeout):
        """
        Estableix un thread de timer que executarà l'event per indicar el fi d'una reserva de la maquina = 'maquina'
        """
        if id_maquina  not in self.fi_reserves:
            print ("Set timeout fi reserva maquina:",id_maquina)
            self.fi_reserves[id_maquina] = Scheduler(time_timeout,self.handle_timeout_fi_reserva, args= id_maquina)
            self.fi_reserves[id_maquina].start()



    def cancel_timeout_fi_reserva(self,id_maquina):
        """
        Cancel·la el thread de timer de fi reserva de la maquina amb id='id_maquina'
        """
        if id_maquina in self.fi_reserves:
            print("Cancel fi reserva per la id_maquina",id_maquina)
            self.fi_reserves[id_maquina].cancel()
            del self.fi_reserves[id_maquina]

    

    def handle_timeout_fi_reserva(self,id_maquina):
        """
        Funció que s'executa quan es dona el timeout de fi reserva. Posa el final de la reserva de la maquina amb id_maquina='id_maquina'
        """
        print ("Finish reserva en la maquina",id_maquina)
        time_now = day_hour()
        Data = time_now[0]
        hora = time_now[1]
        models.fin_reserva(hora, id_maquina,Data)
        models.entra_reserva(id_maquina,Data,hora,2)
        max_aforament, aforament_actual = models.check_aforament()
        models.update_aforament(aforament_actual-1)
        del self.fi_reserves[id_maquina]


    """
    #######################################
             CONTROL COMUNICACIÓ
    #######################################
    """
    
    def set_comm_timeout(self,maquina):
        """
        Estableix un thread de timer que executarà l'event per indicar l'emergencia de no comunicacio de la maquina = 'maquina'
        """
        print("Set timout emergencia comunicacio maquina:",maquina)
        id_maquina = models.get_maquina_id(maquina)
        self.emergencia_comm[id_maquina] = Scheduler(self.time_emergencia_comm,self.handle_timeout_emergencia_comm,args= maquina)
        self.emergencia_comm[id_maquina].start()

    def cancel_timeout_emergency_comm(self,id_maquina):
        """
        Cancel·la el thread de timer de la màquina amb id='id_maquina'
        """
        if id_maquina in self.emergencia_comm:
            print("Cancel timeout emergencia comunicacio per la id_maquina",id_maquina)
            self.emergencia_comm[id_maquina].cancel()
            del self.emergencia_comm[id_maquina]


    def handle_timeout_emergencia_comm(self,maquina):
        """
        Funció que s'executa quan es dona el timeout d'emergencia de comunicacio. Posa en emergencia la maquina: 'maquina'
        """
        print("Emergencia en la",maquina,". Sense comunicacio")
        models.canvia_estat_maquina(maquina,2)
        id_maquina = models.get_maquina_id(maquina)
        del self.emergencia_comm[id_maquina]



def day_hour():
    """
    Retorna la data i la hora actual en el format de la bd.
    """
    Data = datetime.datetime.now().strftime("%Y-%m-%d")
    hora = datetime.datetime.now().strftime("%H:%M")
    return Data,hora



