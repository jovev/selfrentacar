@app.route('/rezervacijeKorisnik', methods = ['GET', 'POST'])
def rezervacijeKorisnik():



   

   
   
   if request.method == 'POST':


        


      location = request.form.get('location')
      return_date = request.form.get('return_date')
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


   winterMonths = [11,12,1,2,3]


   currentYear = datetime.now().year

   currentMonth = datetime.now().month


   # print("current month")
   # print(type(currentMonth))


   snowchain_date_from = datetime.strptime(str(currentYear-1)+"/11/1", "%Y/%m/%d")
   timestamp_snow_chain_from =(int(snowchain_date_from.timestamp()))

   snowchain_date_to = datetime.strptime(str(currentYear+1)+"/04/1", "%Y/%m/%d")
   timestamp_snow_chain_to =(int(snowchain_date_to.timestamp()))


   today = date.today()
   current_date = datetime.strptime(str(today), "%Y-%m-%d")
   today_timestamp = (int(current_date.timestamp()))
   
   # current_date = datetime.strptime(str(now_date), "%Y/%m/%d")
   # timestamp_current_date =(int(current_date.timestamp()))
   # print("today timestamp")
   # print(today_timestamp)

   # print("timestamp_snow_chain_from")
   # print(timestamp_snow_chain_from)

   # print("timestamp_snow_chain_to")
   # print(timestamp_snow_chain_to)

   if currentMonth in winterMonths:
   # if today_timestamp > timestamp_snow_chain_from and today_timestamp < timestamp_snow_chain_to:
      is_winter = True

   # print("Is winter?")
   # print(is_winter)
   

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


         # print("Options from odoo")
         # print(response.text)

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



   day_num_timestamp = day_num*24*3600

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

   deposit_discount = 1
   # if day_num == 1 or day_num == 2:
   #    deposit_discount = 1
   # elif day_num == 3 or day_num == 4:
   #    deposit_discount = 0.75
   # elif day_num == 5 or day_num == 6 or day_num == 7:
   #    deposit_discount = 0.6
   # else:
   #    deposit_discount = 0.5

   print("deposit_discount")
   print(deposit_discount)

   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
   URL = "https://cheapcarhire.rent/wp-json/my/price/cardeposit?car_id="+str(web_car_id)
   deposit_data = requests.get(url = URL, headers = headers, data='')
   deposit = json.loads(deposit_data.text)[0]['fixed_rental_deposit']
   deposit_price = float(json.loads(deposit_data.text)[0]['price'])*float(day_num)*deposit_discount
   print("depozit: ")
   print(deposit_data.text)
   # print(deposit)






   # kasko osiguranje

   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

   URL = "https://cheapcarhire.rent/wp-json/my/price/getpriceinsurance?date_from="+str(from_timestamp)+"&date_to="+str(to_timestamp)+"&from=1&to=522&vehicle_category_id="+str(vehicle_category_id)+"&vehicle_id="+str(web_car_id)+"&duration="+str(day_num_timestamp)

   prices = requests.get(url = URL, headers = headers, data='')


   print("Kasko extras prices: ")
   print(prices.text)
   json_object_insurance = json.loads(prices.text)



   casco_price = json_object_insurance[0]['price']
   casco_discount = json_object_insurance[0]['discount_percentage']
   extra_id = json_object_insurance[0]['extra_id']


   total_casco_price = int(day_num)*float(casco_price)*(100-float(casco_discount))/100


   print("total_casco_price")
   print(total_casco_price)

# SELECT 
# wp_car_rental_extras.price, 
# wp_car_rental_discounts.discount_percentage, 
# wp_car_rental_extras.extra_id, 
# wp_car_rental_discounts.period_from, 
# wp_car_rental_discounts.period_till 

# FROM wp_car_rental_extras LEFT JOIN wp_car_rental_discounts ON wp_car_rental_discounts.extra_id = wp_car_rental_extras.extra_id 

# WHERE 

# wp_car_rental_extras.item_id = $vehicle_category_id  
# AND 
# ($duration_timestamp BETWEEN wp_car_rental_discounts.period_from AND wp_car_rental_discounts.period_till OR wp_car_rental_discounts.period_till IS NULL) 
# AND 
# wp_car_rental_extras.extra_name LIKE 'SCDW%'





   # EXTRAS
   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
   URL = "https://cheapcarhire.rent/wp-json/my/price/extras"
   extras_data = requests.get(url = URL, headers = headers, data='')
   extras_web = json.loads(extras_data.text)


   # print("Extras from web")
   # print(extras_data.text)
   # print("Extras extras from web end")

   
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


   print("Price Extras: ")
   print(prices_extras.text)
   json_object = json.loads(prices_extras.text)

   price_per_day_extra = 0
   total_price_extra = 0
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


   return render_template('/rezervacija/rezervacijeKorisnik.html',total_casco_price=total_casco_price, tyres=tyres, is_winter=is_winter, extras_web=extras_web, days_range=days_range, months_range=months_range, years_range=years_range,carDetails = toAdd, allLocations = allLocations, allOptions = allOptions)
