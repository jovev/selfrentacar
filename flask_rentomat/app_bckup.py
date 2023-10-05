from flask import Flask, request, url_for
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
from datetime import datetime, timedelta
# from babel import configure
# from babel import gettext

# from flask_babel import Babel
# from flask_babel import gettext, ngettext
import ast


import urllib.request
from urllib.parse import urljoin




app = Flask(__name__)
# babel = Babel(app)

#configure(app)

         
      

@app.route('/rentomat')
def rentomat():
   with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
      data = json.load(jsonFile)

   # print(data)


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

   


   return render_template('rentomat/rentomat_settings.html', rent_data = rent_data)





 


@app.route('/')
def root():
   # read_rentomat("root", "0")
   # text_test = gettext('Hello, world!')
   # print(text_test)
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

   pause_time = data['cleaning_time']



   location_from = request.args.get('location_from')
   date_from = request.args.get('date_from')
   location_to = request.args.get('location_to')
   date_to = request.args.get('date_to')

   # print("location from "+location_from)
   # print("date from "+date_from)
   # print("location to "+location_to)
   # print("date to "+date_to)

   date_object = datetime.strptime(date_to, '%Y/%m/%d %H:%M')
   #date_start_value =date_object.strftime('%Y-%m-%d %H:%M:%S')
   
   # print(date_start_value)

   time_with_pause = date_object + timedelta(hours=pause_time)
   time_with_pause_value =time_with_pause.strftime('%Y-%m-%d %H:%M:%S')
   # print("---------------------------")
   # print(time_with_pause_value)
   # print("---------------------------")

   # with open("/home/pi/VSCProjects/selfrentacar/flask_rentomat/settings.json", "r") as jsonFile:
   #    data = json.load(jsonFile)


   available_cars=[]



  
       




   for key in data['key_positions']:
  
      if (data['key_positions'][key]['rfid'] != ""):
         rfid = data['key_positions'][key]['rfid']
         


         response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

         response_data = json.loads(response.text)
         access_token = response_data['access_token']
 

         

         url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('x_key_rfid', '=', '"+rfid+"'), ('date_end', '>', '"+time_with_pause_value+"'),'|',('state','=','open'),('state','=','running')]"




         header_data = {'Access-Token' : str(access_token)}

         response = requests.get(url, headers=header_data)

         response_data = json.loads(response.text)
         print("*************************")
         print(response.text)
         print("*************************")
         # print(response.text)
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

         if(response_data['count'] == 0):


            url = "http://23.88.98.237:8069/api/fleet.vehicle?filters=[('x_key_rfid', '=', '"+rfid+"')]"
            header_data = {'Access-Token' : str(access_token)}

            response = requests.get(url, headers=header_data)

            response_data = json.loads(response.text)
            # print(response_data)
            vehicle_id = str(response_data['results'][0]['id'])


            url = "http://23.88.98.237:8069/api/fleet.vehicle/"+vehicle_id
            header_data = {'Access-Token' : str(access_token)}

            response = requests.get(url, headers=header_data)

            response_data = json.loads(response.text)
            # print(response_data)

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
               'image' : image
            }

            available_cars.append(toAdd)
            # print(available_cars)


      # location_from = request.args.get('location_from')
      # date_from = request.args.get('date_from')
      # location_to = request.args.get('location_to')
      # date_to = request.args.get('date_to')

 


   return render_template('rezervacija/listaVozila.html', cars = available_cars, location_from = location_from, date_from = date_from, location_to = location_to, date_to = date_to)



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


@app.route('/rezervacijeKorisnik', methods = ['GET', 'POST'])
def rezervacijeKorisnik():



   

   
   
   if request.method == 'POST':


        


        location = request.form.get('location')
        return_date = request.form.get('return_date')





        return redirect(url_for('submit_form', location=location, return_date=return_date))
   # return render_template('/rezervacija/rezervacijeKorisnik.html')



   location_from = request.args.get('location_from')
   date_from = request.args.get('date_from')
   location_to = request.args.get('location_to')
   date_to = request.args.get('date_to')
   carId = request.args.get('carId')






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

   # print(response.text)

   allOptions=[]


   if(response_data['count'] != 0):

      for key in response_data['results']:
          
         allOptions.append(key)

   print(allOptions)
 

   car_url = "http://23.88.98.237:8069/api/fleet.vehicle/"+carId

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(car_url, headers=header_data)

   response_data_car = json.loads(response.text)

   # print(response.text)   

   #print(vehicle_id)
   vehicle_brand = str(response_data_car['brand_id']['name'])
   vehicle_name = str(response_data_car['model_id']['name'])

   transmission = str(response_data_car['transmission'])
   category = str(response_data_car['category_id']['name'])
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
      'price': 26
   }

   years_range = list(range(1943, 2013))
   months_range = list(range(1, 13))
   days_range = list(range(1, 32))

   




   return render_template('/rezervacija/rezervacijeKorisnik.html',days_range=days_range, months_range=months_range, years_range=years_range,carDetails = toAdd, allLocations = allLocations, allOptions = allOptions)


