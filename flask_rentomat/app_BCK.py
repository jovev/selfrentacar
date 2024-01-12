from base64 import b64decode
import binascii
import os
from flask import Flask, request, session, url_for
from flask_babel import Babel
import time
import serial
from flask import Blueprint, render_template, redirect
from bs4 import BeautifulSoup
import requests
import bs4 as bs
import json
import pprint
# from datetime import datetime
from urllib.parse import urlencode
from datetime import datetime, timedelta, date, time
from flask_babel import Babel
import ast
from babel import numbers, dates
from flask_babel import Babel, format_date, gettext
import socket
import RPi.GPIO as GPIO
import pyqrcode
from pyqrcode import QRCode
from reportlab.pdfgen import canvas
from fpdf import FPDF 
import codecs
import urllib.request
from urllib.parse import urljoin
babel = Babel()

import png 
from pyqrcode import QRCode 
import subprocess
import math









def lights():
   # Use physical pin numbers
   GPIO.setmode(GPIO.BOARD)
   # Set up header pin 11 (GPIO17) as an output
   print("Setup Pin 11")
   GPIO.setup(11, GPIO.OUT)
   
   var=1
   print("Start loop")
   while var==1:
      print("Set Output False")
      GPIO.output(11, False)
      time.sleep(1)
      print("Set Output True")
      GPIO.output(11, True)
      time.sleep(1)

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)

app.secret_key = "super secret key"

@app.route('/language=<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(url_for('root'))


app.config['LANGUAGES'] =  {
    'en': 'English',
    'sr': 'Srpski',
    'ru': 'Russian'
}


def get_locale():
    if request.args.get('language'):
        session['language'] = request.args.get('language')
    return session.get('language', 'en')


# def get_locale():
#    return 'sr'

babel.init_app(app, locale_selector=get_locale)




@app.route('/getData')
def getData():

  




  
  
   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

   URL = "https://cheapcarhire.rent/wp-json/my/price/getprice?date_from=11&date_to=51&from=1&to=522"

   r = requests.get(url = URL, headers = headers, data='')


   # print(r)
   # print(r.text)
   print(r.status_code)




   data_insert_final = json.dumps(r.text)
   print(data_insert_final)

   return "1"
@app.route('/lang')
def lang():


   d = date(2017, 5,2)


   irvas = gettext('Irvas')

   us_num = numbers.format_decimal(1.23456, locale= 'en_US')
   sv_num = numbers.format_decimal(1.23456, locale= 'sv_SE')
   sr_num = numbers.format_decimal(1.23456, locale= 'sr_RS')
   ru_num = numbers.format_decimal(1.23456, locale= 'ru_RU')


   de_date = format_date(d)


   results = {'de_date' : de_date, 'us_num' : us_num, 'sv_num' : sv_num, 'sr_num' : sr_num, 'ru_num' : ru_num}

   return render_template('lang.html', results = results, irvas = irvas)




@app.route('/invoice')
def invoice():
      


   JSONBody = {
      "itemId":"1",
      "quantity":1,
      "amount":100,
      "buyerId":"123456789"
   }

   response = requests.get("http://79.101.159.196:8099/esir/westapi/newInvoice",json = JSONBody)


   response_data = json.loads(response.text)

   print(response_data)

   before = response_data["journalBefore"]
   after = response_data["journalAfter"]
   qrcode_url = response_data["qrCodeUrl"]
   invoiceNumber = response_data["invoiceNumber"]


   
   # Generate QR code 
   url = pyqrcode.create(qrcode_url) 
   
  
   
   # Create and save the png file naming "myqr.png" 
   url.png('myqr.png', scale = 1) 


   # print(invoiceNumber)
   # print(before+after)
   # print(qrcode_url)
   # print(after)


   margin_topce = "\n\n\n\n\n\n\n\n\n\n"

   content = margin_topce+before+after

   # bytes = b64decode(content, validate=True)

   f = open("fiskalni.txt", "wb")
   f.write(content.encode('latin-1', 'ignore'))
   f.close()



   pdf = FPDF()      
   # Add a page 
  


   pdf.add_page()  
   # set style and size of font  
   # that you want in the pdf 
   pdf.set_font("Arial", size = 11)
   pdf.set_margins(10, 10, 0)
   # open the text file in read mode 
   f = open("fiskalni.txt", "r") 
   # insert the texts in pdf 
   for x in f: 
      pdf.cell(50,5, txt = x, ln = 1, align = 'C') 
   # save the pdf with name .pdf 

   pdf.image('myqr.png', 1, 1)


   pdf.output("pdf.pdf")


   
   my_canvas = canvas.Canvas("testic.pdf")
   my_canvas.drawString(50, 350, content)
   my_canvas.save()

   os.system("lp pdf.pdf")

   return "1"


@app.route('/rentomat')
def rentomat():
   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
      data = json.load(jsonFile)

   # print(data)


   response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

   response_data = json.loads(response.text)
   access_token = response_data['access_token']


   car_list = []


   for i in range(12):
      key_pos = i+1

      current_rfid = data['key_positions'][str(key_pos)]['rfid']

      url = "http://23.88.98.237:8069/api/fleet.vehicle?filters=[('x_key_rfid', '=', '"+current_rfid+"')]"
      header_data = {'Access-Token' : str(access_token)}

      response = requests.get(url, headers=header_data)

      response_data = json.loads(response.text)
      print(response_data)
      # vehicle_id = str(response_data['results'][0]['id'])
      if(response_data['count'] != 0):
         vehicle_name = str(response_data['results'][0]['name'])
      else:
         vehicle_name = ""
      # print(current_rfid)
      # print(vehicle_name)

      car_list.append(vehicle_name)

   print(car_list)

   rent_data = {
       'rentomat_id' : data['rentomat_id'],
       'last_contract_id' : data['last_contract_id'],
       'location' : data['location'],
       'location_description' : data['location_description'],
       'cleaning_time' : data['cleaning_time'],
       'key_pos_1' : data['key_positions']['1']['rfid'],
       'key_pos_2' : data['key_positions']['2']['rfid'],
       'key_pos_3' : data['key_positions']['3']['rfid'],
       'key_pos_4' : data['key_positions']['4']['rfid'],
       'key_pos_5' : data['key_positions']['5']['rfid'],
       'key_pos_6' : data['key_positions']['6']['rfid'],
       'key_pos_7' : data['key_positions']['7']['rfid'],
       'key_pos_8' : data['key_positions']['8']['rfid'],
       'key_pos_9' : data['key_positions']['9']['rfid'],
       'key_pos_10' : data['key_positions']['10']['rfid'],
       'key_pos_11' : data['key_positions']['11']['rfid'],
       'key_pos_12' : data['key_positions']['12']['rfid'],
   }

   


   return render_template('rentomat/rentomat_settings.html', rent_data = rent_data, car_list = car_list)


@app.route('/izbaci_kljuc',  methods=['GET', 'POST'])
def izbaci_kljuc():
   
   
   
   position = request.args.get('position')


   # UPDATE JSON

   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
      data = json.load(jsonFile)
   
   rentomat_id = data['rentomat_id']

   data["key_positions"][position]["rfid"] = ""

   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "w") as jsonFile:
      json.dump(data, jsonFile)

   # UPDATE ODOO RFID
   
   update_odoo_rfid(rentomat_id)



   # IZBACI KLJUC

   with open('/home/pi/VSCProjects/selfrentacar/flask_rentomat/komanda.txt', 'w') as f:
               f.write("EMPTY,"+str(position))





   # print(position)
   # return position
 
   return redirect(url_for('rentomat'))




@app.route('/ubaci_kljuc_scan',  methods=['GET', 'POST'])
def ubaci_kljuc_scan():

   if request.method == 'POST':

        position = request.form.get('position')
        rfid = request.form.get('rfid')
        return redirect(url_for('ubaci_kljuc', position=position, rfid=rfid))
   

   position = request.args.get('position')

   return render_template('rentomat/ubaci_kljuc_scan.html', position = position)
   



@app.route('/ubaci_kljuc',  methods=['GET', 'POST'])
def ubaci_kljuc():
   
   
   position = request.args.get('position')
   rfid = request.args.get('rfid')


   # print("Position: "+position)
   # print("RFID: "+rfid)
   

   
   return render_template('rentomat/ubaci_kljuc_final.html', position = position, rfid = rfid), {"Refresh": "7; url=/ubaci_kljuc_final?position="+position+"&rfid="+rfid}



@app.route('/ubaci_kljuc_final',  methods=['GET', 'POST'])
def ubaci_kljuc_final():
   
   
   position = request.args.get('position')
   rfid = request.args.get('rfid')


   print("Position: "+position)
   print("RFID: "+rfid)
   # UPDATE JSON

   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
      data = json.load(jsonFile)
   
   rentomat_id = data['rentomat_id']

   data["key_positions"][position]["rfid"] = rfid

   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "w") as jsonFile:
      json.dump(data, jsonFile)

   # UPDATE ODOO RFID
   
   update_odoo_rfid(rentomat_id)



   # UBACI KLJUC

   with open('/home/pi/VSCProjects/selfrentacar/flask_rentomat/komanda.txt', 'w') as f:
               f.write("FILL,"+str(position))





   # print(position)
   # return position
 
   return redirect(url_for('rentomat'))


@app.route('/')
def root():
   # read_rentomat("root", "0")
   # text_test = gettext('Hello, world!')
   # print(text_test)


   # dropoff = gettext('DROP OFF')
   # reservation = gettext('RESERVATION')
   # pickup = gettext('PICK UP')
   # selectLang = gettext('Select language')
   # english = gettext('English')
   # serbian = gettext('Serbian')
   # russian = gettext('Russian')


   # translation = {
   #    #'dropoff' : dropoff,
   #    'reservation' : reservation,
   #    'pickup' : pickup,
   #    'selectLang' : selectLang,
   #    'english' : english,
   #    'serbian' : serbian,
   #    'russian' : russian
   # }

   
   

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
















################################################

#########      AD HOK REZERVACIJA      #########

################################################







@app.route('/pretraga')
def pretraga():



   response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

   response_data = json.loads(response.text)
   access_token = response_data['access_token']

   
   url = "http://23.88.98.237:8069/api/stock.location"

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)

   # print(response.text)

   allLocations=[]


   if(response_data['count'] != 0):

      for key in response_data['results']:
          
         allLocations.append(key)


   return render_template('rezervacija/pretraga.html', allLocations = allLocations)





