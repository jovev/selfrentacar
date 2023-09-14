import time
import serial

ser = serial.Serial('/dev/myUSB', 9600, timeout=5)
komanda = 'HOME'
prazni = 'EMPTY'
pozicija = '5'
emptied = 'EMPTIED'
ready = 'READY'
uart_received = 'UART RECIVE...'
position_txt = 'Pozicija:'
ser.write(komanda.encode())
time.sleep(1)
checkRead = True
isReady = True


print('\nStatus -> ', ser)


data_in = ser.readline().decode("ascii")
print('pocetak')
print(data_in)
i=1



while checkRead:


    # print('data in 0 -4')
    # print(data_in[0:4])
    # print('rady 0 - 4')
    # print(ready[0:4])

    i=i+1
    if ser.inWaiting() > 0:
        data_in = ser.readline()
        print("Procitano O",data_in)
    if data_in[0:4] == ready[0:4]:
        checkRead = False
    if i==100:
        checkRead = False 


#ser.close()
while "1==1":
    # 
    #  = ser.readline()

    
    # print("\nPrvi print",data_in, i)
    # print('prvi karakteri')
    # print(data_in[0:5]
    # print(ready[0:5])

    if data_in[0:5] == ready[0:5]:
        print("Uneti broj koripice")
        ser.write(prazni.encode())
        time.sleep(1)
        #data_in = ser.readline().decode("ascii")
       # print("UART - ", data_in)
        print("Pozicija:: ")
        print(str(pozicija))


        
        ser.write(5)
        data_in = ser.readline().decode("ascii")
        print("Procitano 1 pre",data_in)
        data_in = ser.readline()
        print("Procitano 1 posle",data_in)

    
        if data_in[0:6] == emptied[0:6]:
            print("Procitano 2 emptied",data_in)
            data_in = ser.readline().decode("ascii")
            if data_in[0:8] == position[0:8]:
                print("Procitano 3 pozicija",data_in[9])
                data_in = ser.readline().decode("ascii")
                if data_in[0:4] == ready[0:4]:
                    print("Procitano 4 ready",data_in)
                    data_in = ser.readline().decode("ascii")
                    # isReady = False
                
        pozicija = input("Unesi poziciju korpice")
    else:
        print("Ode na else ")
        if ser.inWaiting() >= 0:
            data_in = ser.readline().decode("ascii")
            print("Procitano else ",data_in)
        # print("Cekamo READY")

    # time.sleep(1)
ser.close()




# import time
# import serial

# ser = serial.Serial('/dev/myUSB', 115200, timeout=25)

# print("Starting program")

# # ser = serial.Serial("/dev/ttyUSB", baudrate=9600,
# parity=serial.PARITY_NONE,
# stopbits=serial.STOPBITS_ONE,
# bytesize=serial.EIGHTBITS
# time.sleep(1)

# start_r ='HOME REQ...'
# komanda = 'HOME'
# ready = 'READY'
# prazni = 'EMPTY'
# pozicija = '5'






# def read_rentomat(komanda, pozicija):
#    while 1:
      
#       while ser.in_waiting:
#          try:
#             data_in = ser.readline().decode("ascii")
#          except:
#             print("Ispao na readline")
#             # ser.reset_output_buffer()
#             # ser.reset_input_buffer
#             time.sleep(5)

#          # for character in data_in:
#             # print(character, character.encode('utf-8').hex())


#          if data_in[0:10] == start_r[0:10]:
#                ser.write(komanda.encode())
#                print("Izdata komanda HOME")
#                f.write("Nesto Drugo")
#                time.sleep(5)
               

#          if data_in[0:4] == ready[0:4]:
#                print("*******   Spreman za sledecu komandu")

#                # komanda=input('Unesi Komandu EMPTY ili FILL:')
#                if komanda == "EMPTY":
#                   # pozicija=input("unesi poziciju korpice:")


#                   ser.write(prazni.encode())

#                   time.sleep(1)
#                   ser.write(pozicija.encode())
#                   print("Izdata komanda EMPTY")
#                   time.sleep(5)
                  
# while (1==1):
#     with open("/var/komanda.txt","r+") as f:
#         contents = f.readlines()
#         print (contents)
#         read_rentomat(contents[0], pozicija)