# socket_echo_client.py
import binascii
import socket
import sys
import time

send_dict = { "identifier" : "3030",
    "terminalID" : "3030",
    "sourceID" : "3030",
    "sequentialNumber" : "30303031",
    "transactionType" : "3031",
    "printerFlag" : "30",
    "cashierID" : "3030",
    "transactionNumber" : "",
    "fieldSeparator1" : "1C",
    "transactionAmount1" : "31",
    "fieldSeparator2" : "1C",
    "fieldSeparator3" : "1C",
    "amountExponent" : "2B30",
    "fieldSeparator4" : "1C",
    "amountCurrency" : "393431",
    "fieldSeparator5" : "1C",
    "fieldSeparator6" : "1C",
    "fieldSeparator7" : "1C",
    "fieldSeparator8" : "1C",
    "authorizationCode" : "",
    "fieldSeparator9" : "1C",
    "fieldSeparator10" : "1C",
    "fieldSeparator11" : "1C",
    "inputLabel" : "",
    "fieldSeparator12" : "1C",
    "insurancePolicyNumber" : "",
    "fieldSeparator13" : "1C",
    "installmentsNumber" : "",
    "fieldSeparator14" : "1C",
    "minimumInputLenght" : "",
    "maximumInputLenght" :"",
    "maskInputData" : "",
    "fieldSeparator15" : "1C",
    "languageID" : "3030",
    "fieldSeparator16" : "1C",
    "printData" : "",
    "fieldSeparator17" : "1C",
    "cashierID2" : "",
    "fieldSeparator18" : "1C",
    "transactionAmount2" : "",
    "fieldSeparator19" : "1C",
    "payservicesData" : "",
    "fieldSeparator20" : "1C",
    "transactionActivationCode" : "",
    "fieldSeparator21" : "1C",
    "instantPaymentReference" : "",
    "fieldSeparator22" : "1C",
    "qrCodeData" : "",
    "fieldSeparator23" : "1C",
    "specificProcessingFlag" : "",
    "fieldSeparator24" : "1C",
    "random_transportationSpecificData" : ""
}




