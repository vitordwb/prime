from machine import Pin, PWM , ADC 
import onewire, ds18x20, time
import ujson

"""
    Aqui vao todas as variaveis que se 
    referem a pinagem dos componentes.
    Modular em um arquivo separado permite que
    caso os pinos mudem fique mais 
    simples de fazer as modificações
"""

with open("./files/pin_config.json","r") as pin_config:
    pin = ujson.loads(pin_config.read())

"""
    Aqui capta primiero os números dos pinos
    para cada atuador e sensor. 
"""

DUMPER_PIN        = int(pin["DUMPER"])
UP_FAN_PIN        = int(pin["UP_FAN"])
DOWN_FAN_PIN      = int(pin["DOWN_FAN"])
TEMP_PIN_INTERN   = int(pin["TEMP_PIN_INTERN"])
TEMP_PIN_EXTERN   = int(pin["TEMP_PIN_EXTERN"])
TEMP_PIN_COPPER   = int(pin["TEMP_PIN_COPPER"])
CURRENT_PIN_1     = int(pin["CURRENT_PIN_1"])
CURRENT_PIN_2     = int(pin["CURRENT_PIN_2"])
SPEED_MEASURE_PIN_UP   = int(pin["SPEED_MEASURE_PIN_UP"])
SPEED_MEASURE_PIN_DOWN = int(pin["SPEED_MEASURE_PIN_DOWN"])
DOOR_PIN          = int(pin["DOOR_PIN"])

FIM_DE_CURSO_ABERTURA_PIN = int(pin["FIM_DE_CURSO_ABERTURA"])
FIM_DE_CURSO_FECHAMENTO_PIN = int(pin["FIM_DE_CURSO_FECHAMENTO"])

"""
    Depois converte cada número em um tipo de saida
    correspondente ao tipo necessário para fazer
    a captação das informações ou a atuação 
"""

DUMPER             = PWM(Pin(DUMPER_PIN),5000)
UP_FAN             = PWM(Pin(UP_FAN_PIN),5000)
DOWN_FAN           = PWM(Pin(DOWN_FAN_PIN),5000)

TEMP_PIN_INTERN   = Pin(TEMP_PIN_INTERN, Pin.IN)
TEMP_PIN_EXTERN   = Pin(TEMP_PIN_EXTERN, Pin.IN)
TEMP_PIN_COPPER   = Pin(TEMP_PIN_COPPER, Pin.IN)
CURRENT_PIN_1     = ADC(Pin(CURRENT_PIN_1, Pin.IN))
CURRENT_PIN_2     = ADC(Pin(CURRENT_PIN_2, Pin.IN))

CURRENT_PIN_1.atten(ADC.ATTN_11DB)  
CURRENT_PIN_1.width(ADC.WIDTH_12BIT)  

CURRENT_PIN_2.atten(ADC.ATTN_11DB)  
CURRENT_PIN_2.width(ADC.WIDTH_12BIT)  

SPEED_MEASURE_PIN_UP   = Pin(SPEED_MEASURE_PIN_UP, Pin.IN)
SPEED_MEASURE_PIN_DOWN = Pin(SPEED_MEASURE_PIN_DOWN, Pin.IN)

DOOR_PIN                    = Pin(DOOR_PIN)
FIM_DE_CURSO_ABERTURA_PIN   = Pin(FIM_DE_CURSO_ABERTURA_PIN, Pin.IN)
FIM_DE_CURSO_FECHAMENTO_PIN = Pin(FIM_DE_CURSO_FECHAMENTO_PIN, Pin.IN)



# eof 

# --------------------------

