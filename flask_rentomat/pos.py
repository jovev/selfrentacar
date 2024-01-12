# socket_echo_client.py
import binascii
import socket
import sys
import time

send_dict = { "identifier" : "3030",
    "terminalID" : "3030",
    "sourceID" : "3030",
    "sequentialNumber" : "30303030",
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

        my_hexdata = ord(str(input_data[i:i+1]))
        scale = 16
        # final = bin(int(my_hexdata, scale))[2:]
        # print(final)
        # print(input_data[i:i+1])
        lrc ^= ord(str(input_data[i:i+1]))
    return lrc

for key in send_dict:
    
    message_data = str(message_data) + str(send_dict[key])



message_data = message_data + str(ETX)
ack_message_data_tmp = ACK + ETX
nack_message_data_tmp = NACK + ETX

lrc = xor_sum(message_data)
print(message_data)
# print(str(message_data[0:2]))





# print(final)
# lrc_ack = xor_sum(ack_message_data_tmp)
# lrc_nack = xor_sum(nack_message_data_tmp)


message_data = STX+STX+message_data+str(lrc)
# ack_message_data = STX+STX+ack_message_data_tmp+str(lrc_ack)
# nack_message_data = STX+STX+nack_message_data_tmp+str(12)






S_TCP_IP = '192.168.1.101'  
S_TCP_PORT = 3000



TCP_IP = '192.168.1.113'    
TCP_PORT = 3000   

sock_payten = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
status = sock_payten.connect((TCP_IP, TCP_PORT))




dobar_format = bytearray.fromhex(message_data).decode()
print("02023030303030303030303030313030301C311C1C2B301C3934311C1C1C1C1C1C1C1C1C1C1C30301C1C1C1C1C1C1C1C1C0324")
print(message_data)
print(type(message_data))


i = 1

try:
    for i in range(1):
        sent = sock_payten.sendto(bytes(dobar_format, encoding='iso-8859-2'),(TCP_IP,TCP_PORT))
        data = sock_payten.recv(1024)
        print(data)

except:
    print("Ode na except")

finally:
    print('closing socket')


# 0202303030303030303030 30 30313030301C311C1C2B301C3934311C1C1C1C1C1C1C1C1C1C1C30301C1C1C1C1C1C1C1C1C0324
# 02 02 30 30 30 30 30 30 30 30 30 31 30313030301C311C1C2B301C3934311C1C1C1C1C1C1C1C1C1C1C30301C1C1C1C1C1C1C1C1C0324