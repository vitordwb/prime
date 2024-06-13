import machine
import onewire, ds18x20
from library.Pins import *
import library.ufirebase as firebase
from machine import PWM, Pin
import math
import network
import json 
import utime
import urequests 
from time import localtime, mktime

class Wifi:
    
    """
        Este objeto tem como função conectar ao WiFi
        e publicar informações no banco de dados
    """
    
    def __init__(self):
        with open("./files/config.json","r") as connection_file:
            connection_content = json.loads(connection_file.read())             
            self.net_name      = connection_content["wifi"]["ssid"]
            self.password      = connection_content["wifi"]["password"]
            self.url_database  = connection_content["db"]["url"]
            self.db_topic      = connection_content["db"]["name"]
            connection_file.close()
         
        self.connected = False

    def connect(self: Wifi)->bool:
        """
            Conecta ao wifi e ao banco de dados
            utilizando as informações coletadas
            através do arquivo config.json
            
            Args:
                self (Wifi): O próprio objeto
            
            Returns:
                bool: O estado da conexão   
            
        """
        
        try:
            firebase.setURL(self.url_database)
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
            self.wlan.connect(self.net_name, self.password)
            
            while not self.wlan.isconnected():
                time.sleep(1)

            self.connected = True
            return self.connected 
        except:
            return False 

    def post_data(self,data:dict)->bool:
        """
            Posta informação no banco de dados que foi
            definido anteriomente no tópico do firebase
            que também está definido no arquivo config.json
            
            Args:
                self (Wifi): O próprio objeto
                data (dict): A informação que quer ser postada 
            
            Returns:
                bool: Estado da requisição
            
        """
        try:
            firebase.setURL(self.url_database)
            response = urequests.get('http://worldtimeapi.org/api/timezone/America/Sao_Paulo')
            data_json = response.json()

            datetime_str = data_json['datetime']
            datetime_str = datetime_str.split('.')[0]

            date_str, time_str = datetime_str.split('T')
            year, month, day = map(int, date_str.split('-'))
            hour, minute, second = map(int, time_str.split(':'))

            time_tuple = (year, month, day, hour, minute, second, 0, 0)

            local_time = localtime(mktime(time_tuple))

            formatted_time = "{:02d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                local_time[0] % 100,  # year
                local_time[1],        # month
                local_time[2],        # day
                local_time[3],        # hour
                local_time[4],        # minute
                local_time[5]         # second
            )
            firebase.patch("{}/{}".format(self.db_topic,formatted_time),data)
            return True
        except:
            return False 
    
    def check_connection(self: Wifi)->bool:
        """
            Checa o estado atual da conexão de wifi atual
            
            Args:
                self (Wifi): O próprio objeto
                
            Returns:
                bool: Estado da requisição
                
        """
        return self.wlan.isconnected()

class Fan:
    
    """
        Objeto que contém os dois ventiladores para
        serem controlados 
    """
    
    def __init__(self):
        self.fan_up_pin   = UP_FAN
        self.fan_down_pin = DOWN_FAN
        self.MAX = 0 
        return None
    
    def set_engine_speed(self: Fan,speed_percent:float)->float:
        """
            Baseado na porcentagem de entrada calcula os
            valores que serao inseridos no PWM
            
            Args:
                self (Fan): O próprio objeto 
                speed_percent (float): Porcentagem da velocidade requerida maxima de 0 a 100
                
            Returns:
                float: Velocidade em termos absolutos baseado na porcentagem máxima estabelecida 
            
            
        """
        speed = (lambda speed_percent: int((100 - speed_percent) / 100 * 1023))(speed_percent)
        return self.MAX if speed < self.MAX else speed
    
    def control_up_fan(self,state:int)->Tuple[bool,float | str]:
        """
            Controla a velocidade do ventilador superior
            que tem 3 estados: 10%, 70% e 0%
            
            Args:
                self (Fan): O próprio objeto
                state (int): O estado desejado do ventilador superior
                
            Returns:
                Tuple[bool,float | str]: A saúde do ventilador e o estado  
                    
        """
        try:
            if state == 2:
                self.fan_up_pin.duty(self.set_engine_speed(100))
                return (True,100)
            elif state == 1:
                self.fan_up_pin.duty(self.set_engine_speed(25))
                return (True,70)
            elif state == 0:
                self.fan_up_pin.duty(self.set_engine_speed(0))
                return (True,0)
        except Exception as e:
            return (False,str(e))

    def control_down_fan(self,state:int)->Tuple[bool,float | str]:
        """
            Controla a velocidade do ventilador
            inferior que tem 2 estados apenas: 100% e 0%
            
            Args:
                self (Fan): O próprio objeto
                state (int): O estado desejado do ventilador inferior 
            
            Returns 
                Tuple[bool,float | str]: A saúde do ventilador e o estado 
                
        """
        try:
            if state == 1:    
                self.fan_down_pin.duty(self.set_engine_speed(100))
                return (True,100)
            else:
                self.fan_down_pin.duty(self.set_engine_speed(70))
                return (True,0)
        except Exception as e:
            return (False,e)
        