@app.route('/submit_form',  methods=['GET', 'POST'])
def submit_form():
   
   
   
   options = request.args.getlist('options')

   deposit_amt = 0

   for el in options:
      if el == 13:
            deposit_amt = 600

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

   print(rent_details)


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

   print(user_details)

   contract_id = create_contract(rent_details, user_details)


   # response = requests.get(
   #          "http://23.88.98.237:8069/api/auth/get_tokens",
   #          params={"username": "odoo@irvas.rs", "password": "irvasadm"}
   #     )

   # response_data = json.loads(response.text)
   # access_token = response_data['access_token']


   # header_data = {'Content-Type': 'text/html; charset=utf-8', 'Access-Token' : str(access_token)}

   # url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id
   
   
   # response = requests.get(url, headers=header_data)

   # response_data = json.loads(response.text)

   # print(response_data)
      
   # contract_id = str(response_data['results'][0]['id'])


   return render_template('/rezervacija/submit_form_confirm.html', contract_id = contract_id)

   

   

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

   base_url = "https://selfcar.naisrobotics.com"
   access_url = response_data["access_url"]
   token = response_data["access_token"]
   
   


   print(response.text)



   print(base_url)
   print(access_url)
   print(token)
   final_url = base_url + access_url + "?access_token=4" + token
   print(final_url)
   # contract_id = str(response_data['results'][0]['id'])




   # print(contract_id)
   return render_template('/rezervacija/takekey.html', final_url = final_url)

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
       print("User postoji")
       user_id = response_data['results'][0]['id']
 
   else:
       print("User NE postoji")


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
   
   print("*************************")
   print(user_id)
   print("*************************")

   


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

   print("*****************")
   print(reservation_code)
   print("*****************")
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
      print("ID opcije je"+selected_option)

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
      "name": "Rent from rentomat",
      "tenant_id" : user_id, ####
      "date_start" : date_start, ####
      "date_end" : date_end, ####
      "reservation_code" : reservation_code, ####
      "notes" : notes, ####
      "rent_from" : rent_from,
      "return_location" : return_location,
      "web_car_request" : web_car_request,
      "total_rent" : total_rent,
      "state" : "running", ####
      "rent_amt" : rent_amt, ####
      "deposit_amt": deposit_amt,
      "option_ids" : option_line_ids, ####
      "currency_id" : currency_id,
      "vehicle_id" : carid,
      "duration" : days_num_var,
      "odometer": "321",
      "odometer_unit" : "kilometers"
      }


   data_insert_final = json.dumps(data_insert)
   url = "http://23.88.98.237:8069/api/fleet.rent"
   response = requests.post(url, data=data_insert_final, headers=header_data)

   # print("****************")
   # print(response.text)
   # print("****************")

   data_odometer = {
       'vehicle_id' : carid,
       'value' : "126",
       'unit' : "kilometers"
   }

   data_insert_final_odometer = json.dumps(data_odometer)
   url = "http://23.88.98.237:8069/api/fleet.vehicle.odometer"
   response = requests.post(url, data=data_insert_final_odometer, headers=header_data)



   url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('reservation_code', '=', '"+reservation_code+"')]"

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)


   contract_id = str(response_data['results'][0]['id'])

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
   print("da")
   url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('reservation_code', '=', 'RN01834_8')]"

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


   response = requests.get(
            "http://23.88.98.237:8069/api/auth/get_tokens",
            params={"username": "odoo@irvas.rs", "password": "irvasadm"}
      )

   response_data = json.loads(response.text)
   access_token = response_data['access_token']



   url = "http://23.88.98.237:8069/api/fleet.rent?filters=[('reservation_code', '=', 'RN01834_8')]"

   header_data = {'Access-Token' : str(access_token)}

   response = requests.get(url, headers=header_data)

   response_data = json.loads(response.text)
   print(response.text)


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
   
   try:
      a = int(contract_id)


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

      #print(response.text)


      position = 3
      link_ugovora = ugovor_link
      #link_ugovora = 'https://selfcar.naisrobotics.com/my/carrental_contract/47?access_token=0a23e16e-10da-47f5-9008-c239e8ae7cb6'
      #link_ugovora = 'https://selfcar.naisrobotics.com/my/invoices/18?access_token=c4d293f1-7d45-433a-b6e0-ad17f779dc23'
      
      return render_template('odoo.html', contract_id = contract_id, position = position, iframe= link_ugovora)


   except:
      print("varibale not a number")


   
   
   



@app.route('/preuzimanjeUgovorStampa')
def preuzimanjeUgovorStampa():
   return render_template('preuzimanjeUgovorStampa.html')



@app.route('/preuzimanjeKljuc', methods = ['GET', 'POST', 'PUT'])
def preuzimanjeKljuc():



   # PREUZIMANJE RFID BROJA IZ UGOVORA


   contract_id = request.args.get('contract_id')
   
   # print("Broj ugovora")
   # print(contract_id)


   try:
      rfid_num = get_rfid(contract_id)
   except:
       return render_template('/errors/non_exist_rfid_in_database.html')


   # print("RFID num")
   # print(rfid_num)
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
      # print("**************************")
      # print(rentomat_id)
      # print("**************************")
         

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
         # print("Ugovor id je: "+contract_id)
         # print("Acces token je: "+access_token)
         # print("Url je"+url)
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
   # print("Ugovor id je: "+contract_id)
   # print("Acces token je: "+access_token)
   # print("Url je"+url)
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
    

