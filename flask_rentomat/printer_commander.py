import os
import binascii







f = open("file_name.txt", "wb")
set_bold1  = bytearray.fromhex("1B4501")

s = "Boldiran tekst"
line = bytearray()
line.extend(map(ord, s))


s_br = bytearray.fromhex("1013")
line_br = bytearray()
line_br.extend(map(ord, s_br))


unset_bold  = bytearray.fromhex("1B4500")
#line2 = binascii.hexlify("Neboldiran tekst")

f.write("0x1D 0x28 0x6B 0x03 0x00 0x30 0x41 0x03")
# f.write(set_bold1)
# f.write(line_br)
# f.write(line)
# f.write(line_br)
# f.write(unset_bold)
#f.write(line2)

# print(f.read())
f.close()
os.system("lp file_name.txt")


# import time
# import serial

# ser = serial.Serial('/dev/usb/lp0', 9600, timeout=5)

# komanda = 'HOME'


# ser.write(komanda.encode())

# time.sleep(1)
# checkRead = True
# isReady = True


# print('\nStatus -> ', ser)


# data_in = ser.readline().decode("ascii")
# print('pocetak')
# print(data_in)
# i=1



# while checkRead:


#     # print('data in 0 -4')
#     # print(data_in[0:4])
#     # print('rady 0 - 4')
#     # print(ready[0:4])

#     i=i+1
#     if ser.inWaiting() > 0:
#         data_in = ser.readline()
#         print("Procitano O",data_in)
#     if data_in[0:4] == ready[0:4]:
#         checkRead = False
#     if i==100:
#         checkRead = False 


# #ser.close()
# while "1==1":
#     # 
#     #  = ser.readline()

    
#     # print("\nPrvi print",data_in, i)
#     # print('prvi karakteri')
#     # print(data_in[0:5]
#     # print(ready[0:5])

#     if data_in[0:5] == ready[0:5]:
#         print("Uneti broj koripice")
#         ser.write(prazni.encode())
#         time.sleep(1)
#         #data_in = ser.readline().decode("ascii")
#        # print("UART - ", data_in)
#         print("Pozicija:: ")
#         print(str(pozicija))


        
#         ser.write(5)
#         data_in = ser.readline().decode("ascii")
#         print("Procitano 1 pre",data_in)
#         data_in = ser.readline()
#         print("Procitano 1 posle",data_in)

    
#         if data_in[0:6] == emptied[0:6]:
#             print("Procitano 2 emptied",data_in)
#             data_in = ser.readline().decode("ascii")
#             if data_in[0:8] == position[0:8]:
#                 print("Procitano 3 pozicija",data_in[9])
#                 data_in = ser.readline().decode("ascii")
#                 if data_in[0:4] == ready[0:4]:
#                     print("Procitano 4 ready",data_in)
#                     data_in = ser.readline().decode("ascii")
#                     # isReady = False
                
#         pozicija = input("Unesi poziciju korpice")
#     else:
#         print("Ode na else ")
#         if ser.inWaiting() >= 0:
#             data_in = ser.readline().decode("ascii")
#             print("Procitano else ",data_in)
#         # print("Cekamo READY")

#     # time.sleep(1)
# ser.close()

