import binascii


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


STX = "02"
ETX = "03"
EOT = "04"
ACK = "06"
NACK = "15"





# message_data = '3030303030303030303030313030301C311C1C2B301C3934311C1C1C1C1C1C1C1C1C1C1C30301C1C1C1C1C1C1C1C1C03'
# # message_data = "484848484848484848484849484848284928284348285752492828282828282828282828484828282828282828282803"
# message_data1 = binascii.hexlify(message_data)

# print(message_data1)

# input_data = message_data.decode('utf-8')

# dobar_format = bytearray.fromhex("3030303030303030303030313030301C311C1C2B301C3934311C1C1C1C1C1C1C1C1C1C1C30301C1C1C1C1C1C1C1C1C03").decode()
# print("...................")
# test = bytes(dobar_format, encoding='iso-8859-2')
# # print(input_data)




# string_to_input = test.decode('hex')
# print(string_to_input)


# ba = bytearray(string_to_input)

message = "3030303030303030303030313030301C311C1C2B301C3934311C1C1C1C1C1C1C1C1C1C1C30301C1C1C1C1C1C1C1C1C03"
message = "3030303030303030303130313030301C311C1C2B301C3934311C1C1C1C1C1C1C1C1C1C1C30301C1C1C1C1C1C1C1C1C03"
msg = '100000000001020000070006021123123540280000000000022828+02894128C285258389999999999999289928282845182628UPTTEST19281111111128MASTERCARD28282828282828ODOBRENO                 2828288407A0000000041010950500000080019F120A4D6173746572636172649F2608DEB8E5D2535327169F2701809F34031F03022812828028280028C1282828282844441106444428028282828282828282828282800000000000028282828282828282828012828282828x03'
lrc = 0
msg = b'100000000001020000070006021123123540\x1c000000000002\x1c\x1c+0\x1c941\x1cC\x1c5258389999999999999\x1c99\x1c\x1c\x1c451826\x1cUPTTEST19\x1c11111111\x1cMASTERCARD\x1c\x1c\x1c\x1c\x1c\x1c\x1cODOBRENO                 \x1c\x1c\x1c8407A0000000041010950500000080019F120A4D6173746572636172649F2608DEB8E5D2535327169F2701809F34031F0302\x1c1\x1c\x1c0\x1c\x1c00\x1cC1\x1c\x1c\x1c\x1c\x1c444411064444\x1c0\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c000000000000\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c01\x1c\x1c\x1c\x1c\x1c\x03'

msg1 = msg.hex()

j = 0
print(msg1)
for i in range(0, len(msg1)-1, 2):
    b = msg1[i:i+2]

    print(int(b, 16))
    if int(b, 16) == 28: 
        j = j+1
    lrc ^= int(b, 16)

print(j)

print(lrc)
hex_value = hex(lrc)
# print(str(hex_value))
# print(type(hex_value))


# def xor_sum(input_data):
 
#     lrc = int(input_data[0]);

#     for i in range(1, len(input_data)-1, 1):

#         lrc ^= int(input_data[i]);



#     return lrc



# print(xor_sum(ba))



# nack_message_data_tmp = NACK + ETX


# # print(message_data)
# total_sum = xor_sum(message_data)
# print(total_sum)
# moduo = total_sum % 256

# final_value = 256 - moduo

# print(final_value)


#  internal class Program

#     {

#         static void Main(string[] args)

#         {

 

#             byte[] hexPoruka = { 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x31, 0x30,

#                    0x30, 0x30, 0x1C, 0x31, 0x1C, 0x1C, 0x2B, 0x30, 0x1C, 0x39, 0x34, 0x31, 0x1C,

#                    0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x30, 0x30, 0x1C,

#                    0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x03 };

#             string strPoruka = System.Text.Encoding.UTF8.GetString(hexPoruka);

#             char charLrcRezultat = LRC.calculateS(strPoruka);

#             Console.Write("hexPoruka: ");

#             foreach (byte item in hexPoruka)

#             {

#                 Console.Write($"{item.ToString("x2")} ");

#             }

#             Console.WriteLine($"\nstrPoruka: {strPoruka}\n" +

#                 $"Hex odgovor: {Convert.ToByte(charLrcRezultat).ToString("x2")}\n" +

#                 $"Ascii odgovor : {Convert.ToByte(charLrcRezultat).ToString()}\n" +

#                 $"Char odgovor: {charLrcRezultat}");

#             Console.ReadLine();

#         }

#         class LRC

#         {

#             public static char calculateS(string input)

#             {

#                 return calculate(input.ToCharArray());

#             }

 

#             public static char calculate(char[] input)

#             {

#                 char lrc = input[0];

#                 for (int i = 1; i < input.Length; i++)

#                 {

#                     lrc ^= input[i];

#                 }

#                 return lrc;

#             }

#         }

#     }