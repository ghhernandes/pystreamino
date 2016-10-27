from app import *
import serial

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

    def __extract_sensor_data(self, value):
        #Valor recebido pelo arduino = sensor:NOME_SENSOR:VALOR_SENSOR
        #Ex: sensor:Temperatura:23.5
        data_list = value.split(':')
        if data_list[0] == "sensor":
            return [data_list[1], data_list[2]] #{NOME_SENSOR:VALOR_SENSOR}

    def add_sensor_data(self, name, value):
        if not (type(value) == float):
            print("Tipo de dados do sensor nao aceito. (Valor: {0})".format(value))
        elif self.__sensor_added(name):
            self.sensors[name].append(value)
        else:
            self.sensors[name] = [float(value)]

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

if __name__ == "__main__":
    g = ArduinoStreamGraph('teste', 9600)
    g.connect()
    print(g.isConnected)