class Porta:
    
    """
        Objeto que define a porta, a porta
        tem estados que servem para definir
        o estado dos ventiladores
    """

    def __init__(cls):
        cls.porta = DOOR_PIN
        return None
    
    @classmethod
    def check_porta_aberta(cls)->bool:
        """
            checa se a porta está aberta
            e com isso se a máquina de estados
            pode ou nao prosseguir
            
            Args:
                cls (Porta): O próprio objeto 
            
            Returns:
                bool: O estado da porta aberto ou fechado 
            
        """
        
        return (DOOR_PIN.value() == 1)

class Dumper:
    
    """
        O damper serve para controlar o fluxo
        de ar interno ao rack. Tem dois estados possíveis
        e conta com feedback dos sensores de fim de curso
        para checar sua saúde. 
    """
    
    def __init__(self):
        self.abertura = FIM_DE_CURSO_ABERTURA_PIN
        self.fechamento = FIM_DE_CURSO_FECHAMENTO_PIN
        self.dumper = DUMPER
        self.last_cycle = 0
        
        try:        
            with open("./files/cycles.txt","r") as file_cycle:
                self.cycle = int(file_cycle.read())
                file_cycle.close()
        except Exception as e:
            self.cycle = (False,str(e))
        
        return None 

    def increase_cycle(self)->bool:
        """
            Incrementa os ciclos de contagem do damper e
            escreve as informações no arquivo de ciclos
            
            Args:
                self (Dumper): O próprio objeto
            
            Returns:
                bool: A saúde do incremento do ciclo 
            
        """
        try:
            with open("./files/cycles.txt","w") as file_cycle:    
                self.cycle += 1
                file_cycle.write(str(self.cycle))
                file_cycle.close()
                return True 
        except Exception as e:
            print(e)
            return False 
            
    def get_cycle(self)->int:
        """
            Retorna a quantidade de ciclos atual
            
            Args:
                self (Dumper): O próprio objeto
                
            Returns:
                int: A quantidade de ciclos 
                
        """
        return self.cycle 
    
    def control(self,state:int)->Tuple[bool,float | str]:
        """
            Controla o dumper e depois espera
            pelo feedback do sistema para
            ver se o comando foi bem sucedido
            
            Args:
                self (Dumper): O próprio objeto
                state (int): O estado que se deseja mudar, 0 para fechado e 1 para aberto
            
            Returns:
                Tuple[bool,float | str]: A saúde do comando do dumper e o estado  
                        
        """    
        try:                                
            self.dumper.duty((state^1)*412)
            time.sleep(30)
            feedback_ = self.check_comando(state)
            if self.last_cycle != state:
                self.last_cycle = state     
                if feedback_ == True:
                    self.increase_cycle()
                return self.cycle
            elif feedback_ == False:
                return -1
            else:
                return self.cycle
            
        except Exception as e:
            print(e)
            return (False,str(e))

 
    def check_comando(self,state:int)->bool:
        """
            Checa se após o comando o dumper
            atingiu o fim de curso seja para abrir
            ou fechar
            
            Args:
                self (Dumper): O próprio objeto
                state (int): O estado atual do damper
                
            Returns
                bool: Caso o estado checado seja igual ao estado esperado no fim de curso 
            
        """
        if state == 0:
            return (self.fechamento.value() == 0)
        else:
            return (self.abertura.value() == 0)
    

