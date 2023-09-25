from flask import Flask, request, url_for
import time
import serial
from flask import Blueprint, render_template, redirect
from bs4 import BeautifulSoup
import requests
import bs4 as bs
import json
import pprint


import urllib.request
from urllib.parse import urljoin




app = Flask(__name__)

         
      




@app.route('/')
def root():
   # read_rentomat("root", "0")
   return render_template('index.html')


# redirect to reservation website
@app.route('/rezervacije')
def rezervacije():
   return redirect("https://cheapcarhire.rent/")





# @app.route('/odoo')
# def odoo():
#    return render_template('odoo.html', iframe='https://www.google.com/')





# @app.route('/html')
# def html():
#     return render_template('html.html')





@app.route('/listaVozila')
def listaVozila():
   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
      data = json.load(jsonFile)


   available_cars=[]



  
       





   for key in data['key_positions']:
      if (data['key_positions'][key]['rfid'] != ""):
         rfid = data['key_positions'][key]['rfid']
         


         response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

         response_data = json.loads(response.text)
         access_token = response_data['access_token']


         

         url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('x_key_rfid', '=', '"+rfid+"'), ('state', '!=', 'open'), ('state', '!=', 'running')]"

         header_data = {'Access-Token' : str(access_token)}

         response = requests.get(url, headers=header_data)

         response_data = json.loads(response.text)
         print(response.text)
         # if(response_data['count'] != 0):
         #     available_cars.append(rfid)

         #     url = "http://23.88.98.237:8069/api/fleet.vehicle?filters=[('x_key_rfid', '=', '"+rfid+"')]"

         #     header_data = {'Access-Token' : str(access_token)}

         #     response = requests.get(url, headers=header_data)

         #     response_data = json.loads(response.text)
             
         # if(response_data['count'] != 0):
         #    vehicle_id = str(response_data['results'][0]['vehicle_id']['id'])

         #    url = "http://23.88.98.237:8069/api/fleet.vehicle/"+vehicle_id

         #    header_data = {'Access-Token' : str(access_token)}

         #    response = requests.get(url, headers=header_data)

         #    response_data = json.loads(response.text)

         #    print(response_data)
         #    print("Vehicle name: "+response_data['name'])
         #    print("Vehicle plate"+response_data['license_plate'])

         if(response_data['count'] != 0):
            vehicle_id = str(response_data['results'][0]['vehicle_id']['id'])
            #print(vehicle_id)
            vehicle_name = str(response_data['results'][0]['vehicle_id']['name'])
            vehicle_plate = str(response_data['results'][0]['vehicle_id']['license_plate'])

            transmission = str(response_data['results'][0]['vehicle_id']['transmission'])
            fuel_type = str(response_data['results'][0]['vehicle_id']['fuel_type'])
            seats = str(response_data['results'][0]['vehicle_id']['seats'])
            doors = str(response_data['results'][0]['vehicle_id']['doors'])
            # vehicle_plate = str(response_data['results'][0]['vehicle_id']['license_plate'])
            image = str(response_data['results'][0]['vehicle_id']['image_128'])


            toAdd = {
               'id' : vehicle_id,
               'name' : vehicle_name,
               'plate' : vehicle_plate,
               'transmission' : transmission,
               'fuel_type' : fuel_type,
               'seats' : seats,
               'doors' : doors,
               'image' : image
            }

            available_cars.append(toAdd)
            # print(available_cars)

 
   return render_template('rezervacija/listaVozila.html', cars = available_cars)



