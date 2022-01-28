
from datetime import timedelta
import datetime


def check_hour(time_in,time_out,rol):

    hora_in = datetime.datetime.strptime(time_in, "%H:%M")
    hora_out =  datetime.datetime.strptime(time_out, "%H:%M")

    substract = hora_out-hora_in
    new_substract = int(substract.total_seconds())

    if rol =="client":
        return (new_substract/3600)>=1 and (new_substract/3600)<=2
    else:
        return (new_substract/3600)>=1 


def convert_second(time_in,time_out):

    hora_in = datetime.datetime.strptime(time_in, "%H:%M")
    hora_out =  datetime.datetime.strptime(time_out, "%H:%M")

    substract = hora_out-hora_in
    new_substract = int(substract.total_seconds())

    return new_substract


def avisador(time_in,time_out):

    hora_in = datetime.datetime.strptime(time_in, "%H:%M")
    hora_out =  datetime.datetime.strptime(time_out, "%H:%M")

    substract = hora_out-hora_in
    new_substract = int(substract.total_seconds())

    return new_substract<=300