receive_dict = { "identifier" : "10",
    "terminalID" : "",
    "sourceID" : "",
    "sequentialNumber" : "",
    "transactionType" : "",
    "transactionFlag" : "02",
    "transactionNumber" : "",
    "batchNumber" : "",
    "transactionDate" : "",
    "transactionTime" : "",
    "fieldSeparator1" : "",
    "transactionAmount1" : "",
    "fieldSeparator2" : "",
    "fieldSeparator3" : "",
    "amountExponent" : "+0",
    "fieldSeparator4" : "",
    "amountCurrency" : "705",
    "fieldSeparator5" : "",
    "cardDataSource" : "",
    "fieldSeparator6" : "",
    "cardNumber" : "",
    "fieldSeparator7" : "",
    "expirationDate" : "",
    "fieldSeparator8" : "",
    "fieldSeparator9" : "",
    "fieldSeparator10" : "",
    "authorizationCode" : "",
    "fieldSeparator11" : "",
    "tidNumber" : "",
    "fieldSeparator12" : "",
    "midNumber" : "",
    "fieldSeparator13" : "",
    "companyName" : "",
    "fieldSeparator14" : "",
    "fieldSeparator15" : "",
    "fieldSeparator16" : "",
    "fieldSeparator17" : "",
    "fieldSeparator18" : "",
    "fieldSeparator19" : "",
    "fieldSeparator20" : "",
    "displayMessage" : "",
    "fieldSeparator21" : "",
    "fieldSeparator22" : "",
    "inputData" : "",
    "fieldSeparator23" : "",
    "emvData" : "",
    "fieldSeparator47" : "",
    "signatureLinePrintFlag" : "",
    "fieldSeparator48" : "",
    "acquirerName" : "",
    "debitTransactionCount" : "",
    "debitTransactionAmount" : "",
    "refundTransactionCount" : "",
    "refundTransactionAmount" : "",
    "fieldSeparator49" : "",
    "moreMessagesFlag" : "",
    "fieldSeparator50" : "",
    "installmentsNumber" : "",
    "fieldSeparator51" : "",
    "fullResponseCode" : "",
    "fieldSeparator52" : "",
    "transactionStatus" : "",
    "fieldSeparator53" : "",
    "spdhTerminalTotals" : "",
    "fieldSeparator54" : "",
    "spdhHostTotals" : "",
    "fieldSeparator55" : "",
    "pinBlock" : "",
    "fieldSeparator56" : "",
    "cardholderName" : "",
    "fieldSeparator57" : "",
    "rrn" : "",
    "fieldSeparator58" : "",
    "pinFlag" : "",
    "fieldSeparator59" : "",
    "transactionAmount2" : "",
    "fieldSeparator60" : "",
    "payservicesData" : "",
    "fieldSeparator61" : "",
    "availableBalance" : "",
    "fieldSeparator62" : "",
    "offlineCryptogram" : "",
    "fieldSeparator63" : "",
    "loyaltyData" : "",
    "fieldSeparator64" : "",
    "formattedTextToPrint" : "",
    "fieldSeparator65" : "",
    "dccNumber" : "",
    "fieldSeparator66" : "",
    "dccProvider" : "",
    "fieldSeparator67" : "",
    "dccExchangeRate" : "",
    "fieldSeparator68" : "",
    "dccExchangeRateDate" : "",
    "fieldSeparator69" : "",
    "dccMarkUpPercent" : "",
    "fieldSeparator70" : "",
    "dccAmount" : "",
    "fieldSeparator71" : "",
    "dccDisclaimer" : "",
    "fieldSeparator72" : "",
    "dccStatus" : "",
    "fieldSeparator73" : "",
    "dccCurrencySymbol" : "",
    "fieldSeparator74" : "",
    "instantPaymentReference" : "",
    "fieldSeparator75" : "",
    "personal_vehicleCardData" : "",
    "fieldSeparator76" : "",
    "mifareCardType" : "",
    "fieldSeparator77" : "",
    "mifareCardUID" : "",
    "fieldSeparator78" : "",
    "f4gCode" : "",
    "fieldSeparator79" : "",
    "radcom_transportationSpecificData" : "",
    "fieldSeparator80" : "",
    "acquirerId" : "",
    "fieldSeparator81" : "",
    "transactionID" : "",
    "fieldSeparator82" : "",
}
STX = "02"
ETX = "03"
EOT = "04"
ACK = "06"
NACK = "15"


message_data = ""

# message_data = STX+STX

def xor_sum(input_data):
    input_data_lenght = len(input_data)
    # print(input_data)
    lrc = ord(str(input_data[0:1]))
    for i in range(2, input_data_lenght-1, 1):
        # print(ord(str(input_data[i:i+1])))
    
        lrc ^= ord(str(input_data[i:i+1]))

    return 24

for key in send_dict:
    
    message_data = str(message_data) + str(send_dict[key])



message_data = message_data + str(ETX)
ack_message_data_tmp = ACK + ETX
nack_message_data_tmp = NACK + ETX

lrc = xor_sum(message_data)

lrc_ack = xor_sum(ack_message_data_tmp)
lrc_nack = xor_sum(nack_message_data_tmp)


message_data = STX+STX+message_data+str(lrc)
ack_message_data = STX+STX+ack_message_data_tmp+str(lrc_ack)
nack_message_data = STX+STX+nack_message_data_tmp+str(12)






# message1 = binascii.hexlify(b'0202000000000001000281002828+028RSD28282828282828Labelce2828280120028002828282828282828282828280339')


# for_test = bytes(message_data, encoding="ascii")


# print(bytes(message_data, "utf-8").hex())




S_TCP_IP = "127.0.0.1"
S_TCP_PORT = 3000



TCP_IP = '192.168.1.113'    
TCP_PORT = 3000   

sock_payten = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_payten.connect((TCP_IP, TCP_PORT))

sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.bind((S_TCP_IP, S_TCP_PORT))




# print("cock.connect=")
# print(con)
# print(message_data)
# print(type(message_data))


str_to_send = "02023030303030303030303030313030301C311C1C2B301C3934311C1C1C1C1C1C1C1C1C1C1C30301C1C1C1C1C1C1C1C1C0324"
dobar_format = bytearray.fromhex("02023030303030303030303030313030301C311C1C2B301C3934311C1C1C1C1C1C1C1C1C1C1C30301C1C1C1C1C1C1C1C1C0324").decode()

