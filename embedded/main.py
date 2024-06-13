from library.Core_v3 import *
import time
import utime
import urequests
from time import localtime, mktime

def state_machine(temp_interna, temp_externa,counter, d):
    porta_aberta = Porta.check_porta_aberta()
    if not porta_aberta:
        if temp_interna <= 15:
            d.control_devices(0, 2, 0)
            d.add_info("TEMPERATURA MUITO BAIXA")
            return
        elif temp_interna >= 40:
            d.control_devices(0, 2, 1)
            d.add_info("TEMPERATURA MUITO ALTA")
            return
        
        if temp_interna >= 35:
            if temp_externa < temp_interna:
                d.control_devices(0, 1, 1)
                d.add_info("TEMPERATURA MUITO ALTA")
                return 
            else:
                d.control_devices(0, 2, 0)
                d.add_info("TEMPERATURA INTERNA E EXTERNA MUITO ALTA")
                return  
         
        if temp_externa >= 23:
            if temp_interna >= 29:
                d.control_devices(1, 2, 0)
                d.add_info("OPERACAO NORMAL")
                return 
            elif temp_interna <= 26:
                d.control_devices(0, 1, 0)
                d.add_info("OPERACAO NORMAL")
                return 
        else:
            if temp_interna >= temp_externa:
                if temp_interna >= 25.5:
                    d.control_devices(0, 2, 1)
                    d.add_info("OPERACAO NORMAL")
                    return 
                elif temp_interna <= 23:
                    d.control_devices(0, 1, 0)
                    d.add_info("OPERACAO NORMAL")
                    return 
            else:
                if temp_interna > 15:
                    d.control_devices(0, 1, 0)
                    d.add_info("TEMPERATURA ABAIXANDO")
                    return 
                else:
                    d.add_info("TEMPERATURA MUITO BAIXA")
                    return
    else:
        d.control_devices(0,0,0)
        d.add_info("PORTA ABERTA")

def mini_state_machine(temp_interna,temp_externa,counter,d):
    porta_aberta = Porta.check_porta_aberta()
    if not porta_aberta: # valiadado
        if temp_interna <= 15:
            d.control_devices(0,1,0)
            d.add_info("TEMPERATURA MUITO BAIXA")
            return 
        elif temp_interna > 40:
            d.control_devices(1,2,1)
            d.add_info("TEMPERATURA MUITO ALTA")
            return 
        else:
            if temp_externa > 35 and temp_interna > temp_externa and temp_interna <= 40:
                d.control_devices(2,2,0)
                d.add_info("TEMPERATURA INTERNA E EXTERNA MUITO ALTA")
            elif 23 <= temp_externa <= 35 and 26 < temp_interna <= 29:
                d.control_devices(1,2,0) 
                d.add_info("OPERACAO NORMAL DE RESFRIAMENTO")
            elif 23 <= temp_externa <= 35 and temp_interna <= 26:
                d.control_devices(0,1,0)
                d.add_info("OPERACAO NORMAL")
            elif 15 < temp_externa < 23 and temp_interna > temp_externa:
                d.control_devices(0,2,1)
                d.add_info("TENTATIVA DE FREE COOLING")
            
    else:
        d.control_devices(0,0,0)
        d.add_info("PORTA ABERTA")
    

def main():
    try:
        d = Device()
        wifi = Wifi()
        wifi.connect()
        while True:
            # Capta o horário atual 
            current_time = utime.time()
            time_tuple = utime.localtime(current_time)
            formatted_time = "2024-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format( 
                time_tuple[1],        # month
                time_tuple[2],        # day
                time_tuple[3],        # hour
                time_tuple[4],        # minute
                time_tuple[5]         # second
            )
            
            """
                Capta as informações relativas aos sensores que são necessários
                para todas as decisões a seguir 
            """
            
            (state_corrente_cima,info_corrente_cima)   = Corrente.medir("corrente_cima")
            (state_corrente_baixo,info_corrente_baixo) = Corrente.medir("corrente_baixo")

            (state_rpm_cima,info_rpm_cima)   = Rotacoes.medir("measure_up")
            (state_rpm_baixo,info_rpm_baixo) = Rotacoes.medir("measure_down")
            
            (state_interna,info_interna) = Temperatura.medir("interna")
            (state_externa,info_externa) = Temperatura.medir("externa")
            (state_copper,info_copper)   = Temperatura.medir("copper")
            
            # Para testes apenas 
            #info_interna = float(input("temperatura interna: "))
            #info_externa = float(input("temperatura externa: "))
            
            
            """
                Checa se todos os sensores estão com saúde. Se todos estiverem com
                saúde a máquina de estados é inicializada
            """
            if all([state_interna,state_externa,state_copper]):
                mini_state_machine(info_interna, info_externa, 1, d)
                
            """
                A seguir são as informações relativas a todos os sensores
                que foram captados após a inicalização de uma rodada da
                máquina de estados 
            """
            data = {
                "corrente_cima":(state_corrente_cima,info_corrente_cima),
                "corrente_baixo":(state_corrente_baixo,info_corrente_baixo),
                "rpm_cima":(state_rpm_cima,info_rpm_cima),
                "rpm_baixo":(state_rpm_baixo,info_rpm_baixo), 
                "temperatura_interna":(state_interna,info_interna),
                "temperatura_externa":(state_externa,info_externa),
                "temperatura_cobre":(state_copper,info_copper),
                "datetime":formatted_time
            }
            
            """
                Após isso junta as informações de sensores
                com a informação da saúde dos atuadores depois de ja
                terem sido atuados e as publica no banco de dados
            """
            
            data = data | d.log
            
            print(data)
            
            while not wifi.check_connection():
                wifi.connect()
                time.sleep(2)
            else:
                wifi.post_data(data)
        
            time.sleep(5)
            
    except Exception as e:
        print(e)
        time.sleep(5)
        pass
    except OSError as os_error:
        print(e)
        time.sleep(5)
        pass
        
if __name__ == "__main__":
    main()

# --------------------------

