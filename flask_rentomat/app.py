from flask import Flask, request
import time
import serial
from flask import Blueprint, render_template, redirect
from bs4 import BeautifulSoup
import requests
import bs4 as bs



import urllib.request
from urllib.parse import urljoin




app = Flask(__name__)

# ser = serial.Serial('/dev/myUSB', 115200, timeout=20)

print("Starting program")

# ser = serial.Serial("/dev/ttyUSB", baudrate=9600,
#parity=serial.PARITY_NONE,
#stopbits=serial.STOPBITS_ONE,
#bytesize=serial.EIGHTBITS
time.sleep(1)

komanda = 'HOME'
prazni = 'EMPTY'
pozicija = '5'
emptied = 'EMPTIED'
ready = 'READY'
i=1
# print(komanda.encode())
start_r ='HOME REQ...'

# ser.write(komanda.encode())
# time.sleep(20)
#            ser.write('\n')

@app.route('/')
def root():
   return render_template('index.html')
if __name__ == '__main__':
   app.run()

# redirect to reservation website
@app.route('/rezervacije')
def rezervacije():
   return redirect("https://cheapcarhire.rent/")
if __name__ == '__main__':
   app.run()




@app.route('/odoo')
def odoo():
   return render_template('odoo.html', iframe='https://www.google.com/')
if __name__ == '__main__':
   app.run()




@app.route('/html')
def html():
    return render_template('html.html')










# VRACANJE
@app.route('/vracanjeHome')
def vracanjeHome():
   return render_template('/vracanje/vracanjeHome.html')
if __name__ == '__main__':
   app.run()

@app.route('/vracanjeStatus',  methods=['GET', 'POST'])
def vracanjeStatus():
   return render_template('/vracanje/vracanjeStatus.html')
if __name__ == '__main__':
   app.run()






# API CALL

@app.route('/api')
def api():
   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   return (response.text)

   # "http://23.88.98.237:8069/api/fleet.rent?filters=[('reservation_code','=','$resrvation_number')]"
   
if __name__ == '__main__':
   app.run()






# PREUZIMANJE

@app.route('/preuzimanjeHome')
def preuzimanjeHome():
   return render_template('/preuzimanje/preuzimanjeHome.html')
if __name__ == '__main__':
   app.run()


@app.route('/preuzimanjeUgovor/', methods = ['POST', 'GET'])
def preuzimanjeUgovor():

   # iza URL ugovora treba da se izvucu svi potrebni podaci
   # contract_id = parse(URL)
   # contract_data = get_contract_data(contract_id)

     
   
   # position = contract_data->rfid_position
   # update tabel for key location
   # EMPTY


   position = 9;

   return render_template('odoo.html', position = position, iframe='https://selfcar.naisrobotics.com/my/invoices/18?access_token=c4d293f1-7d45-433a-b6e0-ad17f779dc23')
   
   


   
if __name__ == '__main__':
   app.run()


@app.route('/preuzimanjeUgovorStampa')
def preuzimanjeUgovorStampa():
   return render_template('preuzimanjeUgovorStampa.html')
if __name__ == '__main__':
   app.run()


@app.route('/preuzimanjeKljuc')
def preuzimanjeKljuc():



   # 
   pozicija_kljuca = request.args.get('pos')
    
   ser = serial.Serial('/dev/myUSB', 115200, timeout=20)
   data_in = ser.readline().decode("ascii")
   while data_in[0:4] == ready[0:4]:
        
      if data_in[0:4] == ready[0:4]:
         # ser.write(prazni.encode())
         time.sleep(1)

         ser.write(pozicija_kljuca.encode())

         # time.sleep(20)
         ser.close()

   return render_template('/preuzimanje/preuzimanjeKljuc.html')

if __name__ == '__main__':
   app.run()

















# OPERACIJE SA AUTOMATOM


@app.route('/HOME')
def home():
    
    ser = serial.Serial('/dev/myUSB', 115200, timeout=20)
    data_in = ser.readline().decode("ascii")
#    while ser.in_waiting:
    while data_in[0:10] == start_r[0:10]:
        
        print(data_in)
        if data_in[0:10] == start_r[0:10]:
            ser.write(komanda.encode())
            time.sleep(20)
            # if ser.is_open:
            #    ser.close()
            return 'Izdata naredba HOME'
        else:
            print(data_in)
#            ser.write('\n')
    # if ser.is_open:
     #   ser.close()
    return "Odrdjen home"
    # while ser.in_waiting:
    #     data_in = ser.readline().decode("ascii")


    # if data_in[0:6] == emptied[0:6]:
    #     print("*******   Vratio sa na pocetnu poziciju")
    # ser.flush()
    # data_in = ser.readline().decode("ascii")
    # print(data_in)
    
    # else:
    #     return 'nismo dobili odgovor da je homirat automat'

@app.route('/EMPTY', methods=['GET'])
def empty():
    pozicija_kljuca = request.args.get('pos')
    
    ser = serial.Serial('/dev/myUSB', 115200, timeout=20)
    data_in = ser.readline().decode("ascii")
    while data_in[0:4] == ready[0:4]:
        
        if data_in[0:4] == ready[0:4]:
            ser.write(prazni.encode())
            time.sleep(1)

            ser.write(pozicija_kljuca.encode())

            time.sleep(20)
            ser.close()
            return pozicija_kljuca
    return "Odradjena komanda EMPTY"



    
@app.route('/FILL')
def fill():

    rfid = request.args.get('pos')
    

