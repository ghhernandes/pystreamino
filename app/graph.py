from app import log, arduino
import numpy
import matplotlib.pyplot as plt
from drawnow import *

class ArduinoStreamGraph(arduino.Arduino):
    def __init__(self, port, baud_rate):
        super(ArduinoStreamGraph, self).__init__(port, baud_rate)
        self.title = "Arduino Streaming Data - TechWeek UNIFEV"
        self.plot = plt

    def start(self, limit=-1):
        count = 0
        if not self.isConnected:
            self.connect()
        self.plot.ion() #modo interativo para atualizar grafico em tempo real
        while True:
            while (self.serial.inWaiting()==0): # esperar ate possuir algo
                log.debug("Aguardando informacoes do arduino...")
                sleep(1000)

            self.add_data(self.serial.readline()) #obtem a string enviada pelo arduino

            sensor_data_list = self.__extract_sensor_data(self.get_last_data())
            self.add_sensor_data(sensor_data_list[0], sensor_data_list[1]) #adiciona o valor para o sensor

            if (limit > 0) and (count >= limit):
                break
            count += 1
