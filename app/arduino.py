from app import *
import serial
import numpy
import matplotlib.pyplot as plt
from drawnow import *

class Arduino(object):
    def __init__(self, port, baud_rate):
        log.debug("Criando classe Arduino...")
        self.port = str(port)
        self.baud_rate = int(baud_rate)
        self.sensors = []
        self.serial = serial.Serial() #instancia para criar depois
        self.data = [] #todas informacoes recebidas

    # Property utilizada para verificar se esta conectado com o arduino via serial
    @property
    def isConnected(self):
        return self.serial.is_open

    def __sensor_added(self, name):
        try:
            self.sensors.keys().index(name)
            return True
        except ValueError as e:
            return False

    def add_sensor_data(self, name, value):
        if not self.__sensor_added(name):

    def add_data(self, str_value):
        self.data.append(str(str_value))

    def get_last_data(self):
        return self.data[-1]
    # Tenta conexao com o Arduino
    # Retorno: True/False
    def connect(self):
        log.debug("Tentando conectar com o Arduino...")
        self.disconnect()
        try:
            self.serial.baudrate = self.baud_rate
            self.serial.port = self.port
            self.serial.open()
            return self.serial.is_open
        except Exception as e:
            log.debug("Erro ao conectar com o Arduino.\n{0}".format(e))
            return False

    # Desconecta da porta serial
    def disconnect(self):
        if self.serial.is_open:
            log.debug("Desconectando do Arduino...")
            self.serial.close()
            log.debug("Desconectado.")

class ArduinoStreamGraph(Arduino):
    def __init__(self, port, baud_rate):
        super(ArduinoStreamGraph, self).__init__(port, baud_rate)
        self.title = "Arduino Streaming Data - TechWeek UNIFEV"
        self.plot = plt

    def start(self, limit=-1):
        count = 0
        if not self.isConnected:
            self.connect()
        self.plot.ion() #modo interativo para interacao em tempo real
        while True:
            while (self.serial.inWaiting()==0): # esperar ate possuir algo
                log.debug("Aguardando informacoes do arduino...")
                sleep(1000)

            self.add_data(self.serial.readline()) #obtem a string enviada pelo arduino
            self.add_sensor_data(self.get_last_data())

            if (limit > 0) and (count >= limit):
                break
            count += 1

if __name__ == "__main__":
    g = ArduinoStreamGraph('teste', 9600)
    g.connect()
    print(g.isConnected)