@app.route('/listaVozila',  methods=['GET', 'POST'])
def listaVozila():
   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
      data = json.load(jsonFile)
   # print(data)
   pause_time = data['cleaning_time']



   location_from = request.args.get('location_from')
   date_from = request.args.get('date_from')
   location_to = request.args.get('location_to')
   date_to = request.args.get('date_to')




   dt_from = datetime.strptime(date_from, "%Y/%m/%d %H:%M")
   from_timestamp =(int(dt_from.timestamp()))


   dt_to = datetime.strptime(date_to, "%Y/%m/%d %H:%M")
   to_timestamp =(int(dt_to.timestamp()))

   time_with_pause = dt_to + timedelta(hours=pause_time)
   time_with_pause_value =time_with_pause.strftime('%Y/%m/%d %H:%M')



   available_cars=[]


   for key in data['key_positions']:
  
      if (data['key_positions'][key]['rfid']):
         rfid = data['key_positions'][key]['rfid']
         


         response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

         response_data = json.loads(response.text)
         access_token = response_data['access_token']
 

         

         url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('x_key_rfid', '=', '"+rfid+"'), ('date_end', '>', '"+time_with_pause_value+"'),'|',('state','=','open'),('state','=','running')]"




         header_data = {'Access-Token' : str(access_token)}

         response = requests.get(url, headers=header_data)

         response_data = json.loads(response.text)
         print("*************************")
         if(response_data['count'] == 0):


            url = "http://23.88.98.237:8069/api/fleet.vehicle?filters=[('x_key_rfid', '=', '"+rfid+"')]"
            header_data = {'Access-Token' : str(access_token)}

            response = requests.get(url, headers=header_data)

            response_data = json.loads(response.text)
            
            vehicle_id = str(response_data['results'][0]['id'])


            url = "http://23.88.98.237:8069/api/fleet.vehicle/"+vehicle_id
            header_data = {'Access-Token' : str(access_token)}

            response = requests.get(url, headers=header_data)

            response_data = json.loads(response.text)
            vehicle_category_id = response_data['web_price_group_id']
            web_car_id = response_data['web_car_id']
            print(response_data)


            # get prices 


            # print(from_timestamp)
   
            # print(to_timestamp)


            day_num = math.ceil((to_timestamp - from_timestamp)/86400)


            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

            

            


            # print("Days: ", day_num)
            # print("****************")


            default_discount = 0

            if day_num == 1 or day_num == 2:
               print("Popust 20")
               default_discount = 20;
            elif day_num >= 3 and day_num <= 7:
               print("Popust 45")
               default_discount = 45;
            elif day_num >= 8:
               print("Popust 50")
               default_discount = 50;



            total_price = 0

            for x in range(day_num):
               # print("--------------------")
               # print(x)
               current_day = from_timestamp + x*86400
               # print("Current day")
               # print(current_day)

               # print("Duration: ")
               # print(to_timestamp - from_timestamp)

               dt_object = datetime.fromtimestamp(current_day)
               dt_string = dt_object.strftime("%a").lower()
               # print(dt_string)
               key_day = "daily_rate_"+dt_string

               URL = "https://cheapcarhire.rent/wp-json/my/price/getprice?selected_day="+str(key_day)+"&current_day="+str(current_day)+"&date_from="+str(from_timestamp)+"&date_to="+str(to_timestamp)+"&from=1&to=522&vehicle_category_id="+str(vehicle_category_id)
               prices = requests.get(url = URL, headers = headers, data='')
               json_object = json.loads(prices.text)
               print(prices.text)
               day_price = json_object[0][key_day]


               if not json_object[0]['discount_percentage']:
                  print("popust 1")
                  current_discount = default_discount
               else:
                  print("popust 2")
                  current_discount = json_object[0]['discount_percentage']

               dayprice_with_discount = float(day_price) * (100 - float(current_discount))/100

               total_price = total_price + float(dayprice_with_discount)
               price_per_day = float(dayprice_with_discount)



               


               print("discount je: ")
               print(current_discount)
            print("total price: ")
            print(total_price)
            print("****************")

            # DEPOZIT
            
            URL = "https://cheapcarhire.rent/wp-json/my/price/cardeposit?car_id="+str(web_car_id)
            deposit_data = requests.get(url = URL, headers = headers, data='')
            deposit = float(json.loads(deposit_data.text)[0]['fixed_rental_deposit'])
            print("depozit: ")
            print(deposit)

            

            # return 1
            # total_price = 0
            # price_per_day = 0

            # now = datetime.now()
            # dt_string = now.strftime("%a").lower()
            # print("date and time =", dt_string)
            


            # for itemce in json_object:
            #    print(itemce["price_plan_id"])
               
               
            #    print("total price: ", total_price)


            #    if itemce["discount_percentage"] != None:
             

                  
            #       price_per_day = float(float(itemce[key_day])*(100 - float(itemce["discount_percentage"]))/100)
            #       total_price = float(day_num*price_per_day*(100 - float(itemce["discount_percentage"]))/100)
            #    else:
                  
            #       price_per_day = float(itemce[key_day])
            #       total_price = float(day_num*price_per_day)








            vehicle_id = str(response_data['id'])
            vehicle_name = str(response_data['name'])
            vehicle_plate = str(response_data['license_plate'])

            transmission = str(response_data['transmission'])
            fuel_type = str(response_data['fuel_type'])
            seats = str(response_data['seats'])
            doors = str(response_data['doors'])
            # vehicle_plate = str(response_data['results'][0]['vehicle_id']['license_plate'])
            image = str(response_data['image_128'])


            toAdd = {
               'id' : vehicle_id,
               'name' : vehicle_name,
               'plate' : vehicle_plate,
               'transmission' : transmission,
               'fuel_type' : fuel_type,
               'seats' : seats,
               'doors' : doors,
               'image' : image,
               'price_per_day' : price_per_day,
               'total_price' : total_price,
               'deposit' : deposit
            }

            available_cars.append(toAdd)
            # print(available_cars)


      # location_from = request.args.get('location_from')
      # date_from = request.args.get('date_from')
      # location_to = request.args.get('location_to')
      # date_to = request.args.get('date_to')

 


   return render_template('rezervacija/listaVozila.html', cars = available_cars, location_from = location_from, date_from = date_from, location_to = location_to, date_to = date_to)


@app.route('/rezervacijeKorisnik', methods = ['GET', 'POST'])
def rezervacijeKorisnik():



   

   
   
   if request.method == 'POST':


        


      location = request.form.get('location')
      return_date = request.form.get('return_date')
      pricePerDay = request.form.get('pricePerDay')

      print("price per day 1:")
      print(pricePerDay)



      return redirect(url_for('submit_form', location=location, return_date=return_date))
   # return render_template('/rezervacija/rezervacijeKorisnik.html')


   pricePerDay = request.args.get('pricePerDay')
   location_from = request.args.get('location_from')
   date_from = request.args.get('date_from')
   location_to = request.args.get('location_to')
   date_to = request.args.get('date_to')
   carId = request.args.get('carId')
   dayPrice = request.args.get('pricePerDay')

   # print("price per day 2:")
   # print(dayPrice)
   # print("car ID:")
   # print(carId)
   # print("location_from:")
   # print(location_from)


   dt_from = datetime.strptime(date_from, "%Y/%m/%d %H:%M")
   from_timestamp =(int(dt_from.timestamp()))


   dt_to = datetime.strptime(date_to, "%Y/%m/%d %H:%M")
   to_timestamp =(int(dt_to.timestamp()))






   # CHECK IF WINTER SEASON


   is_winter = False

   currentYear = datetime.now().year
   snowchain_date_from = datetime.strptime(str(currentYear)+"/11/1", "%Y/%m/%d")
   timestamp_snow_chain_from =(int(snowchain_date_from.timestamp()))

   snowchain_date_to = datetime.strptime(str(currentYear+1)+"/04/1", "%Y/%m/%d")
   timestamp_snow_chain_to =(int(snowchain_date_to.timestamp()))


   today = date.today()
   current_date = datetime.strptime(str(today), "%Y-%m-%d")
   today_timestamp = (int(current_date.timestamp()))
   
   # current_date = datetime.strptime(str(now_date), "%Y/%m/%d")
   # timestamp_current_date =(int(current_date.timestamp()))

   print(today_timestamp)

   if today_timestamp > timestamp_snow_chain_from and today_timestamp < timestamp_snow_chain_to:
      is_winter = True

   

   response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

   response_data = json.loads(response.text)
   access_token = response_data['access_token']

   url = "http://23.88.98.237:8069/api/stock.location/"+location_from

   header_data = {'Access-Token' : str(access_token)}

   response_locationFrom = requests.get(url, headers=header_data)

   response_data_locationFrom = json.loads(response_locationFrom.text)
   location_from_name = response_data_locationFrom['name']


   url = "http://23.88.98.237:8069/api/stock.location/"+location_to
   response_locationTo = requests.get(url, headers=header_data)

   response_data_locationTo = json.loads(response_locationTo.text)
   location_to_name = response_data_locationTo['name']




   
   url = "http://23.88.98.237:8069/api/stock.location"

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)

   # print(response.text)

   allLocations=[]


   if(response_data['count'] != 0):

      for key in response_data['results']:
          
         allLocations.append(key)
   


   url = "http://23.88.98.237:8069/api/product.product"

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)

   

   allOptions=[]


   if(response_data['count'] != 0):

      for key in response_data['results']:
         # print(key)
         product_id = str(key['id'])



         url = "http://23.88.98.237:8069/api/product.product/"+product_id

         header_data = {'Access-Token' : str(access_token)}

         response = requests.get(url, headers=header_data)

         response_data = json.loads(response.text)

         id = response_data['id']
         name = response_data['name']
         price = response_data['lst_price']

         add_with_pricce = {
            'id' : id,
            'name' : name,
            'price' : price
         }

         # print(key)

         allOptions.append(add_with_pricce)
   #print(allOptions)
   # print("Id je: "+str(allOptions['id']))
  

   # if is_winter:
   #    add_with_pricce = {
   #          'id' : '22',
   #          'name' : 'Snow Chains. Required from 01.11.2023-01.04.2024. Price Per Rental:',
   #          'price' : '25'
   #       }

   #       # print(key)

   #    allOptions.append(add_with_pricce)
   # else:
   #    print("Nije zima")

   day_num = math.ceil((to_timestamp - from_timestamp)/86400)

   car_url = "http://23.88.98.237:8069/api/fleet.vehicle/"+carId

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(car_url, headers=header_data)

   response_data_car = json.loads(response.text)

   # print("Car data")
   # print(response.text)   
   # print("car data end")

   #print(vehicle_id)
   vehicle_brand = str(response_data_car['brand_id']['name'])
   vehicle_name = str(response_data_car['model_id']['name'])

   transmission = str(response_data_car['transmission'])
   category = str(response_data_car['category_id']['name'])
   vehicle_category_id = response_data_car['driver_identification_no']
   web_car_id = response_data_car['web_car_id']

   print("Webcar id:")
   print(web_car_id)



   # DEPOZIT
   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
   URL = "https://cheapcarhire.rent/wp-json/my/price/cardeposit?car_id="+str(web_car_id)
   deposit_data = requests.get(url = URL, headers = headers, data='')
   deposit = json.loads(deposit_data.text)[0]['fixed_rental_deposit']
   deposit_price = float(json.loads(deposit_data.text)[0]['price'])*float(day_num)
   # print("depozit: ")
   # print(deposit_data.text)
   # print(deposit)









   # EXTRAS
   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
   URL = "https://cheapcarhire.rent/wp-json/my/price/extras"
   extras_data = requests.get(url = URL, headers = headers, data='')
   extras_web = json.loads(extras_data.text)


   # print("Extras")
   # print(extras_data.text)
   # print("Extras end")

   
   # get prices 


   # print(from_timestamp)

   # print(to_timestamp)

   duration_time = to_timestamp - from_timestamp






   # print("time stamp duration: ")
   # print(duration_time)


   


   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

   URL = "https://cheapcarhire.rent/wp-json/my/price/getprice?date_from="+str(from_timestamp)+"&date_to="+str(to_timestamp)+"&from=1&to=522&vehicle_category_id="+str(vehicle_category_id)

   prices = requests.get(url = URL, headers = headers, data='')


   # print("Days: ", day_num)
   # print(prices.text)
   json_object = json.loads(prices.text)


   total_price = 0
   price_per_day = 0

   now = datetime.now()
   dt_string = now.strftime("%a").lower()
   # print("current day =", dt_string)
   key_day = "daily_rate_"+dt_string


   for itemce in json_object:
      # print(itemce["price_plan_id"])
      # print("total price: ", total_price)

      if itemce["discount_percentage"] != None:
         price_per_day = float(float(itemce[key_day])*(100 - float(itemce["discount_percentage"]))/100)
         total_price = float(day_num*price_per_day*(100 - float(itemce["discount_percentage"]))/100)
      else:
         price_per_day = float(itemce[key_day])
         total_price = float(day_num*price_per_day)

   


   # EXTRAS PRICES

   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

   URL = "https://cheapcarhire.rent/wp-json/my/price/getpriceextras?date_from="+str(from_timestamp)+"&date_to="+str(to_timestamp)+"&from=1&to=522&vehicle_category_id="+str(web_car_id)

   prices_extras = requests.get(url = URL, headers = headers, data='')


   # print("Price Extras: ")
   # print(prices_extras.text)
   json_object = json.loads(prices_extras.text)



   for itemce in json_object:
      # print(itemce["price_plan_id"])
      # print("total price: ", total_price)

      if itemce["discount_percentage"] != None:
         price_per_day_extra = float(float(itemce["price"])*(100 - float(itemce["discount_percentage"]))/100)
         total_price_extra = float(day_num*price_per_day*(100 - float(itemce["discount_percentage"]))/100)
      else:
         price_per_day_extra = float(itemce["price"])
         total_price_extra = float(day_num*price_per_day_extra)






 # EXTRAS PRICES TYRES

   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

   URL = "https://cheapcarhire.rent/wp-json/my/price/getpriceextrastyres?date_from="+str(from_timestamp)+"&date_to="+str(to_timestamp)+"&from=1&to=522&vehicle_category_id="+str(web_car_id)

   prices_extras_tyres = requests.get(url = URL, headers = headers, data='')


   print("Price Extras: ")
   print(prices_extras_tyres.text)
   json_object_tyres = json.loads(prices_extras_tyres.text)


   tyres_price = json_object_tyres[0]['price']
   tyres_price_discount = json_object_tyres[0]['discount_percentage']
   extra_name_tyres = json_object_tyres[0]['extra_name']


   if tyres_price_discount != None:
      total_price_extra_tyres = float(day_num*float(tyres_price)*(100 - float(tyres_price_discount))/100)
   else:
      total_price_extra_tyres = float(day_num*tyres_price)

   
   
   tyres = {
      'extra_name_tyres' : extra_name_tyres,
      'total_price_extra_tyres' : total_price_extra_tyres

   }
   print(tyres)


   # fuel_type = str(response_data_car['results'][0]['vehicle_id']['fuel_type'])
   # seats = str(response_data_car['results'][0]['vehicle_id']['seats'])
   # doors = str(response_data_car['results'][0]['vehicle_id']['doors'])
   # # vehicle_plate = str(response_data['results'][0]['vehicle_id']['license_plate'])
   # image = str(response_data_car['results'][0]['vehicle_id']['image_128'])

   


   toAdd = {
       'location_from_id' : location_from,
       'location_to_id' : location_to,
       'location_from': location_from_name,
       'date_from': date_from,
       'location_to': location_to_name,
       'date_to': date_to,
       'carId' : carId,
      'brand' : vehicle_brand,
      'name' : vehicle_name,
      'transmission': transmission,
      'category': category,
      'price': float(dayPrice),
      'day_num' : int(day_num),
      'price_per_day_extra' : price_per_day_extra,
      'total_price_extra' : total_price_extra,
      'deposit' : float(deposit),
      'deposit_price' : float(deposit_price)
   }

   years_range = list(range(1943, 2013))
   months_range = list(range(1, 13))
   days_range = list(range(1, 32))

   
   # print("ALL OPTIONS")
   # print(allOptions)
   # print("ALL OPTIONS END")


   return render_template('/rezervacija/rezervacijeKorisnik.html',tyres=tyres, is_winter=is_winter, extras_web=extras_web, days_range=days_range, months_range=months_range, years_range=years_range,carDetails = toAdd, allLocations = allLocations, allOptions = allOptions)




