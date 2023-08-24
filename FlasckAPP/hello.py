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

komanda = 'HOME'
prazni = 'EMPTY'
pozicija = '5'
emptied = 'EMPTIED'
i=1
print(komanda.encode())
start_r ='HOME REQ...'

# ser.write(komanda.encode())
# time.sleep(20)
#            ser.write('\n')

@app.route('/')
def hello_world():
    return 'Hello, Peppe8o users!'

@app.route('/HOME')
def home():
    ser.write(komanda.encode())
    time.sleep(20)
#            ser.write('\n')

    return 'Hello, Peppe8o users!'

@app.route('/EMPTY', methods=['GET'])
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

    return pozicija_kljuca
@app.route('/FILL')
def fill():
    return 'Peco hoces da uradis Vacanje kljuca'