@app.route('/vozilo',  methods=['GET', 'POST'])
def vozilo():

   vehicle_id = request.args.get('id')



   response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

   response_data = json.loads(response.text)
   access_token = response_data['access_token']

   
   url = "http://23.88.98.237:8069/api/fleet.vehicle/"+vehicle_id

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)

   print(response.text)


   brand = response_data['brand_id']['name']
   model = response_data['model_id']['name']
   gearbox = response_data['transmission']
   fuel_type = response_data['fuel_type']
   category = response_data['category_id']['name']
   license_plate = response_data['license_plate']
   seats = response_data['seats']
   model_year = response_data['model_year']
   doors = response_data['doors']
   horsepower = response_data['horsepower']
   power = response_data['power']
   image_128 = response_data['image_128']

   
   


   print("Brand: "+brand)
   print("model: "+model)
   print("gearbox: "+gearbox)
   print("fuel_type: "+fuel_type)
   print("category: "+category)
   print("license_plate: "+license_plate)
   print("seats: "+str(seats))
   print("model_year: "+str(model_year))
   print("doors: "+str(doors))
   print("horsepower: "+str(horsepower))
   print("power: "+str(power))

   # vehicle_data = {
   #             'name' : vehicle_name,
   #             'plate' : vehicle_plate,
   #          }




   return render_template('/rezervacija/vozilo.html', brand=brand, model=model, gearbox=gearbox, fuel_type=fuel_type, category=category, license_plate=license_plate, seats=seats, model_year=model_year, doors=doors, horsepower=horsepower, power=power, image_128=image_128)


@app.route('/rezervacijeKorisnik')
def rezervacijeKorisnik():
   return render_template('/rezervacija/rezervacijeKorisnik.html')







# VRACANJE

@app.route('/vracanjeHome', methods = ['GET', 'POST'])
def vracanjeHome():
    if request.method == 'POST':
        rfid = request.form.get('rfid')
        return redirect(url_for('vracanjeStatus', rfid_input=rfid))
    return render_template('/vracanje/vracanjeHome.html')

@app.route('/vracanjeStatus',  methods=['GET', 'POST'])
def vracanjeStatus():


   rfid_input = request.args.get('rfid_input')
   # return(rfid_input)
   return render_template('/vracanje/vracanjeStatus.html', rfid_input = rfid_input)






@app.route('/vracanjeOcena',  methods=['GET', 'POST'])
def vracanjeOcena():

   status = request.args.get('status')
   rfid_input = request.args.get('rfid')

   return render_template('/vracanje/vracanjeOcena.html', rfid_input = rfid_input, status = status)






@app.route('/vracanjePrimedbe',  methods=['GET', 'POST'])
def vracanjePrimedbe():



   if request.method == 'POST':
        rating = request.form.get('rating')
        rfid_input = request.form.get('rfid_input')
        status = request.form.get('status')
        comment = request.form.get('comment')
        return redirect(url_for('vracanjeOtvori', rating=rating, rfid_input=rfid_input, status=status, comment=comment))


   status = request.args.get('status')
   rfid_input = request.args.get('rfid')
   rating = request.args.get('rating')

   return render_template('/vracanje/vracanjePrimedbe.html', rfid_input = rfid_input, status = status, rating=rating)






@app.route('/vracanjeOtvori',  methods=['GET', 'POST'])
def vracanjeOtvori():


 
   rating = request.args.get('rating')
   rfid_input = request.args.get('rfid_input')
   status = request.args.get('status')
   comment = request.args.get('comment')
   

   

   # PROVERA DA LI IMA SLOBODNE POZICIJE U RENTOMATU

   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
      data = json.load(jsonFile)

   first_empty_key_position = ''

   for key in data['key_positions']:
      if (data['key_positions'][key]['rfid'] == ""):
         first_empty_key_position = key
         break

   rentomat_id = data['rentomat_id']




   if(first_empty_key_position != ''):


      # POKRETANJE RENTOMATA


      with open('/home/pi/VSCProjects/selfrentacar/flask_rentomat/komanda.txt', 'w') as f:
               f.write("FILL,"+str(first_empty_key_position))


      # UPDATE JSON

      with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
         data = json.load(jsonFile)

      data["key_positions"][first_empty_key_position]["rfid"] = rfid_input

      with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "w") as jsonFile:
         json.dump(data, jsonFile)

      # UPDATE ODOO RFID
      
      update_odoo_rfid(rentomat_id)



      # UPDATE STATUSA UGOVORA
      # mora preko API-ja da se dobije BROJ UGOVORA (STATUS, pozcija kljuca za vozilo)


      response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

      response_data = json.loads(response.text)
      access_token = response_data['access_token']
      #return(access_token)

      rfid_num = str(rfid_input)
      

      url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('x_key_rfid', '=', '"+rfid_num+"'), ('state', '=', 'running')]"

      header_data = {'Access-Token' : str(access_token)}

      response = requests.get(url, headers=header_data)

      response_data = json.loads(response.text)


      
      contract_id = str(response_data['results'][0]['id'])





      header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

      url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id
     
     
      data_update = json.dumps({'state': 'done',})
      response = requests.put(url, data=data_update, headers=header_data)






      # SLANJE PODATAKA O UTISCIMA




      return render_template('/vracanje/vracanjeOtvori.html', rating=rating, rfid_input=rfid_input, status=status, comment=comment)
    
   else:
       return render_template('/errors/no_empty_position.html')





      
      

    
 
 
