import time
import serial

ser = serial.Serial('/dev/myUSB', 9600, timeout=5)



komanda = 'HOME'
empty = 'EMPTY'
# empty_pos = '2'
fill = 'FILL'
fill_pos = '5'


while 1==1:

    with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/komanda.txt", "r") as komanda_fajl:
        komanda_text = komanda_fajl.readline()
        print(komanda_text)


    if(komanda_text != ""):
        if(komanda_text != "HOME"):
            result = [x.strip() for x in komanda_text.split(',')]

            komanda_text = result[0]
            empty_pos = result[1]

            print(komanda_text)
            print(empty_pos)
            

    if(komanda_text == 'HOME'):
        ser.write(komanda.encode())
        with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/komanda.txt", "w") as komanda_fajl:
           komanda_fajl.write("") 
    if(komanda_text == 'EMPTY'):
        ser.write(empty.encode())
        time.sleep(2)
        ser.write(empty_pos.encode())
        with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/komanda.txt", "w") as komanda_fajl:
           komanda_fajl.write("") 

    if(komanda_text == 'FILL'):
        ser.write(fill.encode())
        time.sleep(2)
        ser.write(fill_pos.encode())
        with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/komanda.txt", "w") as komanda_fajl:
           komanda_fajl.write("") 

    #if(komanda_text == ""):
        
    time.sleep(2)