@app.route('/submit_form',  methods=['GET', 'POST'])
def submit_form():
   
   
   
   options = request.args.getlist('options')
   deposit_val = request.args.get('deposit_val')

   print(options)

   deposit_amt = 0

   for el in options:
      if el == "13":
            deposit_amt = 0
      else:
         deposit_amt = deposit_val
   
   if not options:
      deposit_amt = deposit_val

   # print("&&&&&&&&")
   # print(deposit_amt)
   # print("&&&&&&&&")
   carid = request.args.get('carid')
   grand_value = request.args.get('grand_total_val')


   location_from_id = request.args.get('location_from_id')
   location_to_id = request.args.get('location_to_id')

   location = request.args.get('location')
   return_date = request.args.get('date_to')
   start_date_input = request.args.get('start_date_input')


   

   # casco_checkbox = request.args.get('casco_checkbox')
   # tyres_checbox = request.args.get('tyres_checbox')

   # if(casco_checkbox == 'on'):
   #     casco = "1"
   #     deposit_amt = 0
   # else :
   #     casco = "0"
   #     deposit_amt = 600
   

   # if(tyres_checbox == 'on'):
   #     tyres = "1"
   # else :
   #     tyres = "0"





   
   # print("deposit amount je: ")
   # print(deposit_amt)


   # USER DETAILS

   first_name = request.args.get('first_name')
   last_name = request.args.get('last_name')
   year = request.args.get('year')
   month = request.args.get('month')
   day = request.args.get('day')
   address = request.args.get('address')
   city = request.args.get('city')
   country = request.args.get('country')
   phone = request.args.get('phone')
   email = request.args.get('email')
   comments = request.args.get('comments')
   days_num_var = request.args.get('days_num_var')
   birthday = year+'-'+month+'-'+day


   rent_details = {
       'carId': carid,
       'grand_value' : grand_value,
       # 'location': location_to_id,
       'start_date' : start_date_input,
       'rent_from' : location_from_id,
       'return_location' : location_to_id,
       'return_date': return_date,
      #  'casco' : casco,
      #  'tyres' : tyres,
       'options' : options,
       'days_num_var' : days_num_var,
       'total_rent' : grand_value,
       'deposit_amt' : deposit_amt
   }


   # print(rent_details)


   user_details = {
       'first_name': first_name,
       'last_name': last_name,
       'birthday': birthday,
       'address' : address,
       'city' : city,
       'country' : country,
       'phone' : phone,
       'email' : email,
       'comments' : comments
   }

   # print(user_details)

   contract_id = create_contract(rent_details, user_details)


   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']


   header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

   url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id+"/change_odometer"
   
   
   response_odo = requests.put(url, headers=header_data)

   response_data_od = json.loads(response_odo.text)
   print("**********************")
   print(response_data_od)
   print("**********************")
   # contract_id = str(response_data['results'][0]['id'])


   return render_template('/rezervacija/submit_form_confirm.html', contract_id = contract_id), {"Refresh": "3; url=/paymentPage?contract_id="+contract_id}

   

   

   # print("carid je:" + carid)
   # print("lokacija je:" + location)
   # print("datum i vreme preuzimanja je:" + start_date_input)
   # print("datum i vreme vracanja je:" + return_date)
   # print("casco_checkbox je:" + casco)
   # print("tyres_checbox je:" + tyres)

   # print("***********************")

   # print("first_name je:" + first_name)
   # print("last_name je:" + last_name)
   # print("year je:" + year)
   # print("month je:" + month)
   # print("day je:" + day)
   # print("address je:" + address)
   # print("city je:" + city)
   # print("country je:" + country)
   # print("phone je:" + phone)
   # print("email je:" + email)
   # print("comments je:" + comments)


   return render_template('/rezervacija/submit_form.html')






@app.route('/paymentPage', methods = ['GET', 'POST'])
def paymentPage():

   contract_id = request.args.get('contract_id')
   payment_succes = request.args.get('payment_succes')
   payment_type = request.args.get('payment_type')
   # print(payment_succes)
   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']


   header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

   url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id
   
   
   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)


   print(url)
   print(response.text)
   print("******************")


   rent_amt = response_data['total_rent']
   rent_currency = response_data['currency_id']
   deposit_amt = response_data['deposit_amt']
   is_payment_received = response_data['is_payment_received']
   is_deposid_received = response_data['is_deposid_received']
   deposit_received = response_data['deposit_received']


   options = response_data['option_ids']['option']
   print(options)
   
   casco_id = 13

   is_casco = 0
   if options:
      if isinstance(options, int):
         if options == casco_id:
            is_casco = 1
      else:
         if casco_id in options:
            is_casco = 1
   
   print("sa casco?")
   print(is_casco)

   # print(type(options))

   # print(len(options))

   # if 13 in options:
   #    print("ima")
   # else:
   #    print("nema")

   

   return render_template('/rezervacija/paymentPage.html', is_casco = is_casco, payment_type = payment_type, payment_succes = payment_succes, contract_id = contract_id, rent_amt = rent_amt, rent_currency = rent_currency, deposit_amt = deposit_amt, deposit_received = deposit_received, is_payment_received = is_payment_received, is_deposid_received = is_deposid_received)









@app.route('/payNow', methods = ['GET', 'POST', 'PUT'])
def payNow():
   contract_id = request.args.get('contract_id')
   payment_type = request.args.get('payment_type')

   return render_template('/preuzimanje/payNow.html'), {"Refresh": "1; url=/paymentProcess?contract_id="+contract_id+"&payment_type="+payment_type}



@app.route('/paymentProcess', methods = ['GET', 'POST', 'PUT'])
def paymentProcess():
 
   contract_id = request.args.get('contract_id')
   payment_type = request.args.get('payment_type')
   

   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']

   url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)

   rent_amt = response_data['rent_amt']*100
   deposit_amt = response_data['deposit_amt']*100


   # print("Payment type: ")
   # print(payment_type)
   
   
   final_deposit = binascii.hexlify(bytes(str(int(response_data['deposit_amt'])), encoding='utf-8')).decode()
   
   
   print(response_data['currency_id']['name'])

   if response_data['currency_id']['name'] == "EUR":
      amountCurrency = "393431"
      # amountCurrency = "393738" # EUR
   else:
      amountCurrency = "393431" # RSD

   if payment_type == "0":
      transactionType = "3031"
      final_val = binascii.hexlify(bytes(str(int(rent_amt)), encoding='utf-8')).decode()
   elif payment_type == "1":
      transactionType = "3032"
      final_val = binascii.hexlify(bytes(str(int(deposit_amt)), encoding='utf-8')).decode()
   elif payment_type == "2":
      transactionType = "3031"

      casco_price = 25*100

      final_val = binascii.hexlify(bytes(str(int(casco_price)), encoding='utf-8')).decode()



   send_dict = { "identifier" : "3030",
      "terminalID" : "3030",
      "sourceID" : "3030",
      "sequentialNumber" : "30303030",
      "transactionType" : transactionType,
      "printerFlag" : "31",
      "cashierID" : "3030",
      "transactionNumber" : "",
      "fieldSeparator1" : "1C",
      "transactionAmount1" : final_val,
      "fieldSeparator2" : "1C",
      "fieldSeparator3" : "1C",
      "amountExponent" : "2B30",
      "fieldSeparator4" : "1C",
      "amountCurrency" : amountCurrency,
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


   message_data = ""


   for key in send_dict:
      message_data = str(message_data) + str(send_dict[key])

   message_data = message_data + str(ETX)
   ack_message_data_tmp = ACK + ETX
   nack_message_data_tmp = NACK + ETX

   lrc = xor_sum(message_data)

   message_data = STX+STX+message_data+str(lrc)



   TCP_IP = '192.168.1.113'    
   TCP_PORT = 3000   

   sock_payten = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   status = sock_payten.connect((TCP_IP, TCP_PORT))


   payment_succes = False

   dobar_format = bytearray.fromhex(message_data).decode()


   i = 1

   try:
      
      
      for i in range(1):



         sent = sock_payten.sendto(bytes(dobar_format, encoding='iso-8859-2'),(TCP_IP,TCP_PORT))

         data = sock_payten.recv(1024)
         print("prvi prijem")
         print(data)
         if data.hex() == ACK:
               data = sock_payten.recv(1024)
               sent = sock_payten.sendto(bytes(ACK, encoding='iso-8859-2'),(TCP_IP,TCP_PORT))
               hold = True
               print("drugi prijem")
               print(data)




               while hold == True:
                  print("uso u hold")
                  data = sock_payten.recv(1024)
                  print(data)
                  print("data je primljen")
                  message_identifier = data.hex()
                  print("treci prijem")
                  print(data)
                  if message_identifier[2:6] == "3130":   # kod 10
                     print("uso u dobio 10")
                     transaction_data = data
                     hold = False
                     payment_succes = True
                  elif message_identifier[2:6] == "3236":
                     print("TRANSAKCIJA NIJE DOZVOLJEA")
                     hold = False
               
               sent = sock_payten.sendto(bytes(ACK, encoding='iso-8859-2'),(TCP_IP,TCP_PORT))

   except:
      print("Except error")


   if payment_succes:
      # update payment status
      response = requests.get(
               "http://23.88.98.237:8069/api/auth/get_tokens",
               params={"username": "odoo@irvas.rs", "password": "irvasadm"}
         )

      response_data = json.loads(response.text)
      access_token = response_data['access_token']

      header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}


      url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id


      if payment_type == "0":
         data_update = json.dumps({'is_payment_received': 'True',})
      else:
         data_update = json.dumps({'is_deposid_received': 'True',})


      



      response = requests.put(url, data=data_update, headers=header_data)

   return redirect(url_for('paymentPage', contract_id=contract_id, payment_succes = payment_succes, payment_type = payment_type))

   #  return render_template('/preuzimanje/paymentDetails.html', data = dict_example)
   transaction_data = b'\x02100000000001020000260006031123132541\x1c000000005200\x1c\x1c+0\x1c941\x1cC\x1c5351529999999999999\x1c99\x1c\x1c\x1c225048\x1cUPTTEST19\x1c11111111\x1cMASTERCARD\x1c\x1c\x1c\x1c\x1c\x1c\x1cODOBRENO                 \x1c\x1c\x1c8407A0000000041010950500000080019F12104465626974204D6173746572636172649F26085455AD1ABEEF589F9F2701809F34031F0302\x1c1\x1c\x1c0\x1c\x1c00\x1cC1\x1c\x1c\x1c\x1c\x1c444411534444\x1c0\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c000000000000\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c01\x1c\x1c\x1c\x1c\x1c\x03\x12'


   dict_example = {}

   for k in range(0,63,1):
      
      left_text = transaction_data.split(b'\x1c')[k]
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
         dict_example['transactionDate'] = str(string[25:27])+"."+str(string[27:29])+".20"+str(string[29:31])+"."
         dict_example['transactionTime'] = string[31:33]+":"+string[33:35]+"h"
      if k == 1:
         # print(string)
         dict_example['transactionAmount1'] = "{:.2f}".format(float(string)/100).replace('.', ',')
      if k == 3:
         # print(string)
         dict_example['amountExponent'] = string
      if k == 4:
         # print(string)


         if string == "941":
             cur = "RSD"
         else:
             cur = "€"

         dict_example['amountCurrency'] = cur
      if k == 5:
         # print(string)
         dict_example['cardDataSource'] = string
      if k == 6:
         # print(string)
         dict_example['cardNumber'] = string[0:4]+"*********"
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
      
      



   #pretty = json.dumps(dict_example)
   

   return render_template('/preuzimanje/paymentDetails.html', data = dict_example)




