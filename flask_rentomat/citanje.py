import serial
from serial.tools import list_ports
import codecs



ser = serial.Serial('/dev/myUSB', 9600, timeout=1)
enum_ports = enumerate(list_ports.comports())



with open('/home/pi/VSCProjects/selfrentacar/flask_rentomat/komanda.txt', 'w') as f:
               f.write("EMPTY,"+str(11))


return_data = {}
line_num = 0
hold = True

function_to_execute = "EMPTIED"
position = 11
while hold:


    receivedData = ser.readline()


    if len(receivedData) >= 1:
        line_num = line_num +1
        receive_hex = receivedData.hex().replace('0a', '')
        receive_hex_bytes = bytes(receive_hex, encoding='utf-8')
        binary_string = codecs.decode(receive_hex_bytes, "hex")
        sitrng_to_check = str(binary_string, 'utf-8')

        if line_num == 1:
            print("funcija je: ")
            print(sitrng_to_check.replace('\r', ''))
            print(function_to_execute)
            print(sitrng_to_check)
            return_data["function_send"] = function_to_execute

            if function_to_execute == sitrng_to_check.replace('\r', ''):
                return_data["function_status"] = "OK"
            else:
                return_data["function_status"] = "NO"

            return_data["function"] = sitrng_to_check.replace('\r', '')
         
        
        if line_num == 2:


            return_data["position_send"] = sitrng_to_check.split("Pozicija:",1)[1]

            if position == int(sitrng_to_check.split("Pozicija:",1)[1]):
                return_data["position_status"] = "OK"
            else:
                return_data["position_status"] = "NO"
            return_data["position"] = sitrng_to_check.split("Pozicija:",1)[1]
            hold = False
        
print(return_data)


