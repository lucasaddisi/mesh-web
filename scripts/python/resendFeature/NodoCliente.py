from socket import *
import time,traceback
import json
import datetime
import informationPrinter as Printer

IP_LOCAL_NODE = '10.10.5.1'
UDP_PORT_Arduino = 8888
IP_NODO_MASTER= '10.10.5.5'
PUERTO_NODO_MASTER= 5005

list_stampers = [Printer.TimestampStamper(), Printer.IpStamper()]
json_stamper = Printer.InformationStamper(list_stampers)

def enviarUDP(IP,port,message):

    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.sendto(message, (IP, port))
    except:
        print("error")
        print(traceback.format_exc())
        return


def escucharMensajesArduino():

    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(("0.0.0.0", UDP_PORT_Arduino))#Sacar a archivo properties o como variable global
    except:
        print("error")
        print(traceback.format_exc())
        print("Reintentando...\n")
        time.sleep(5)
        escucharMensajesArduino()# Reintento Abrir socket
        return

    print("listo")

    while True:
        try:
            data,addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        except:
            print("error")
            escucharMensajesArduino()
            return
        # json decode
        json_data = json.loads(data.decode('utf-8'))
        # Ponerla la ip y el timestamp
        json_stamper.stamp_info(json_data)
        # Volver a codificar
        to_send = json.dumps(json_data)
        print(to_send)
        print("\nEnviando a NodoMaster...")
        enviarUDP(IP_NODO_MASTER,PUERTO_NODO_MASTER,to_send)

print("\n//////////NODO CLIENTE/////////\n")
escucharMensajesArduino()