@app.route('/create_final_contract', methods = ['GET', 'POST'])
def create_final_contract():

   contract_id = request.args.get('contract_id')



   

   


   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']


   header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

   url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id
   
   
   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)


   print("******************")
   print(response.text)
   print("******************")

   base_url = "https://selfcar.naisrobotics.com"
   access_url = response_data["access_url"]
   token = response_data["access_token"]
   
   


   



   # print(base_url)
   # print(access_url)
   # print(token)
   final_url = base_url + access_url + "?access_token=" + token
   # print(final_url)
   # contract_id = str(response_data['results'][0]['id'])




   # print(contract_id)
   #return redirect(final_url)
   position = 3
   return render_template('odoo.html', contract_id = contract_id, position = position, iframe= final_url)
   return render_template('/rezervacija/takekey.html', final_url = final_url), {"Refresh": "5; url=/create_final_contract?contract_id="+contract_id}



@app.route('/preuzimanjeKljuc', methods = ['GET', 'POST', 'PUT'])
def preuzimanjeKljuc():
   contract_id = request.args.get('contract_id')

   return render_template('/preuzimanje/preuzimanjeKljuc.html'), {"Refresh": "2; url=/preuzmiKljuc?contract_id="+contract_id}

@app.route('/preuzmiKljuc', methods = ['GET', 'POST', 'PUT'])
def preuzmiKljuc():



   # PREUZIMANJE RFID BROJA IZ UGOVORA


   contract_id = request.args.get('contract_id')
   
 

   try:
      rfid_num = get_rfid(contract_id)
   except:
       return render_template('/errors/non_exist_rfid_in_database.html')


   key_rfid = rfid_num



   try:

      with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
         data = json.load(jsonFile)

      

      key_position = ''
      for key in data['key_positions']:
         if (data['key_positions'][key]['rfid'] == key_rfid):
         
            key_position = key
      rentomat_id = data['rentomat_id']


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

         data_update = json.dumps({'state': 'running',})
         response = requests.put(url, data=data_update, headers=header_data)




         ########################

         # STAMPANJE UGOVORA

         ########################

      ####################################

         ##    CITANJE IZ MOTOR KONTROLERA ##

         ####################################

         function_to_execute = "EMPTIED"
         position = key_position

         ser = serial.Serial('/dev/myUSB', 9600, timeout=1)

         return_data = {}
         line_num = 0
         hold = True
         while hold:


            receivedData = ser.readline()


            if len(receivedData) >= 1:
               line_num = line_num +1
               receive_hex = receivedData.hex().replace('0a', '')
               receive_hex_bytes = bytes(receive_hex, encoding='utf-8')
               binary_string = codecs.decode(receive_hex_bytes, "hex")
               sitrng_to_check = str(binary_string, 'utf-8')

               if line_num == 1:
                     print("funcija je: ")
                     print(sitrng_to_check)
                     return_data["function_send"] = function_to_execute

                     if function_to_execute == sitrng_to_check.replace('\r', ''):
                        return_data["function_status"] = "OK"
                     else:
                        return_data["function_status"] = "NO"

                     return_data["function"] = sitrng_to_check.replace('\r', '')
                  
               
               if line_num == 2:
                     print("pozicija je: ")
                     print(sitrng_to_check.split("Pozicija:",1)[1])
                     return_data["position_send"] = sitrng_to_check.split("Pozicija:",1)[1]

                     if position == int(sitrng_to_check.split("Pozicija:",1)[1]):
                        return_data["position_status"] = "OK"
                     else:
                        return_data["position_status"] = "NO"
                     return_data["position"] = sitrng_to_check.split("Pozicija:",1)[1]
                     hold = False
               
         print(return_data)

         

         return redirect(url_for('print_final_contract', contract_id = contract_id))
   
         











         return render_template('/preuzimanje/preuzimanjeKljuc.html'), {"Refresh": "10; url=/print_final_contract?contract_id="+contract_id}
      else:
         
         return render_template('/errors/non_exist_rfid.html')
   except:
       return render_template('/errors/general_except.html')




@app.route('/print_final_contract', methods = ['GET', 'POST'])
def print_final_contract():

   contract_id = int(request.args.get('contract_id'))
   # print(contract_id)
  

   response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

   response_data = json.loads(response.text)
   access_token = response_data['access_token']


   # print("Token: "+access_token)

   response_pdf = requests.get(
      'http://23.88.98.237:8069/api/report/get_pdf',
      headers = {
         'Content-Type': 'text/html; charset=utf-8',
         'Access-Token': access_token
      },
      data = json.dumps({
         "report_name":  "fleet_rent.report_fleet_rent_pdf",
         "ids": [contract_id],
      }),
   )

   # print("_________________")
   # print(response_pdf.text)
   # print("_________________")

   pdf_file = str(response_pdf.text[1: len(response_pdf.text)-1])



   stripped = pdf_file.replace('\\n', '')
   bytes = b64decode(stripped, validate=True)

   f = open("temp.pdf", "wb")
   f.write(bytes)
   f.close()
   os.system("lp temp.pdf")




   return render_template('/rezervacija/print_contract.html'), {"Refresh": "5; url=/"}







####################################################

################      END AD HOK    ################

####################################################

















#####################################################

##############      VRACANJE VOZILA    ##############

#####################################################




# VRACANJE

@app.route('/vracanjeHome', methods = ['GET', 'POST'])
def vracanjeHome():
    if request.method == 'POST':
        rfid = request.form.get('rfid')
        return redirect(url_for('vracanjeStatus', rfid_input=rfid))
    return render_template('/vracanje/vracanjeHome.html')

@app.route('/vracanjeStatus',  methods=['GET', 'POST'])
def vracanjeStatus():


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

      rfid_input = request.args.get('rfid_input')



      # PRoVERA DA POSTOJI UGOVOR VEZAN ZA OVAJ KLJUC/VOZILO


      response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

      response_data = json.loads(response.text)
      access_token = response_data['access_token']
      #return(access_token)

      rfid_num = str(rfid_input)
      

      url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('x_key_rfid', '=', '"+rfid_num+"'), ('state', '=', 'running')]"

      header_data = {'Access-Token' : str(access_token)}

      response = requests.get(url, headers=header_data)

      response_data = json.loads(response.text)

      # print(response_data)
      
      
      if(response_data['count'] == 0):

         return render_template('/errors/no_contract.html')
      else:
      
         return render_template('/vracanje/vracanjeStatus.html', rfid_input = rfid_input)







      
   
   else:
       
       return render_template('/errors/no_empty_position.html')





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
        return redirect(url_for('vracanjeVratiKljuc', rating=rating, rfid_input=rfid_input, status=status, comment=comment))


   status = request.args.get('status')
   rfid_input = request.args.get('rfid')
   rating = request.args.get('rating')

   return render_template('/vracanje/vracanjePrimedbe.html', rfid_input = rfid_input, status = status, rating=rating)



 
@app.route('/vracanjeVratiKljuc',  methods=['GET', 'POST'])
def vracanjeVratiKljuc():

   rating = request.args.get('rating')
   rfid_input = request.args.get('rfid_input')
   status = request.args.get('status')
   comment = "neki komentar"

   return render_template('/vracanje/vracanjeOtvori.html', rating=rating, rfid_input=rfid_input, status=status, comment=comment), {"Refresh": "5; url=/vracanjeOtvori?rating="+rating+"&rfid_input="+rfid_input+"&status="+status+"&comment="+comment}







@app.route('/vracanjeOtvori',  methods=['GET', 'POST'])
def vracanjeOtvori():

 
 
   rating = request.args.get('rating')
   rfid_input = request.args.get('rfid_input')
   status = request.args.get('status')
   comment = request.args.get('comment')
   print("RFID")
   print(rfid_input)
   print("Kraj")

   

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
      





      
























      # hold_motor("FILED", first_empty_key_position)
      # UPDATE JSON

      with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
         data = json.load(jsonFile)

      data["key_positions"][first_empty_key_position]["rfid"] = rfid_input

      with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "w") as jsonFile:
         json.dump(data, jsonFile)

      # UPDATE ODOO RFID
      
      
      update_odoo_rfid(rentomat_id)



      # UPDATE STATUSA UGOVORA
      # preko API-ja da se dobije BROJ UGOVORA (STATUS, pozcija kljuca za vozilo)


      response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

      response_data = json.loads(response.text)
      access_token = response_data['access_token']
      #return(access_token)

      rfid_num = str(rfid_input)
      

      url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('x_key_rfid', '=', '"+rfid_num+"'), ('state', '=', 'running')]"

      header_data = {'Access-Token' : str(access_token)}

      response = requests.get(url, headers=header_data)

      response_data = json.loads(response.text)

      # print(response_data)
      
      contract_id = str(response_data['results'][0]['id'])





      header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

      url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id
     
     
      data_update = json.dumps({'state': 'done',})
      response = requests.put(url, data=data_update, headers=header_data)






      # SLANJE PODATAKA O UTISCIMA




      ####################################

      ##    CITANJE IZ MOTOR KONTROLERA ##

      ####################################

      function_to_execute = "FILLED"
      position = first_empty_key_position

      ser = serial.Serial('/dev/myUSB', 9600, timeout=1)

      return_data = {}
      line_num = 0
      hold = True
      while hold:


         receivedData = ser.readline()


         if len(receivedData) >= 1:
            line_num = line_num +1
            receive_hex = receivedData.hex().replace('0a', '')
            receive_hex_bytes = bytes(receive_hex, encoding='utf-8')
            binary_string = codecs.decode(receive_hex_bytes, "hex")
            sitrng_to_check = str(binary_string, 'utf-8')

            if line_num == 1:
                  print("funcija je: ")
                  print(sitrng_to_check)
                  return_data["function_send"] = function_to_execute

                  if function_to_execute == sitrng_to_check.replace('\r', ''):
                     return_data["function_status"] = "OK"
                  else:
                     return_data["function_status"] = "NO"

                  return_data["function"] = sitrng_to_check.replace('\r', '')
               
            
            if line_num == 2:
                  print("pozicija je: ")
                  print(sitrng_to_check.split("Pozicija:",1)[1])
                  return_data["position_send"] = sitrng_to_check.split("Pozicija:",1)[1]

                  if position == int(sitrng_to_check.split("Pozicija:",1)[1]):
                     return_data["position_status"] = "OK"
                  else:
                     return_data["position_status"] = "NO"
                  return_data["position"] = sitrng_to_check.split("Pozicija:",1)[1]
                  hold = False
            
      print(return_data)

      

      return redirect(url_for('vracanjeHvala', rating=rating, rfid_input=rfid_input, status=status, comment=comment, contract_id = contract_id))
      # return render_template('/vracanje/vracanjeOtvori.html', rating=rating, rfid_input=rfid_input, status=status, comment=comment, contract_id = contract_id), {"Refresh": "5; url=/vracanjeHvala"}





      



      
    
   else:
       return render_template('/errors/no_empty_position.html')





      