class Temperatura:
    
    """
        A classe temperatura serve para medir
        a temperatura nos 3 pontos: interna, externa
        e cobre bem como saúde dos sensores
    """
    
    TEMP_PIN_INTERN = TEMP_PIN_INTERN
    TEMP_PIN_EXTERN = TEMP_PIN_EXTERN 
    TEMP_PIN_COPPER = TEMP_PIN_COPPER
        
    
    @classmethod
    def medir(cls,selection:str)->Tuple[bool, float|str]:
        """
            Mede a temperatura do sensor
            escolhido
            
            Args:
                self (Temperatura): O próprio objeto
                selection (str): O nome do sensor de temperatura
                
            
            Returns:
                Tuple[bool, float|str]: Retorna a saúde do sensor e o estado 
            
        """
        try:
            pin = {
                "interna":cls.TEMP_PIN_INTERN,
                "externa":cls.TEMP_PIN_EXTERN,
                "copper":cls.TEMP_PIN_COPPER
            }            
            ds_pin = pin[selection]
            ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
            roms = ds_sensor.scan()
            ds_sensor.convert_temp()
            for rom in roms:
                return (True,ds_sensor.read_temp(rom))
        except Exception as e:
            return (False,"error on measure of temperature ({}): {}".format(selection,str(e)))

class Corrente:
    
    """
        O objeto da corrente mede as 2 correntes(superior e
        inferior) e através da medição extrai outras informações
        que são derivadas dela como consumo de energia elétrica
    """
    
    CURRENT_PIN_1 = CURRENT_PIN_1
    CURRENT_PIN_2 = CURRENT_PIN_2
    sensores = {
        "corrente_cima":CURRENT_PIN_1,
        "corrente_baixo":CURRENT_PIN_2
    }
    OFFSET = 2.2559
    rede = 127
    
    @classmethod 
    def medir(cls,sensor:str)->Tuple[bool, Dict[str,float]|str]:
        """
            Mede a corrente utilizando os dois sensores
            de corrente de que o sistema é composto
            
            Args:
                cls (Corrente): O próprio objeto
                sensor (str): O nome do sensor que se quer monitorar
                
            Returns:
                Tuple[bool, Dict[str,float]|str]: Saúde do sensor e o estado, com os cálculos relevantes baseados na corrente
            
        """
        try:
            correnteRMS = 0
            correnteMax = 0
            correnteMin = 0
            UltimoS = 0
            energia = 0
            timer_Irms = time.ticks_ms()

            amostras = []
            i = 1
            tempo_atual = time.ticks_us()
            while time.ticks_diff(time.ticks_us(), tempo_atual) < 16667:
                corrente = (((((cls.sensores[sensor]).read() - 2048.0) / 4096.0) * 3.3 * 20.0) + cls.OFFSET)/2  # Ajuste de acordo com o sensor SCT
                amostras.append(corrente)
                i += 1

            # Calcula o nível médio
            correnteMax = 20.0
            correnteMin = -20.0
            for amostra in amostras:
                if amostra > correnteMax:
                    correnteMax = amostra
                if amostra < correnteMin:
                    correnteMin = amostra
            nMedio = (correnteMin + correnteMax) / 2.0

            # Remove o nível médio e calcula o somatório das amostras ao quadrado
            soma = 0
            for amostra in amostras:
                produto = amostra * amostra
                soma += produto

            # Calcula a média dos valores
            correnteRMS = soma / (i - 1)

            # Calcula a raiz quadrada
            correnteRMS = math.sqrt(correnteRMS)

            # Cálculo da potência aparente em kVA
            UltimoS = correnteRMS * cls.rede / 1000.0

            # Cálculo da potência em kW considerando FP = 0.8
            Ativa = UltimoS * 0.92

            # Cálculo do consumo de energia em kWh
            tempo_atual = time.ticks_ms()
            deltat = time.ticks_diff(tempo_atual, timer_Irms)
            timer_Irms = tempo_atual
            energia += (Ativa * deltat) / 3600.0 / 1000.0

            # Imprime os resultados
            
            return (True,{
                "corrente_rms":correnteRMS,
                "potencia_apa":UltimoS,
                "potencia_ativ":Ativa,
                "consumo":energia
            })
        except Exception as e:
            return (False,str(e)) 