@app.route('/vracanjeHvala')
def vracanjeHvala():




   return render_template('/vracanje/vracanjeHvala.html')


   


def get_prazna_pozicija():
    # logika za pronalazenje prve prazne pozicije
    return 2


# API CALL





def update_odoo_rfid(rentomatId):
   response = requests.get(
         "http://23.88.98.237:8069/api/auth/get_tokens",
         params={"username": "odoo@irvas.rs", "password": "irvasadm"}
      )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']

   
   url = "http://23.88.98.237:8069/api/rentomat.configurator?filters=[('rentomat_id','=','"+rentomatId+"')]"
   
   
 

   header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   return_data = json.loads(response.content)

   id_rent = str(return_data['results'][0]['id'])



   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
         data = json.load(jsonFile)


   data_insert={
       "position_1" : "",
       "position_2" : "",
       "position_3" : "",
       "position_4" : "",
       "position_5" : "",
       "position_6" : "",
       "position_7" : "",
       "position_8" : "",
       "position_9" : "",
       "position_10" : "",
       "position_11" : "",
       "position_12" : ""
   }



   url = "http://23.88.98.237:8069/api/rentomat.configurator/"+id_rent
   
   for key in data['key_positions']:
       data_insert['position_'+key] = data['key_positions'][key]['rfid']

   data_insert_final = json.dumps(data_insert)

   response = requests.put(url, data=data_insert_final, headers=header_data)









def get_rfid_num(id_ugovora):
   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']
   #return(access_token)

   

   url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('id','=','"+id_ugovora+"')]"

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)

   x_key_rfid = response_data['results'][0]['vehicle_id']['x_key_rfid']

   return x_key_rfid



