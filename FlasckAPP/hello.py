# Fukcija ove aplikacije je da prima zahteve od flutter aplikacije za prijem i izdavanje kljuceva iz rentomata

from flask import Flask, request
import time
import serial
app = Flask(__name__)

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)    

print("Starting program")

# ser = serial.Serial("/dev/ttyUSB", baudrate=9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS
time.sleep(1)

homiranje = 'HOME'  # posle ukljucenja rentomata, ovom naredbom se tocak sa korpicama dovodi u pocetni polozaj.
prazni = 'EMPTY'    # Ovom naredbom se izdaje kljuc iz rentomata
pozicija = '5'      # pozivija je redni broj korpice u kojoj se nalazi kljuc
emptied = 'EMPTIED' # ovo je string koje salje rentomat posle vracanja kljuca
i=1
print(komanda.encode())
start_r ='HOME REQ...'

# ser.write(komanda.encode())
# time.sleep(20)
#            ser.write('\n')

@app.route('/')
def hello_world():
    return 'RENTOMAT V.0.1 - sistem za izdavanje kljuceva'

@app.route('/HOME')   # stigao je zahtev da se izvrsi homiranje
def home():
    ser.write(komanda.encode())
    time.sleep(20)
#            ser.write('\n')

    return 'RENTOMAT V.0.1 - Izdata naredba za početno pozicioniranje točka'

@app.route('/EMPTY', methods=['GET'])   # stigao je zahtev za izdavanje ključa iz rentomata
def empty():
    pozicija_kljuca = request.args.get('pos')
    print(pozicija_kljuca)
   



    # ser.write(prazni.encode())
    # time.sleep(1)
    # ser.write(pozicija.encode())
    # i = 2
    # time.sleep(1)
    # data_in = ser.readline().decode("ascii")
    # for character in data_in:
    #     print(character, character.encode('utf-8').hex())

    # if data_in[0:6] == emptied[0:6]:
    #     print("*******   Vratio sa na pocetnu poziciju")
    #     exit
    return_msg = 'RENTOMAT V.0.1 - izdat ključ' + str(pozicija_kljuca)
    return return_msg

@app.route('/FILL')
def fill():
    return 'Peco hoces da uradis Vacanje kljuca'