# def hold_motor(function_to_execute, position):      

#    ser = serial.Serial('/dev/myUSB', 9600, timeout=1)

#    return_data = {}
#    line_num = 0
#    hold = True
#    while hold:


#       receivedData = ser.readline()


#       if len(receivedData) >= 1:
#          line_num = line_num +1
#          receive_hex = receivedData.hex().replace('0a', '')
#          receive_hex_bytes = bytes(receive_hex, encoding='utf-8')
#          binary_string = codecs.decode(receive_hex_bytes, "hex")
#          sitrng_to_check = str(binary_string, 'utf-8')

#          if line_num == 1:
#                print("funcija je: ")
#                print(sitrng_to_check)
#                return_data["function_send"] = function_to_execute

#                if function_to_execute == sitrng_to_check.replace('\r', ''):
#                   return_data["function_status"] = "OK"
#                else:
#                   return_data["function_status"] = "NO"

#                return_data["function"] = sitrng_to_check.replace('\r', '')
            
         
#          if line_num == 2:
#                print("pozicija je: ")
#                print(sitrng_to_check.split("Pozicija:",1)[1])
#                return_data["position_send"] = sitrng_to_check.split("Pozicija:",1)[1]

#                if position == int(sitrng_to_check.split("Pozicija:",1)[1]):
#                   return_data["position_status"] = "OK"
#                else:
#                   return_data["position_status"] = "NO"
#                return_data["position"] = sitrng_to_check.split("Pozicija:",1)[1]
#                hold = False
         
#    print(return_data)
 
@app.route('/vracanjeHvala',  methods=['GET', 'POST'])
def vracanjeHvala():


   contract_id = int(request.args.get('contract_id'))
   
   print("contract id: ")
   print(contract_id)
   print("kraj")
   ##################################
   # STAMPANJE POTVRDE O VRACENOM KLJUCU
   ##################################



   response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

   response_data = json.loads(response.text)
   access_token = response_data['access_token']


   response_pdf = requests.get(
      'http://23.88.98.237:8069/api/report/get_pdf',
      headers = {
         'Content-Type': 'text/html; charset=utf-8',
         'Access-Token': access_token
      },
      data = json.dumps({
         "report_name":  "fleet_rent.key_return_report_pdf",
         "ids": [contract_id],
      }),
   )

   # print("pdf start")
   # print(response_pdf.text)
   # print("pdr end")


   pdf_file = str(response_pdf.text[1: len(response_pdf.text)-1])



   stripped = pdf_file.replace('\\n', '')
   bytes = b64decode(stripped, validate=True)

   f = open("temp.pdf", "wb")
   f.write(bytes)
   f.close()
   os.system("lp temp.pdf")
   

   ##################################





   return render_template('/vracanje/vracanjeHvala.html'), {"Refresh": "5; url=/"}








##########################################################

##############      VRACANJE VOZILA KRAJ    ##############

##########################################################













##########################################################

##############      PREUZIMANJE VOZILA     ###############

##########################################################





@app.route('/preuzimanjeHome', methods = ['GET', 'POST'])
def preuzimanjeHome():

   if request.method == 'POST':
        ugovor_link = request.form.get('ugovor_link')
        return redirect(url_for('preuzimanjeUgovorEdit', ugovor_link=ugovor_link))



   return render_template('/preuzimanje/preuzimanjeHome.html')




@app.route('/preuzimanjeUgovor/', methods = ['GET', 'POST'])
def preuzimanjeUgovor():


   # if request.method == 'POST':
   #    ugovor_link = request.form.get('ugovor_link')
   #    return redirect(url_for('preuzimanjeUgovor', ugovor_link=ugovor_link))



   # ugovor_link = "https://selfcar.naisrobotics.com/my/carrental_contract/296?access_token=e0650911-9531-4d02-b1c5-c83340c60bcc"
   ugovor_link = request.args.get('ugovor_link')


   # print("Ugovor link: ")
   # print(ugovor_link)
   

   first_part = ugovor_link.split('?')[0]

   Segments = first_part.rpartition('/')
   contract_id = Segments[2]
   

   # print("ugovor br:")
   # print(contract_id)

   try:
 


      response = requests.get(
               "http://23.88.98.237:8069/api/auth/get_tokens",
               params={"username": "odoo@irvas.rs", "password": "irvasadm"}
         )

      response_data = json.loads(response.text)
      access_token = response_data['access_token']

      header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

   
      url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id

      response = requests.get(url, headers=header_data)

      response_data = json.loads(response.text)

      print(contract_id)
      print("ugovor")
      print(response.text)
      print("ugovor kraj")














      location_from = response_data['rent_from']['id']
      location_from_name = response_data['rent_from']['name']
      date_from = response_data['date_start']
      location_to = response_data['return_location']['id']
      location_to_name = response_data['return_location']['name']
      date_to = response_data['date_end']
      carId = response_data['vehicle_id']['id']
      carName = response_data['vehicle_id']['name']
      tenant = response_data['tenant_id']['name']
      currentOptions = response_data['option_ids']['option']

      
      

      print(type(currentOptions))
      print(currentOptions)

      if currentOptions:
         if isinstance(currentOptions, int):
            currentOptionsItems = []
            currentOptionsItems.append(currentOptions)
         else:
            currentOptionsItems = currentOptions
      else:
         currentOptionsItems = []



      print("Izabrane opcije")
      print(currentOptionsItems)


      deposit_required = True
      pay_deposit = True

      pay_payment = True

      if 13 in currentOptionsItems:
         deposit_required = False
         print("ima ga 13 u nizu")


      is_payment_received = response_data['is_payment_received']
      is_deposid_received = response_data['is_deposid_received']


      if deposit_required:
         if is_deposid_received:
            pay_deposit = False
      else: 
         pay_deposit = False

      if is_payment_received:
            pay_payment = False
      

      if pay_deposit:
         print("Plati depozit")
      else:
         print("Plati depozit NE TREBA")
      
      if pay_payment:
         print("Plati payment")
      else:
         print("Plati payment NE TREBA")


      # print(location_from)
      # print(date_from)
      # print(location_to)
      # print(date_to)
      # print(carId)

      
      

      # url = "http://23.88.98.237:8069/api/stock.location/"+location_from

      # header_data = {'Access-Token' : str(access_token)}

      # response_locationFrom = requests.get(url, headers=header_data)
      # print(response_locationFrom.text)
    
      # response_data_locationFrom = json.loads(response_locationFrom.text)


      # location_from_name = response_data_locationFrom['name']
      # print(location_from_name)
      

      # url = "http://23.88.98.237:8069/api/stock.location/"+location_to
      # response_locationTo = requests.get(url, headers=header_data)

      # response_data_locationTo = json.loads(response_locationTo.text)
      # location_to_name = response_data_locationTo['name']


      

      
      url = "http://23.88.98.237:8069/api/stock.location"

      header_data = {'Access-Token' : str(access_token)}

      response = requests.get(url, headers=header_data)

      response_data = json.loads(response.text)


      # print("stock locations")
      # print(response.text)
      # print("stock locations kraj")

      # print(response.text)

      allLocations=[]


      if(response_data['count'] != 0):

         for key in response_data['results']:
            
            allLocations.append(key)
      


      url = "http://23.88.98.237:8069/api/product.product"

      header_data = {'Access-Token' : str(access_token)}

      response = requests.get(url, headers=header_data)

      response_data = json.loads(response.text)
      # print("products")
      # print(response.text)
      # print("products kraj")
      

      allOptions=[]

      
      if(response_data['count'] != 0):

         for key in response_data['results']:
            # print(key)
            product_id = str(key['id'])

            # print("product id")
            # print(product_id)
            # print(key['name'])

            url = "http://23.88.98.237:8069/api/product.product/"+product_id

            header_data = {'Access-Token' : str(access_token)}

            response = requests.get(url, headers=header_data)

            response_data = json.loads(response.text)

            id = response_data['id']
            name = response_data['name']
            price = response_data['lst_price']

            add_with_pricce = {
               'id' : id,
               'name' : name,
               'price' : price
            }

            # print(key)
            if response_data['id'] == 13 or response_data['id'] == 15:
               allOptions.append(add_with_pricce)
      # print(allOptions)
      # print("Id je: "+str(allOptions['id']))
      # print("car id je")
      # print(type(carId))



      
      

      # car_url = "http://23.88.98.237:8069/api/fleet.vehicle/"+carId

      # header_data = {'Access-Token' : str(access_token)}

      # response = requests.get(car_url, headers=header_data)

      # response_data_car = json.loads(response.text)

      # print(response.text)   
      
      #print(vehicle_id)
      # vehicle_brand = str(response_data_car['brand_id']['name'])
      # vehicle_name = str(response_data_car['model_id']['name'])

      # transmission = str(response_data_car['transmission'])
      # category = str(response_data_car['category_id']['name'])
      # fuel_type = str(response_data_car['results'][0]['vehicle_id']['fuel_type'])
      # seats = str(response_data_car['results'][0]['vehicle_id']['seats'])
      # doors = str(response_data_car['results'][0]['vehicle_id']['doors'])
      # # vehicle_plate = str(response_data['results'][0]['vehicle_id']['license_plate'])
      # image = str(response_data_car['results'][0]['vehicle_id']['image_128'])

      


      toAdd = {
         'location_from_id' : location_from,
         'location_to_id' : location_to,
         'location_from': location_from_name,
         'date_from': date_from,
         'location_to': location_to_name,
         'date_to': date_to,
         'carId' : carId,
         # 'brand' : vehicle_brand,
         'name' : carName,
         #'transmission': transmission,
         # 'category': category,
         'price': 26,
         'tenant': tenant,
         'currentOptions': currentOptionsItems
      }

      years_range = list(range(1943, 2013))
      months_range = list(range(1, 13))
      days_range = list(range(1, 32))

      




      # return render_template('/rezervacija/rezervacijeKorisnik.html',days_range=days_range, months_range=months_range, years_range=years_range,carDetails = toAdd, allLocations = allLocations, allOptions = allOptions)






      ##################################
      # STAMPANJE POTVRDE O VRACENOM KLJUCU
      ##################################


      # response_pdf = requests.get(
      #    'http://23.88.98.237:8069/api/report/get_pdf',
      #    headers = {
      #       'Content-Type': 'text/html; charset=utf-8',
      #       'Access-Token': access_token
      #    },
      #    data = json.dumps({
      #       "report_name":  "fleet_rent.key_return_report_pdf",
      #       "ids": [169],
      #    }),
      # )

      # pdf_file = str(response_pdf.text[1: len(response_pdf.text)-1])
 


      # stripped = pdf_file.replace('\\n', '')
      # bytes = b64decode(stripped, validate=True)

      # f = open("temp.pdf", "wb")
      # f.write(bytes)
      # f.close()
      # # os.system("lp temp.pdf")
     

      ##################################





      position = 3
      link_ugovora = ugovor_link




      # return ("dasdsa")
      return render_template('/preuzimanje/preuzimanjeDodatneUsluge.html',contract_id = contract_id, days_range=days_range, months_range=months_range, years_range=years_range,carDetails = toAdd, allLocations = allLocations, allOptions = allOptions)

      return render_template('odoo.html', contract_id = contract_id, position = position, iframe= link_ugovora)


   except:
      print("varibale not a number")