@app.route('/api', methods = ['GET', 'POST', 'PUT'])
def api():


   # response = requests.get(
   #          "http://23.88.98.237:8069/api/auth/get_tokens",
   #          params={"username": "odoo@irvas.rs", "password": "irvasadm"}
   #    )

   # response_data = json.loads(response.text)
   # access_token = response_data['access_token']
   # #return(access_token)

   # rfid_num = str(47)
   

   # url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('x_key_rfid', '=', 'R47'),('state', '=', 'running')]"

   # header_data = {'Access-Token' : str(access_token)}

   # response = requests.get(url, headers=header_data)

   # response_data = json.loads(response.text)


   
   # contract_id = response_data['results'][0]['id']
   # print(contract_id)


   # return render_template('/vracanje/vracanjeHvala.html')






















   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']
   #return(access_token)
   header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}
   

   # url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('id','=','47'), ('state','=','open')]"
   # data_update = json.dumps({'state': 'running',})
   

   
   # ADD USER

   url = "http://23.88.98.237:8069/api/res.users"


 

   data_insert={
       "name" : "Milos",
       "email" : "milos@rentomat.com",
       "login" : "milos@rentomat.com",
       "phone" : "0603525456",
       "is_company" : "0",
       "street" : "Cara Dusana 12",
       "city" : "Nis",
       "country_id" : "1",
       "is_tenant" : True
   }

   data_insert_final = json.dumps(data_insert)
   # print(url)
   # print(data_insert_final)
   # print(header_data)

   response = requests.post(url, data=data_insert_final, headers=header_data)

   print(response)

   return render_template('/vracanje/vracanjeHvala.html')

   response = requests.get(url, headers=header_data)
   #print(response.content)

   return_data = json.loads(response.content)

   id_rent = str(return_data['results'][0]['id'])



   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
         data = json.load(jsonFile)

   # print(data['key_positions'])


   data_insert={
       "position_1" : "",
       "position_2" : "",
       "position_3" : "",
       "position_4" : "",
       "position_5" : "",
       "position_6" : "",
       "position_7" : "",
       "position_8" : "",
       "position_9" : "",
       "position_10" : "",
       "position_11" : "",
       "position_12" : ""
   }



   url = "http://23.88.98.237:8069/api/rentomat.configurator/"+id_rent

   for key in data['key_positions']:
       data_insert['position_'+key] = data['key_positions'][key]['rfid']

   data_insert_final = json.dumps(data_insert)

   response = requests.put(url, data=data_insert_final, headers=header_data)
   





   # url = "http://23.88.98.237:8069/api/rentomat.configurator/"+id_rent

   # response = requests.get(url, headers=header_data)
   # print(response.content)

   # url = "http://23.88.98.237:8069/api/rentomat.configurator?filters=[('rentomat_id','=','RN01834')]"


   # response_data = json.loads(response.text)
   # print(print(json.dumps(response_data, indent=4)))
   # return json.dumps(response_data, indent=4)
   #key_position = response_data['results'][0]['vehicle_id']['license_plate']

   
   

   # find key position

   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
      data = json.load(jsonFile)

   key_rfid = 'R1237'

   key_position = 0

   for key in data['key_positions']:
    if (data['key_positions'][key]['rfid'] == key_rfid):
        print("Pozicija kljuca iz RFID")
        print(key) 
        print("***********************")
        key_position = key

 






   #find first empty place

   first_empty_key_position = 0

   for key in data['key_positions']:
    if (data['key_positions'][key]['rfid'] == ""):
        print("Prva slobodna pozicija: ")
        print(key) 
        print("***********************")
        first_empty_key_position = key
        break


   
   #update JSON table with inserted key



   inserted_key_rfid = 'R333111'

   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
      data = json.load(jsonFile)

   data["key_positions"][first_empty_key_position]["rfid"] = inserted_key_rfid

   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "w") as jsonFile:
      json.dump(data, jsonFile)








   return '1'

   







# PREUZIMANJE

@app.route('/preuzimanjeHome', methods = ['GET', 'POST'])
def preuzimanjeHome():

   if request.method == 'POST':
        ugovor_link = request.form.get('ugovor_link')
        return redirect(url_for('preuzimanjeUgovor', ugovor_link=ugovor_link))



   return render_template('/preuzimanje/preuzimanjeHome.html')



@app.route('/preuzimanjeUgovor/', methods = ['GET', 'POST'])
def preuzimanjeUgovor():
   ugovor_link = request.args.get('ugovor_link')




   first_part = ugovor_link.split('?')[0]

   Segments = first_part.rpartition('/')
   contract_id = Segments[2]
   
  


   position = 3
   link_ugovora = ugovor_link
   #link_ugovora = 'https://selfcar.naisrobotics.com/my/carrental_contract/47?access_token=0a23e16e-10da-47f5-9008-c239e8ae7cb6'
   #link_ugovora = 'https://selfcar.naisrobotics.com/my/invoices/18?access_token=c4d293f1-7d45-433a-b6e0-ad17f779dc23'
   
   return render_template('odoo.html', contract_id = contract_id, position = position, iframe= link_ugovora)
   
   



@app.route('/preuzimanjeUgovorStampa')
def preuzimanjeUgovorStampa():
   return render_template('preuzimanjeUgovorStampa.html')



