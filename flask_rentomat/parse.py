import json

msg = b'\x02100000000004010000330006031123162832\x1c000000000002\x1c\x1c+0\x1c941\x1cM\x1c5351529999999999999\x1c99\x1c\x1c\x1c4UUD6 \x1cUPTTEST19\x1c11111111\x1cMASTERCARD\x1c\x1c\x1c\x1c\x1c\x1c\x1cODOBRENO                 \x1c\x1c\x1c\x1c1\x1c\x1c0\x1c\x1c00\x1cD5\x1c\x1c\x1c\x1c\x1c\x1c0\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c000000000000\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c01\x1c\x1c\x1c\x1c\x1c\x03\x0b'
str = b'\x02100000000001020000100006021123145307\x1c000000000002\x1c\x1c+0\x1c941\x1cC\x1c5351529999999999999\x1c99\x1c\x1c\x1c438947\x1cUPTTEST19\x1c11111111\x1cMASTERCARD\x1c\x1c\x1c\x1c\x1c\x1c\x1cODOBRENO                 \x1c\x1c\x1c8407A0000000041010950500000080019F12104465626974204D6173746572636172649F26088CECA3C1E0E40C529F2701809F34031F0302\x1c1\x1c\x1c0\x1c\x1c00\x1cC1\x1c\x1c\x1c\x1c\x1c444411574444\x1c0\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c000000000000\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c01\x1c\x1c\x1c\x1c\x1c\x03\x10'

hex_format = str.hex()

print(hex_format[2:6])

# print(str.decode()[0:3])







# def return_identifier(msg):
# print(msg)
left_text = msg.split(b'\x1c')

# print(left_text)
dict_example = {}

for k in range(0,63,1):
    
    left_text = msg.split(b'\x1c')[k]
    string = left_text.decode()
    # print(string)

    if k == 0:
        #print(string)
        dict_example['identifier'] = string[1:3]
        dict_example['terminalID'] = string[3:5]
        dict_example['sourceID'] = string[5:7]
        dict_example['sequentialNumber'] = string[7:11]
        dict_example['transactionType'] = string[11:13]
        dict_example['transactionFlag'] = string[13:15]
        dict_example['transactionNumber'] = string[15:21]
        dict_example['batchNumber'] = string[21:25]
        dict_example['transactionDate'] = string[25:31]
        dict_example['transactionTime'] = string[31:37]
    if k == 1:
        # print(string)
        dict_example['transactionAmount1'] = string
    if k == 3:
        # print(string)
        dict_example['amountExponent'] = string
    if k == 4:
        # print(string)
        dict_example['amountCurrency'] = string
    if k == 5:
        # print(string)
        dict_example['cardDataSource'] = string
    if k == 6:
        # print(string)
        dict_example['cardNumber'] = string
    if k == 7:
        # print(string)
        dict_example['expirationDate'] = string
    if k == 10:
        # print(string)
        dict_example['authorizationCode'] = string
    if k == 11:
        # print(string)
        dict_example['tidNumber'] = string
    if k == 12:
        # print(string)
        dict_example['midNumber'] = string
    if k == 13:
        # print(string)
        dict_example['companyName'] = string
    if k == 20:
        # print(string)
        dict_example['displayMessage'] = string
    if k == 22:
        # print(string)
        dict_example['inputData'] = string
    if k == 23:
        # print(string)
        dict_example['emvData'] = string
    if k == 24:
        # print(string)
        dict_example['signatureLinePrintFlag'] = string
    if k == 25:
        # print(string)
        dict_example['acquirerName'] = string[0:10]
        dict_example['debitTransactionCount'] = string[10:14]
        dict_example['debitTransactionAmount'] = string[14:26]
        dict_example['refundTransactionCount'] = string[26:30]
        dict_example['refundTransactionAmount'] = string[31:42]
    if k == 26:
        # print(string)
        dict_example['moreMessagesFlag'] = string
    if k == 27:
        # print(string)
        dict_example['installmentsNumber'] = string 
    if k == 28:
        # print(string)
        dict_example['fullResponseCode'] = string
    if k == 29:
        # print(string)
        dict_example['transactionStatus'] = string
    if k == 30:
        # print(string)
        dict_example['spdhTerminalTotals'] = string
    if k == 31:
        # print(string)
        dict_example['spdhHostTotals'] = string
    if k == 32:
        # print(string)
        dict_example['pinBlock'] = string
    if k == 33:
        # print(string)
        dict_example['cardholderName'] = string
    if k == 34:
        # print(string)
        dict_example['rrn'] = string
    if k == 35:
        # print(string)
        dict_example['pinFlag'] = string
    if k == 36:
        # print(string)
        dict_example['transactionAmount2'] = string
    if k == 37:
        # print(string)
        dict_example['payservicesData'] = string
    if k == 38:
        # print(string)
        dict_example['availableBalance'] = string
    if k == 39:
        # print(string)
        dict_example['offlineCryptogram'] = string
    if k == 40:
        # print(string)
        dict_example['loyaltyData'] = string
    if k == 41:
        # print(string)
        dict_example['formattedTextToPrint'] = string
    if k == 42:
        # print(string)
        dict_example['dccNumber'] = string
    if k == 43:
        # print(string)
        dict_example['dccProvider'] = string
    if k == 44:
        # print(string)
        dict_example['dccExchangeRate'] = string
    if k == 45:
        # print(string)
        dict_example['dccExchangeRateDate'] = string
    if k == 46:
        # print(string)
        dict_example['dccMarkUpPercent'] = string
    if k == 47:
        # print(string)
        dict_example['dccAmount'] = string
    if k == 48:
        # print(string)
        dict_example['dccDisclaimer'] = string
    if k == 49:
        # print(string)
        dict_example['dccStatus'] = string
    if k == 50:
        # print(string)
        dict_example['dccCurrencySymbol'] = string
    if k == 51:
        # print(string)
        dict_example['instantPaymentReference'] = string
    if k == 52:
        # print(string)
        dict_example['personal_vehicleCardData'] = string
    if k == 53:
        # print(string)
        dict_example['mifareCardType'] = string
    if k == 54:
        # print(string)
        dict_example['mifareCardUID'] = string
    if k == 55:
        # print(string)
        dict_example['f4gCode'] = string
    if k == 56:
        # print(string)
        dict_example['radcom_transportationSpecificData'] = string
    if k == 57:
        # print(string)
        dict_example['acquirerId'] = string
    if k == 58:
        # print(string)
        dict_example['transactionID'] = string
    



pretty = json.dumps(dict_example)   
print(pretty)


# pos = 1

# print(msg[pos+0:pos+2])
# pos = pos + 2
# print(msg[pos+0:pos+2])
# pos = pos + 2
# print(msg[pos+0:pos+2])
# pos = pos + 2
# print(msg[pos+0:pos+4])
# pos = pos + 4
# print(msg[pos+0:pos+2])
# pos = pos + 2
# print(msg[pos+0:pos+2])
# pos = pos + 2
# print(msg[pos+0:pos+6])
# pos = pos + 6
# print(msg[pos+0:pos+4])
# pos = pos + 4
# print(msg[pos+0:pos+6])
# pos = pos + 6
# print(msg[pos+0:pos+6])
# pos = pos + 6
# print(msg[pos+0:pos+20])