print(bytearray.fromhex("02023030303030303030303030313030301C311C1C2B301C3934311C1C1C1C1C1C1C1C1C1C1C30301C1C1C1C1C1C1C1C1C0324"))
print(bytearray.fromhex(message_data))
print("-----------")
print(bytes(message_data, encoding='iso-8859-2'))
print("-----------")
print("????????????????")
print(dobar_format)
print("????????????????")

i = 1

try:
    
    
    for i in range(1):
# 3030303030303030303130313030303238302e3031323832382b30323852534432383238323832383238323832384c6162656c63653238323832383031323030323830303238323832383238323832383238323832383238323832383238
# 303230323030303030303030303030313030303238313030323832382b30323852534432383238323832383238323832384c6162656c636532383238323830313230303238303032383238323832383238323832383238323832383238323830333339

# 02023030303030303030303030313030301C 31          1C1C2B30 1C 393431 1C1C1C1C1C1C1C1C1C1C1C 3030 1C1C1C1C1C1C1C1C1C        03 24
# 02023030303030303030303130313030301C 31          1C1C2b30 1C 393431 1C1C1C1C1C1C1C1C1C1C1C 3030 1C1C1C1C1C1C1C1C1C        03 24

        # Send data
        # message1 = binascii.hexlify('0202000000000001000281002828+028RSD28282828282828Labelce2828280120028002828282828282828282828280339')

        # message1=02023030303030303030303030313030301C311C1C2B301C3934311C1C1C1C1C1C1C1C1C1C1C30301C1C1C1C1C1C1C1C1C0324
        # message = str.encode(message_data)
        # print(binascii.hexlify(message_data).encode())
        # print(message_data)

        
        # sent = sock.sendto(dobar_format)






        # print("Pre try poslato= ")
        # print(sent)



        sent = sock_payten.sendto(bytes(dobar_format, encoding='iso-8859-2'),(TCP_IP,TCP_PORT))

        data = sock_server.recvfrom(1024)
        print("************")
        print("Data recived: ")
        print(data)
        print("************")

        exit


        # try: 

        #     print("uso u try")

        #     data = ""
        #     data, ip= sock_server.recvfrom(1024)
        #     print(data)
        #     print(ip)
        #     if not data:
        #         print("ispao na timeout ack")  
        #     else:    
        #         received_data = binascii.hexlify(data).decode()
        #         print("received_data 1: "+received_data)
        #         if(received_data == ACK):
        #             print("Primio je ACK")


        #             data = sock_rcv.recvfrom(1024)
        #             received_data = binascii.hexlify(data).decode()
        #             print("Primljeno posle ACK"+received_data)
        #             print(data)

        #             break
        #         else:
        #             print("nije primio ACK")
        # except:
        #     # time.sleep(5)
        #     ++i
    

    

    # try: 
    #     print("izaso na break")
    #     data, ip = sock_rcv.recvfrom(1024)
    #     print(data)
    #     print(ip)
    #     received_data = binascii.hexlify(data).decode()
    #     print(received_data)
        
    #     # while True:
    #     #     send_nack = sock.send(b'15')
    #     #     data = sock.recv(1024)
    #     #     received_data = binascii.hexlify(data)
    #     #     print(received_data)

    #     #     if received_data:
    #     #         print("Primljeno u while "+received_data)
    #     #         break
    # except:
        
    #     print("Except primljen data")
        
        
 
except:
    print("Ode na except")




finally:




    # print(format(data))
    print('closing socket')
    # sock.close()







# s = socket.socket()
# address = '91.239.151.91'
# port = 21202 


# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)






# message = 'ALO'

# lrc = 0
# for b in message[1:]:
#     print(b)
#     lrc ^= int(b)

# print(lrc)


# try:
#     s.connect((address, port)) 
#     s.send(final_message)
#     data = s.recv(1024)
#     s.close()
#     print('Received', repr(data))
# except Exception as e: 
#     print("something's wrong with %s:%d. Exception is %s" % (address, port, e))
# finally:
#     s.close()








# print(sock)
# # data = sock.recv(1024)
# # print(data)

# message = b'00'

# sent = sock.send(message)
# print(sent)
# # data = sock.recv(2)
# # print(data)



# while True:
#     data = con.recv(2048)
#     if not data: 
#         break
#     print(data)
#     con.send(b"<Server> Got your data. Send some more\n")