@app.route('/preuzimanjeUgovorEdit/', methods = ['GET', 'POST'])
def preuzimanjeUgovorEdit():


   ugovor_link = request.args.get('ugovor_link')


   

   first_part = ugovor_link.split('?')[0]

   Segments = first_part.rpartition('/')
   contract_id = Segments[2]
   


   try:
 


      response = requests.get(
               "http://23.88.98.237:8069/api/auth/get_tokens",
               params={"username": "odoo@irvas.rs", "password": "irvasadm"}
         )

      response_data = json.loads(response.text)
      access_token = response_data['access_token']

      header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

   
      url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id

      response = requests.get(url, headers=header_data)

      response_data = json.loads(response.text)

      print(contract_id)
      print("ugovor")
      print(response.text)
      print("ugovor kraj")














      location_from = response_data['rent_from']['id']
      location_from_name = response_data['rent_from']['name']
      date_from = response_data['date_start']
      location_to = response_data['return_location']['id']
      location_to_name = response_data['return_location']['name']
      date_to = response_data['date_end']
      carId = response_data['vehicle_id']['id']
      carName = response_data['vehicle_id']['name']
      tenant = response_data['tenant_id']['name']
      currentOptions = response_data['option_ids']['option']

      web_car_id = response_data['vehicle_id']['web_car_id']
      web_price_group_id = response_data['vehicle_id']['web_price_group_id']

      



      # RENT PRICE


      dt_from = datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
      from_timestamp =(int(dt_from.timestamp()))


      dt_to = datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
      to_timestamp =(int(dt_to.timestamp()))

      # print("from_timestamp")
      # print(from_timestamp)

      
      # print("to_timestamp")
      # print(to_timestamp)


      day_num = math.ceil((to_timestamp - from_timestamp)/86400)


      total_price = 0

      for x in range(day_num):
         # print("--------------------")
         # print(x)
         current_day = from_timestamp + x*86400
         # print("Current day")
         # print(current_day)

         # print("Duration: ")
         # print(to_timestamp - from_timestamp)

         dt_object = datetime.fromtimestamp(current_day)
         dt_string = dt_object.strftime("%a").lower()
         # print(dt_string)
         key_day = "daily_rate_"+dt_string



         # print("key_day")
         # print(key_day)
         # print("current_day")
         # print(current_day)
         # print("from_timestamp")
         # print(from_timestamp)
         # print("to_timestamp")
         # print(to_timestamp)
         # print("web_price_group_id")
         # print(web_price_group_id)

         headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
         URL = "https://cheapcarhire.rent/wp-json/my/price/getprice?selected_day="+str(key_day)+"&current_day="+str(current_day)+"&date_from="+str(from_timestamp)+"&date_to="+str(to_timestamp)+"&from=1&to=522&vehicle_category_id="+str(web_price_group_id)
         # print(URL)
         prices = requests.get(url = URL, headers = headers, data='')
         json_object = json.loads(prices.text)
         # print(prices.text)
         day_price = json_object[0][key_day]


         default_discount = 0

         if day_num == 1 or day_num == 2:
            print("Popust 20")
            default_discount = 20;
         elif day_num >= 3 and day_num <= 7:
            print("Popust 45")
            default_discount = 45;
         elif day_num >= 8:
            print("Popust 50")
            default_discount = 50;


         if not json_object[0]['discount_percentage']:
            print("popust 1")
            current_discount = default_discount
         else:
            print("popust 2")
            current_discount = json_object[0]['discount_percentage']

         dayprice_with_discount = float(day_price) * (100 - float(current_discount))/100

         total_price = total_price + float(dayprice_with_discount)
         price_per_day = float(dayprice_with_discount)



         


      #    print("discount je: ")
      #    print(current_discount)
      # print("price_per_day: ")
      # print(price_per_day)
      # print("****************")
      

      # DEPOZIT
      headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
      URL = "https://cheapcarhire.rent/wp-json/my/price/cardeposit?car_id="+str(web_car_id)
      deposit_data = requests.get(url = URL, headers = headers, data='')
      deposit = float(json.loads(deposit_data.text)[0]['fixed_rental_deposit'])
      

      print(type(currentOptions))
      print(currentOptions)

      if currentOptions:
         if isinstance(currentOptions, int):
            currentOptionsItems = []
            currentOptionsItems.append(currentOptions)
         else:
            currentOptionsItems = currentOptions
      else:
         currentOptionsItems = []



      print("Izabrane opcije")
      print(currentOptionsItems)


      deposit_required = True
      pay_deposit = True

      pay_payment = True

      if 13 in currentOptionsItems:
         deposit_required = False
         print("ima ga 13 u nizu")


      is_payment_received = response_data['is_payment_received']
      is_deposid_received = response_data['is_deposid_received']


      if deposit_required:
         if is_deposid_received:
            pay_deposit = False
      else: 
         pay_deposit = False

      if is_payment_received:
            pay_payment = False
      

      if pay_deposit:
         print("Plati depozit")
      else:
         print("Plati depozit NE TREBA")
      
      if pay_payment:
         print("Plati payment")
      else:
         print("Plati payment NE TREBA")


      # print(location_from)
      # print(date_from)
      # print(location_to)
      # print(date_to)
      # print(carId)

      
      

      # url = "http://23.88.98.237:8069/api/stock.location/"+location_from

      # header_data = {'Access-Token' : str(access_token)}

      # response_locationFrom = requests.get(url, headers=header_data)
      # print(response_locationFrom.text)
    
      # response_data_locationFrom = json.loads(response_locationFrom.text)


      # location_from_name = response_data_locationFrom['name']
      # print(location_from_name)
      

      # url = "http://23.88.98.237:8069/api/stock.location/"+location_to
      # response_locationTo = requests.get(url, headers=header_data)

      # response_data_locationTo = json.loads(response_locationTo.text)
      # location_to_name = response_data_locationTo['name']


      

      
      url = "http://23.88.98.237:8069/api/stock.location"

      header_data = {'Access-Token' : str(access_token)}

      response = requests.get(url, headers=header_data)

      response_data = json.loads(response.text)


      # print("stock locations")
      # print(response.text)
      # print("stock locations kraj")

      # print(response.text)

      allLocations=[]


      if(response_data['count'] != 0):

         for key in response_data['results']:
            
            allLocations.append(key)
      


      url = "http://23.88.98.237:8069/api/product.product"

      header_data = {'Access-Token' : str(access_token)}

      response = requests.get(url, headers=header_data)

      response_data = json.loads(response.text)
      # print("products")
      # print(response.text)
      # print("products kraj")
      

      allOptions=[]

      
      if(response_data['count'] != 0):

         for key in response_data['results']:
            # print(key)
            product_id = str(key['id'])

            # print("product id")
            # print(product_id)
            # print(key['name'])

            url = "http://23.88.98.237:8069/api/product.product/"+product_id

            header_data = {'Access-Token' : str(access_token)}

            response = requests.get(url, headers=header_data)

            response_data = json.loads(response.text)

            id = response_data['id']
            name = response_data['name']
            price = response_data['lst_price']

            add_with_pricce = {
               'id' : id,
               'name' : name,
               'price' : price
            }

            # print(key)
            if response_data['id'] == 13 or response_data['id'] == 15:
               allOptions.append(add_with_pricce)
      # print(allOptions)
      # print("Id je: "+str(allOptions['id']))
      # print("car id je")
      # print(type(carId))



      
      

      # car_url = "http://23.88.98.237:8069/api/fleet.vehicle/"+carId

      # header_data = {'Access-Token' : str(access_token)}

      # response = requests.get(car_url, headers=header_data)

      # response_data_car = json.loads(response.text)

      # print(response.text)   
      
      #print(vehicle_id)
      # vehicle_brand = str(response_data_car['brand_id']['name'])
      # vehicle_name = str(response_data_car['model_id']['name'])

      # transmission = str(response_data_car['transmission'])
      # category = str(response_data_car['category_id']['name'])
      # fuel_type = str(response_data_car['results'][0]['vehicle_id']['fuel_type'])
      # seats = str(response_data_car['results'][0]['vehicle_id']['seats'])
      # doors = str(response_data_car['results'][0]['vehicle_id']['doors'])
      # # vehicle_plate = str(response_data['results'][0]['vehicle_id']['license_plate'])
      # image = str(response_data_car['results'][0]['vehicle_id']['image_128'])

      


      toAdd = {
         'location_from_id' : location_from,
         'location_to_id' : location_to,
         'location_from': location_from_name,
         'date_from': date_from,
         'location_to': location_to_name,
         'date_to': date_to,
         'carId' : carId,
         # 'brand' : vehicle_brand,
         'name' : carName,
         #'transmission': transmission,
         # 'category': category,
         'price': 26,
         'tenant': tenant,
         'currentOptions': currentOptionsItems
      }

      years_range = list(range(1943, 2013))
      months_range = list(range(1, 13))
      days_range = list(range(1, 32))

      




      # return render_template('/rezervacija/rezervacijeKorisnik.html',days_range=days_range, months_range=months_range, years_range=years_range,carDetails = toAdd, allLocations = allLocations, allOptions = allOptions)






      ##################################
      # STAMPANJE POTVRDE O VRACENOM KLJUCU
      ##################################


      # response_pdf = requests.get(
      #    'http://23.88.98.237:8069/api/report/get_pdf',
      #    headers = {
      #       'Content-Type': 'text/html; charset=utf-8',
      #       'Access-Token': access_token
      #    },
      #    data = json.dumps({
      #       "report_name":  "fleet_rent.key_return_report_pdf",
      #       "ids": [169],
      #    }),
      # )

      # pdf_file = str(response_pdf.text[1: len(response_pdf.text)-1])
 


      # stripped = pdf_file.replace('\\n', '')
      # bytes = b64decode(stripped, validate=True)

      # f = open("temp.pdf", "wb")
      # f.write(bytes)
      # f.close()
      # # os.system("lp temp.pdf")
     

      ##################################





      position = 3
      link_ugovora = ugovor_link

      
      


      # return ("dasdsa")
      return render_template('/preuzimanje/preuzimanjeDodatneUsluge.html',total_price=total_price, price_per_day=price_per_day, day_num=day_num, deposit=deposit, contract_id = contract_id, days_range=days_range, months_range=months_range, years_range=years_range,carDetails = toAdd, allLocations = allLocations, allOptions = allOptions)

      return render_template('odoo.html', contract_id = contract_id, position = position, iframe= link_ugovora)


   except:
      print("varibale not a number")