class Rotacoes:

    """
        O objeto de rotações converte os pulsos
        para rotações e posteriormente mede amostragem
        de rotações em um determinado tempo 
    """

    time_span_seconds = 0.5
    up_speed_pin      = SPEED_MEASURE_PIN_UP
    down_speed_pin    = SPEED_MEASURE_PIN_DOWN
    speed_pins = {
        "measure_up":up_speed_pin,
        "measure_down":down_speed_pin
    }
    
    def pulses_to_rpm(pulses_count:int, ppr:int, time_interval_seconds:float)->float:
        """
            Converte pulsos medidos pelo sensor para rotações por minuto
                
            Args:
                pulses_count (int): Quantidade de pulsos contados
                ppr (int): Quantidade de pulsos por rotação
                time_interval_seconds  (float): Quanto tempo de amostragem dos pulsos 
            
            Returns:
                rpm (float): Quantidade de rotaçõe por minuto baseado nas informações de entrada
                
        """
        rpm = (60 / ppr ) / time_interval_seconds * pulses_count
        return rpm

    def measure_average(container:List[float])->float:
        """
            Faz a média de valores dado uma lista de entrada. Serve
            para verificar a média de uma medição uma amostra de rotações
            
            Args:
                container (List[float]): Amostragem de rotações por minuto
            
            Returns:
                float: Média das amostras, para maior precisão nas medidas finais 
            
        """
        return round(sum(container)/len(container),2)
    
    @classmethod
    def medir(cls,sensor_pin:str)->Tuple[bool, float|str]:
        """
            Mede as rotacoes dos dois motores
            em RPM
            
            Args:
                cls (Rotacoes): O Próprio objeto
                sensor_pin (str): Nome de qual sensor quer medir
            
            Returns:
                Tuple[bool, float|str]: Saúde e estado do sensor  
            
        """
        try:
            container = []
            media      = 0
            sensor_pin = cls.speed_pins[sensor_pin]
            for i in range(0,11):
                sensor = Pin(sensor_pin, Pin.IN)
                start_time = time.time()
                pulse_count = 0
                state       = 0
                while time.time() - start_time < cls.time_span_seconds:
                    if sensor.value() == 0 and state == 0:
                        state = 1
                        pulse_count += 1
                    elif sensor.value() == 1:
                        state = 0
                rpm = cls.pulses_to_rpm(pulse_count,1,cls.time_span_seconds)
                if len(container) >= 10:
                    media = cls.measure_average(container)
                    container = []
                else:    
                    container.append(rpm)
            return (True,media)
        except Exception as e:
            return (False,str(e))

class Device:

    """
        O objeto Device controla os 3 tipos de atuadores
        que tem no sistema e guarda os logs do comportamento
        dos 3 de modo a gerar os relatórios
    """

    def __init__(self):        
        self.fan    = Fan()
        self.dumper = Dumper()
        self.porta  = Porta()
        self.log = {}
        return None
    
    def start(self):
        return None
    
    def add_info(self,info:str)->bool:
        """
            Adiciona o log de entrada ao container
            self.log que irá registrar as ocorrencias
            ao tentar atuar sobre os equipamentos
            
            Args:
                self (Device): O próprio objeto 
                info (str): O log do estado atual dos objetos atuados
                
            Returns:
                bool: Saúde do registro das informações
            
        """
        try:
            self.log["state"] = info 
            return True 
        except:
            return False 
    
    def control_devices(self,ventilador_baixo:int, ventilador_cima:int, dumper_state:int)->Dict[str,Tuple[bool,float|str]]:
        """
            Controla todos os dispositivos
            que tem algum tipo de comando baseado
            nas entradas, ou seja nos estados
            
            Args:
                self (Device): O próprio objeto
                ventilador_baixo (int): Valor para comandar o ventilador inferior 
                ventilador_cima (int):  Valor para comandar o ventilador superior
                dumper_state (int): Valor para comandar o damper
            
            Returns:
                Dict[str,Tuple[bool,float|str]]: Cada estado e saúde dos equipamentos que foram comandados 
            
        """
        cima_status  = self.fan.control_up_fan(ventilador_cima)
        baixo_status   = self.fan.control_down_fan(ventilador_baixo)
        dumper_status = self.dumper.control(dumper_state)
        
        self.log = {
            "ventilador_cima_status":cima_status,
            "ventilador_baixo_status":baixo_status,
            "counter":dumper_status
        }
        
        return self.log