@app.route('/preuzimanjeKljuc', methods = ['GET', 'POST', 'PUT'])
def preuzimanjeKljuc():



   # PREUZIMANJE RFID BROJA IZ UGOVORA


   contract_id = request.args.get('contract_id')
   
   print("Broj ugovora")
   print(contract_id)


   try:
      rfid_num = get_rfid(contract_id)
   except:
       return render_template('/errors/non_exist_rfid_in_database.html')


   print("RFID num")
   print(rfid_num)
   key_rfid = rfid_num
   # get_rfid(contract_id)


   try:

      with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
         data = json.load(jsonFile)

      

      key_position = ''
      # print("pocinje FOR petlja")
      for key in data['key_positions']:
         if (data['key_positions'][key]['rfid'] == key_rfid):
         
            key_position = key
      rentomat_id = data['rentomat_id']
      print("**************************")
      print(rentomat_id)
      print("**************************")
         

      # print(key_position) 
      # Snimanje u komanda.txt fajlu
      
      if(key_position != ''):

         with open('/home/pi/VSCProjects/selfrentacar/flask_rentomat/komanda.txt', 'w') as f:
            f.write("EMPTY,"+str(key_position))

      # update settings.json fajla
      
         with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
            data = json.load(jsonFile)

         data["key_positions"][key_position]["rfid"] = ""

         with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "w") as jsonFile:
            json.dump(data, jsonFile) 
         
         
         update_odoo_rfid(rentomat_id)

      # update contract to RUNNING

         response = requests.get(
                  "http://23.88.98.237:8069/api/auth/get_tokens",
                  params={"username": "odoo@irvas.rs", "password": "irvasadm"}
            )

         response_data = json.loads(response.text)
         access_token = response_data['access_token']


   

   
         
         
      

         header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

     








         url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id
         print("Ugovor id je: "+contract_id)
         print("Acces token je: "+access_token)
         print("Url je"+url)
         data_update = json.dumps({'state': 'running',})
         response = requests.put(url, data=data_update, headers=header_data)


         return render_template('/preuzimanje/preuzimanjeKljuc.html')
      else:
         
         return render_template('/errors/non_exist_rfid.html')
   except:
       return render_template('/errors/general_except.html')




def update_contract_running(contract_id):
   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']


   header_data = {'Access-Token' : str(access_token)}

   url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id
   print("Ugovor id je: "+contract_id)
   print("Acces token je: "+access_token)
   print("Url je"+url)
   data_update = {'state': 'running'}
   requests.put(url, data=data_update, headers=header_data)





def get_rfid(contract_id):
   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']
   #return(access_token)

   

   url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('id','=','"+contract_id+"')]"

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)

   key_position = response_data['results'][0]['vehicle_id']['x_key_rfid']

   return key_position










# OPERACIJE SA AUTOMATOM


@app.route('/HOME')
def home():
   with open('/home/pi/VSCProjects/selfrentacar/flask_rentomat/komanda.txt', 'w') as f:
            f.write("HOME")      
   return "u"
    # read_rentomat('HOME', '0')

#     ser = serial.Serial('/dev/myUSB', 115200, timeout=25)
#     data_in = ser.readline().decode("ascii")
# #    while ser.in_waiting:
#     while data_in[0:10] == start_r[0:10]:
        
#         print(data_in)
#         if data_in[0:10] == start_r[0:10]:
#             ser.write(komanda.encode())
#             print(ser.exclusive)
#             # red = ser.readline().decode("ascii")
#             time.sleep(20)
#             # print(red)
#             # if ser.is_open:
#             # ser.close()
#             return 'Izdata naredba HOME'
#         else:
#             print(data_in)
# #            ser.write('\n')
#     # if ser.is_open:
#      #   ser.close()

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
   read_rentomat('EMPTY', pozicija_kljuca)
   with open('/home/pi/VSCProjects/selfrentacar/flask_rentomat/komanda.txt', 'w') as f:
            f.write("EMPTY")      
   return "u"

if __name__ == '__main__':
   app.run()
   # read_rentomat("")
   #  ser = serial.Serial('/dev/myUSB', 115200, timeout=20)
   #  data_in = ser.readline().decode("ascii")
   #  while data_in[0:4] == ready[0:4]:
        
   #      if data_in[0:4] == ready[0:4]:
   #          ser.write(prazni.encode())
   #          time.sleep(1)

   #          ser.write(pozicija_kljuca.encode())

   #          time.sleep(20)
   #          ser.close()
   #          return pozicija_kljuca
   #  return "Odradjena komanda EMPTY"



    
@app.route('/FILL')
def fill():

    rfid = request.args.get('pos')
    