@app.route('/submit_form_preuzimanje',  methods=['GET', 'POST'])
def submit_form_preuzimanje():
   payment_succes = request.args.get('payment_succes')
   payment_type = request.args.get('payment_type')
   

   added_options = request.args.getlist('options')


   listToInt = list(map(int, added_options))
  


   print("Stilkirane opcije")
   print(listToInt)


   # update "options"


   contract_id = request.args.get('contract_id')

   print("Id ugovora: ")
   print(contract_id)



   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
      )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']

   header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}


   url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)

   # print(contract_id)
   print("ugovor")
   print(response.text)
   print("ugovor kraj")




   print("Opcije iz baze: ")
   currentOptions = response_data['option_ids']['option']
   print(currentOptions)
   
   if currentOptions:
      if isinstance(currentOptions, int):
         currentOptionsItems = []
         currentOptionsItems.append(currentOptions)
      else:
         currentOptionsItems = currentOptions
   else:
      currentOptionsItems = []


   print("Opcije iz baze NIZ: ")
   print(currentOptionsItems)



   # final_options = currentOptionsItems + listToInt
   final_options = listToInt


   print("finalne opcije")
   print(final_options)


   

   deposit_required = True
   pay_deposit = True

   pay_payment = True

   if 13 in currentOptionsItems:
      deposit_required = False
      print("ima ga 13 u nizu")


   is_payment_received = response_data['is_payment_received']
   is_deposid_received = response_data['is_deposid_received']


   if deposit_required:
      if is_deposid_received:
         pay_deposit = False
   else: 
      pay_deposit = False

   if is_payment_received:
         pay_payment = False
   

   if pay_deposit:
      print("Plati depozit")
   else:
      print("Plati depozit NE TREBA")
   
   if pay_payment:
      print("Plati payment")
   else:
      print("Plati payment NE TREBA")




   # update options


   
   
   

   header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}
   url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id
   # data_update = json.dumps({'option': final_options,})
   # data_insert_final = json.dumps(data_insert)



   option_line_ids = []

   for selected_option in final_options:
      # print("ID opcije je"+selected_option)

      response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

      response_data = json.loads(response.text)
      access_token = response_data['access_token']


      url = "http://23.88.98.237:8069/api/product.product/"+str(selected_option)

      header_data = {'Access-Token' : str(access_token)}

      response = requests.get(url, headers=header_data)

      response_data = json.loads(response.text)


      print(response.text)


      price = str(response_data['list_price'])
   
      dic_string = "{'option':"+str(selected_option)+", 'price':"+price+", 'quantity':1}"


      option_line_ids.append(dict(ast.literal_eval(dic_string)))
      



   data_insert={
      "option_ids" : option_line_ids,
      }
  
   data_insert_final = json.dumps(data_insert)



   my_dict = ast.literal_eval(data_insert_final)

   # print(type(my_dict))
   # print(type(datetest))

   




   data_update = json.dumps(my_dict)


   # header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}
   header_data = {'Access-Token' : str(access_token)}
   url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id
   response = requests.put(url, data=data_update, headers=header_data)


   # print("Update data")
   # print(dic_string)
   # print("-----------------------")
   # print(data_insert)
   # print("------------------------")
   # print("json dumps")
   # print(data_insert_final)
   # print(contract_id)
   # print(data_update)
   # print("response")
   # print(response)
   # print("response end")


   return redirect(url_for('paymentPage', contract_id=contract_id, payment_succes = payment_succes, payment_type = payment_type))


   return "1"
   
   
   options = request.args.getlist('options')


   

   deposit_amt = 0

   for el in options:
      if el == "13":
            deposit_amt = 0
      else:
         deposit_amt = 600
   
   if not options:
      deposit_amt = 600

   # print("&&&&&&&&")
   # print(deposit_amt)
   # print("&&&&&&&&")
   carid = request.args.get('carid')
   grand_value = request.args.get('all_days_price_input')


   location_from_id = request.args.get('location_from_id')
   location_to_id = request.args.get('location_to_id')

   location = request.args.get('location')
   return_date = request.args.get('date_to')
   start_date_input = request.args.get('start_date_input')
   # casco_checkbox = request.args.get('casco_checkbox')
   # tyres_checbox = request.args.get('tyres_checbox')

   # if(casco_checkbox == 'on'):
   #     casco = "1"
   #     deposit_amt = 0
   # else :
   #     casco = "0"
   #     deposit_amt = 600
   

   # if(tyres_checbox == 'on'):
   #     tyres = "1"
   # else :
   #     tyres = "0"





   
   # print("deposit amount je: ")
   # print(deposit_amt)


   # USER DETAILS

   first_name = request.args.get('first_name')
   last_name = request.args.get('last_name')
   year = request.args.get('year')
   month = request.args.get('month')
   day = request.args.get('day')
   address = request.args.get('address')
   city = request.args.get('city')
   country = request.args.get('country')
   phone = request.args.get('phone')
   email = request.args.get('email')
   comments = request.args.get('comments')
   days_num_var = request.args.get('days_num_var')
   birthday = year+'-'+month+'-'+day


   rent_details = {
       'carId': carid,
       'grand_value' : grand_value,
       # 'location': location_to_id,
       'start_date' : start_date_input,
       'rent_from' : location_from_id,
       'return_location' : location_to_id,
       'return_date': return_date,
      #  'casco' : casco,
      #  'tyres' : tyres,
       'options' : options,
       'days_num_var' : days_num_var,
       'total_rent' : grand_value,
       'deposit_amt' : deposit_amt
   }


   # print(rent_details)


   user_details = {
       'first_name': first_name,
       'last_name': last_name,
       'birthday': birthday,
       'address' : address,
       'city' : city,
       'country' : country,
       'phone' : phone,
       'email' : email,
       'comments' : comments
   }

   # print(user_details)

   contract_id = create_contract(rent_details, user_details)


   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']


   header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

   url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id+"/change_odometer"
   
   
   response_odo = requests.put(url, headers=header_data)

   response_data_od = json.loads(response_odo.text)
   print("**********************")
   print(response_data_od)
   print("**********************")
   # contract_id = str(response_data['results'][0]['id'])


   return render_template('/rezervacija/submit_form_confirm.html', contract_id = contract_id), {"Refresh": "3; url=/paymentPage?contract_id="+contract_id}  





@app.route('/paymentPagePreuzimanje', methods = ['GET', 'POST'])
def paymentPagePreuzimanje():

   contract_id = request.args.get('contract_id')
   payment_succes = request.args.get('payment_succes')
   payment_type = request.args.get('payment_type')
   # print(payment_succes)
   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']


   header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

   url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id
   
   
   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)


   print(url)
   print(response.text)
   print("******************")


   rent_amt = response_data['rent_amt']
   rent_currency = response_data['currency_id']
   deposit_amt = response_data['deposit_amt']
   is_payment_received = response_data['is_payment_received']
   is_deposid_received = response_data['is_deposid_received']
   deposit_received = response_data['deposit_received']


   options = response_data['option_ids']['option']
   print(options)
   
   casco_id = 13

   is_casco = 0
   if options:
      if isinstance(options, int):
         if options == casco_id:
            is_casco = 1
      else:
         if casco_id in options:
            is_casco = 1
   
   print("sa casco?")
   print(is_casco)

   # print(type(options))

   # print(len(options))

   # if 13 in options:
   #    print("ima")
   # else:
   #    print("nema")

   

   return render_template('/rezervacija/paymentPage.html', is_casco = is_casco, payment_type = payment_type, payment_succes = payment_succes, contract_id = contract_id, rent_amt = rent_amt, rent_currency = rent_currency, deposit_amt = deposit_amt, deposit_received = deposit_received, is_payment_received = is_payment_received, is_deposid_received = is_deposid_received)
  
   




@app.route('/preuzimanjeUgovorStampa')
def preuzimanjeUgovorStampa():
   return render_template('preuzimanjeUgovorStampa.html')








###########################################################

##############    PREUZIMANJE VOZILA KRAJ   ###############

###########################################################











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

   # print(response.text)


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

   
   


   # print("Brand: "+brand)
   # print("model: "+model)
   # print("gearbox: "+gearbox)
   # print("fuel_type: "+fuel_type)
   # print("category: "+category)
   # print("license_plate: "+license_plate)
   # print("seats: "+str(seats))
   # print("model_year: "+str(model_year))
   # print("doors: "+str(doors))
   # print("horsepower: "+str(horsepower))
   # print("power: "+str(power))

   # vehicle_data = {
   #             'name' : vehicle_name,
   #             'plate' : vehicle_plate,
   #          }




   return render_template('/rezervacija/vozilo.html', brand=brand, model=model, gearbox=gearbox, fuel_type=fuel_type, category=category, license_plate=license_plate, seats=seats, model_year=model_year, doors=doors, horsepower=horsepower, power=power, image_128=image_128)






 

@app.route('/go_contract', methods = ['GET', 'POST'])
def go_contract():

   contract_id = request.args.get('contract_id')


   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']


   header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

   url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id
   
   
   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)


   print("***go_contract********")
   print(response.text)
   print("******************")

   base_url = "https://selfcar.naisrobotics.com"
   access_url = response_data["access_url"]
   token = response_data["access_token"]
   
   


   



   # print(base_url)
   # print(access_url)
   # print(token)
   # final_url = base_url + access_url + "?access_token=" + token
   # print(final_url)
   # contract_id = str(response_data['results'][0]['id'])




   # print(contract_id)
   return render_template('/rezervacija/takekey.html'), {"Refresh": "3; url=/paymentPage?contract_id="+contract_id}








@app.route('/contract_test', methods = ['GET', 'POST'])
def contract_test():
   data_insert={
      "name": "test/RN01834/252 name",
      "tenant_id" : 304,
      "date_start" : "2023-11-14 15:33:00",
      "date_end" : "2023-11-16 15:33:00",
      "reservation_code" : "Rtest01",
      "notes" : "notes",
      "rent_from" : '17',
      "return_location" : '17',
      "web_car_request" : "",
      "total_rent" : '78',
      "state" : "open",
      "rent_amt" : "78",
      "deposit_amt": 600,
      "option_ids" : [],
      "currency_id" : 1,
      "vehicle_id" : '85',
      "duration" : '2',
      "odometer_unit" : "kilometers",
      'rent_type_id' : 1
      }

   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']
   #return(access_token)
   header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}



   data_insert_final = json.dumps(data_insert)
   url = "http://23.88.98.237:8069/api/fleet.rent"
   response = requests.post(url, data=data_insert_final, headers=header_data)

   return "3"


@app.route('/create_contract', methods = ['GET', 'POST'])
def create_contract(rent_details, user_details):



   # print(rent_details['carId'])
   # print(user_details['first_name'])

    
   user_name = user_details['first_name']
   user_email = user_details['email']
   phone = user_details['phone']
   street = user_details['address']
   city = user_details['city']
   country_id = 1




   


  
  



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
   

   url = "http://23.88.98.237:8069/api/res.users?filters=[('email','=','"+user_email+"')]"

   # CHECK EXISTING USER



   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)

   if(response_data['count'] > 0):
       # print("User postoji")
       user_id = response_data['results'][0]['id']
 
   else:
       # print("User NE postoji")


       # CREATE USER

       data_insert={
         "name" : user_name,
         "email" : user_email,
         "login" : user_email,
         "phone" : phone,
         "is_company" : "0",
         "street" : street,
         "city" : city,
         "country_id" : country_id,
         "is_tenant" : True
      }


       data_insert_final = json.dumps(data_insert)
       url = "http://23.88.98.237:8069/api/res.users"
       response = requests.post(url, data=data_insert_final, headers=header_data)


      # GET USER ID
       url = "http://23.88.98.237:8069/api/res.users?filters=[('email','=','"+user_email+"')]"
       response = requests.get(url, headers=header_data)

       response_data = json.loads(response.text)
       user_id = response_data['results'][0]['id']
   
   # print("*************************")
   # print(user_id)
   # print("*************************")

   


   date_object = datetime.strptime(rent_details['start_date'], '%B %d, %Y %H:%M')
   date_start_value =date_object.strftime('%Y-%m-%d %H:%M:%S')

   date_object = datetime.strptime(rent_details['return_date'], '%Y/%m/%d %H:%M')
   date_end_value = date_object.strftime('%Y-%m-%d %H:%M:%S')

   



   # rent_details = {
   #     'carId': carid,
   #     'location': location,
   #     'return_date': return_date,
   #     'start_date' : start_date_input,
   #     'casco' : casco,
   #     'tyres' : tyres
   # }

   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
      data = json.load(jsonFile)


   rentomat_id = data['rentomat_id']
   next_contract_id = int(data['last_contract_id'])+1


   # UPDATE JSON

  

   data["last_contract_id"] = next_contract_id

   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "w") as jsonFile:
      json.dump(data, jsonFile)



   date_start = date_start_value
   date_end = date_end_value
   reservation_code = rentomat_id + "_" + str(next_contract_id)
   contract_name = "RNT/"+rentomat_id + "/" + str(next_contract_id)
   notes =""
   rent_from = rent_details['rent_from']
   return_location = rent_details['return_location']
   web_car_request = ""
   total_rent = rent_details['grand_value']
   rent_amt = rent_details['grand_value']
   option_ids = "{'option' : 17, 'price' : 15}"
   currency_id = 1
   carid = rent_details['carId']
   days_num_var = rent_details['days_num_var']
   deposit_amt = rent_details['deposit_amt']

   options = rent_details['options']

   # print("*****************")
   # print(reservation_code)
   # print("*****************")
   # date_start = "2023-02-05 13:00:00"
   # date_end = "2023-02-07 13:00:00"
   # reservation_code = "Rtest01"
   # notes =""
   # rent_from = 1
   # return_location = 1
   # web_car_request = ""
   # total_rent = "20"
   # rent_amt = "20"
   # option_ids = []
   # currency_id = 1

   # CREATE CONTRACT


   option_lines = []

   option_line_ids = []
   for selected_option in options:
      # print("ID opcije je"+selected_option)

      response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

      response_data = json.loads(response.text)
      access_token = response_data['access_token']


      url = "http://23.88.98.237:8069/api/product.product/"+selected_option

      header_data = {'Access-Token' : str(access_token)}

      response = requests.get(url, headers=header_data)

      response_data = json.loads(response.text)

      price = str(response_data['list_price'])

      dic_string = "{'option':"+selected_option+", 'price':"+price+", 'quantity':1, 'total_price': "+price+"}"


      option_line_ids.append(dict(ast.literal_eval(dic_string)))

  


   data_insert={
      "name": contract_name,
      "tenant_id" : user_id, ####
      "date_start" : date_start, ####
      "date_end" : date_end, ####
      "reservation_code" : reservation_code, ####
      "notes" : notes, ####
      "rent_from" : rent_from,
      "return_location" : return_location,
      "web_car_request" : web_car_request,
      "total_rent" : total_rent,
      "state" : "open", ####
      "rent_amt" : rent_amt, ####
      "deposit_amt": deposit_amt,
      "option_ids" : option_line_ids, ####
      "currency_id" : currency_id,
      "vehicle_id" : carid,
      "duration" : days_num_var,
      "odometer_unit" : "kilometers",
      #"odometer_unit" : "kilometers",
      # "odometer": {
      #    "vehicle_id" : carid,
      #    "value" : "5555"
      # },
      }


   data_insert_final = json.dumps(data_insert)
   url = "http://23.88.98.237:8069/api/fleet.rent"
   response = requests.post(url, data=data_insert_final, headers=header_data)

   # print("****************")
   # print(response.text)
   # print("****************")


   

   # data_odometer = {
   #     'vehicle_id' : carid,
   #     'value' : "526",
   #     'unit' : "kilometers"
   # }

   # data_insert_final_odometer = json.dumps(data_odometer)
   # url = "http://23.88.98.237:8069/api/fleet.vehicle.odometer"
   # response = requests.post(url, data=data_insert_final_odometer, headers=header_data)




   



   url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('reservation_code', '=', '"+reservation_code+"')]"

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)


   contract_id = str(response_data['results'][0]['id'])



   # create schedule payment 

   rent_chedule = {
      'start_date' : date_start,
      'pen_amt' : '6',
      'cheque_detail' : 'detalji ceka',
      'paid' : True,
      'move_check' : True,
      'state' : 'open',
      'note' : 'notescici',
      'fleet_rent_id' : contract_id,
      'vehicle_id' : carid,
      'amount' : "12"
   }

   data_insert_final_shedule = json.dumps(rent_chedule)
   url = "http://23.88.98.237:8069/api/tenancy.rent.schedule"
   response = requests.post(url, data=data_insert_final_shedule, headers=header_data)

   # print(response.text)


   return contract_id

   
   # data_insert_final2 = json.dumps(data_insert2)
   # url = "http://23.88.98.237:8069/api/fleet.rent"
   # response = requests.post(url, data=data_insert_final2, headers=header_data)


   # return redirect(url_for("get_redirection"))





   url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('reservation_code', '=', '"+reservation_code+"')]"

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)
   print(response.text)

   url_prefix = "https://selfcar.naisrobotics.com/"
   link = response_data['results'][0]['access_url']
   token = response_data['results'][0]['access_token']

   final_url = url_prefix+link+token

   print(response_data)
   print(token)
   print(link)

   print(final_url)



   return reservation_code
@app.route('/get_redirection', methods = ['GET', 'POST'])
def get_redirection():
   # print("da")
   url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('reservation_code', '=', 'RN01834_8')]"

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)
   # print(response.text)

   url_prefix = "https://selfcar.naisrobotics.com/"
   link = response_data['results'][0]['access_url']
   token = response_data['results'][0]['access_token']

   final_url = url_prefix+link+token

   # print(response_data)
   # print(token)
   # print(link)

   # print(final_url)
    









@app.route('/stampanje_test', methods = ['GET', 'POST', 'PUT'])
def stampanje_test():
   

   contract_id = 433

   response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

   response_data = json.loads(response.text)
   access_token = response_data['access_token']
   print("Token: "+access_token)

   response_pdf = requests.get(
      'http://23.88.98.237:8069/api/report/get_pdf',
      headers = {
         'Content-Type': 'text/html; charset=utf-8',
         'Access-Token': access_token
      },
      data = json.dumps({
         "report_name":  "fleet_rent.key_return_report_pdf",
         "ids": [contract_id],
      }),
   )

   print("-----------")
   print(response_pdf.text)
   print("-----------")
   pdf_file = str(response_pdf.text[1: len(response_pdf.text)-1])



   stripped = pdf_file.replace('\\n', '')
   bytes = b64decode(stripped, validate=True)

   f = open("temp.pdf", "wb")
   f.write(bytes)
   f.close()
   os.system("lp temp.pdf")

   return "odstampano"




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

   params={}

   response = requests.get("http://192.168.1.113", params)

   response_data = json.loads(response.text)

   return(response_data)

   # response = requests.get(
   #          "http://23.88.98.237:8069/api/auth/get_tokens",
   #          params={"username": "odoo@irvas.rs", "password": "irvasadm"}
   #    )

   # response_data = json.loads(response.text)
   # access_token = response_data['access_token']



   # url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('reservation_code', '=', 'RN01834_8')]"

   # header_data = {'Access-Token' : str(access_token)}

   # response = requests.get(url, headers=header_data)

   # response_data = json.loads(response.text)
   # print(response.text)


   # redirect_baseUrl = 'https://www.google.com' 

   # return redirect(redirect_baseUrl)



   # response = requests.get(
   #          "http://23.88.98.237:8069/api/auth/get_tokens",
   #          params={"username": "odoo@irvas.rs", "password": "irvasadm"}
   #    )

   # response_data = json.loads(response.text)
   # access_token = response_data['access_token']
   # #return(access_token)

   # print(access_token)


   # params_email={"pecooou@yahoo.com"}

   # url = "http://23.88.98.237:8069/api/mail.compose.message"

   # header_data = {'Access-Token' : str(access_token)}

   # response = requests.post(url, headers=header_data, params_email)

   # response_data = json.loads(response.text)

   # print(response_data)










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













   # user_email = "pecooou"
   # user_email = "pecooou1@yahoo.com"
   # phone = "123456789"
   # street = "Ulica i broj"
   # city = "Nis"
   # country_id = 1








   # response = requests.get(
   #          "http://23.88.98.237:8069/api/auth/get_tokens",
   #          params={"username": "odoo@irvas.rs", "password": "irvasadm"}
   #     )

   # response_data = json.loads(response.text)
   # access_token = response_data['access_token']
   # #return(access_token)
   # header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}
   

   # # url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('id','=','47'), ('state','=','open')]"
   # # data_update = json.dumps({'state': 'running',})
   

   # url = "http://23.88.98.237:8069/api/res.users?filters=[('email','=','"+user_email+"')]"

   # # CHECK EXISTING USER



   # response = requests.get(url, headers=header_data)

   # response_data = json.loads(response.text)

   # if(response_data['count'] > 0):
   #     print("User postoji")
   #     user_id = response_data['results'][0]['id']
 
   # else:
   #     print("User NE postoji")


   #     # CREATE USER

   #     data_insert={
   #       "name" : "Pecooou1",
   #       "email" : user_email,
   #       "login" : user_email,
   #       "phone" : phone,
   #       "is_company" : "0",
   #       "street" : street,
   #       "city" : city,
   #       "country_id" : country_id,
   #       "is_tenant" : True
   #    }


   #     data_insert_final = json.dumps(data_insert)
   #     url = "http://23.88.98.237:8069/api/res.users"
   #     response = requests.post(url, data=data_insert_final, headers=header_data)


   #    # GET USER ID
   #     url = "http://23.88.98.237:8069/api/res.users?filters=[('email','=','"+user_email+"')]"
   #     response = requests.get(url, headers=header_data)

   #     response_data = json.loads(response.text)
   #     user_id = response_data['results'][0]['id']
   
   # print("*************************")
   # print(user_id)
   # print("*************************")


   # date_start = "2023-02-05 13:00:00"
   # date_end = "2023-02-07 13:00:00"
   # reservation_code = "R0192837465"
   # notes =""
   # rent_from = 1
   # return_location = 1
   # web_car_request = ""
   # total_rent = "20"
   # rent_amt = "20"
   # option_ids = []
   # currency_id = 1

   # # CREATE CONTRACT

   # data_insert={
   #    "tenant_id" : user_id, ####
   #    "date_start" : date_start, ####
   #    "date_end" : date_end, ####
   #    "reservation_code" : reservation_code, ####
   #    "notes" : notes, ####
   #    "rent_from" : rent_from,
   #    "return_location" : return_location,
   #    "web_car_request" : web_car_request,
   #    "total_rent" : total_rent,
   #    "state" : "running", ####
   #    "rent_amt" : rent_amt, ####
   #    "option_ids" : option_ids, ####
   #    "currency_id" : currency_id ####
   # }


   # data_insert_final = json.dumps(data_insert)
   # url = "http://23.88.98.237:8069/api/fleet.rent"
   # response = requests.post(url, data=data_insert_final, headers=header_data)

   # print(response.text)

   return render_template('/vracanje/vracanjeHvala.html')
   # ADD USER

   


   

   
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

   





###################################

######      PREUZIMANJE      ######

###################################





















@app.route('/transaction_success', methods = ['GET', 'POST', 'PUT'])
def transaction_success():


   transaction_data = request.args.get('transaction_data')


   print(transaction_data)

   return render_template('/preuzimanje/transaction_success.html', transaction_data = transaction_data)





def xor_sum(message):
    lrc = 0

    for i in range(0, len(message)-1, 2):
        
        b = message[i:i+2]
        lrc ^= int(b, 16)

    return hex(lrc)[2:4]







@app.route('/pos_client', methods = ['GET', 'POST', 'PUT'])
def pos_client():
    

   send_dict = { "identifier" : "3030",
      "terminalID" : "3030",
      "sourceID" : "3030",
      "sequentialNumber" : "30303030",
      "transactionType" : "3031",
      "printerFlag" : "30",
      "cashierID" : "3030",
      "transactionNumber" : "",
      "fieldSeparator1" : "1C",
      "transactionAmount1" : "32",
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


   message_data = ""


   for key in send_dict:
      message_data = str(message_data) + str(send_dict[key])

   message_data = message_data + str(ETX)
   ack_message_data_tmp = ACK + ETX
   nack_message_data_tmp = NACK + ETX

   lrc = xor_sum(message_data)
   # print("*******")

   # print(lrc)
   # print("*******")
   # lrc_ack = xor_sum(ack_message_data_tmp)
   # lrc_nack = xor_sum(nack_message_data_tmp)


   message_data = STX+STX+message_data+str(lrc)




   S_TCP_IP = '192.168.1.101'  
   S_TCP_PORT = 3000



   TCP_IP = '192.168.1.113'    
   TCP_PORT = 3000   

   sock_payten = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   status = sock_payten.connect((TCP_IP, TCP_PORT))




   dobar_format = bytearray.fromhex(message_data).decode()


   i = 1

   try:
      
      
      for i in range(1):



         sent = sock_payten.sendto(bytes(dobar_format, encoding='iso-8859-2'),(TCP_IP,TCP_PORT))

         data = sock_payten.recv(1024)
     

         if data.hex() == ACK:
               data = sock_payten.recv(1024)
               sent = sock_payten.sendto(bytes(ACK, encoding='iso-8859-2'),(TCP_IP,TCP_PORT))
               hold = True
               while hold == True:
               
                  data = sock_payten.recv(1024)
                  time.sleep(3)

                  message_identifier = data.hex()
                  # print(message_identifier[2:6])
                  if message_identifier[2:6] == "3130":   # kod 10
                     hold = False
               
               sent = sock_payten.sendto(bytes(ACK, encoding='iso-8859-2'),(TCP_IP,TCP_PORT))
               # print("Transakcija uspesno realizovana")
               return "Transakcija uspesno realizovana"
               
         


   
   except:
      return "Ode na except"






def update_contract_running(contract_id):
   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']


   header_data = {'Access-Token' : str(access_token)}

   url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id
   data_update = {'state': 'running'}
   requests.put(url, data=data_update, headers=header_data)





def get_rfid(contract_id):
   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
       )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']

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
 
@app.route('/EMPTY', methods=['GET'])
def empty():
   
   
   pozicija_kljuca = request.args.get('pos')
   read_rentomat('EMPTY', pozicija_kljuca)
   with open('/home/pi/VSCProjects/selfrentacar/flask_rentomat/komanda.txt', 'w') as f:
            f.write("EMPTY")      
   return "u"

if __name__ == '__main__':
   app.run()

    
@app.route('/FILL')
def fill():

    rfid = request.args.get('pos')
    

