import json
import math
import requests
from datetime import datetime, timedelta, date, time




######  TYRES PRICES FROM WEB   ######

def getpriceextrastyresfromid(from_timestamp, to_timestamp):



   day_num = math.ceil((to_timestamp - from_timestamp)/86400)

   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

   URL = "https://cheapcarhire.rent/wp-json/my/price/getpriceextrastyresfromid?date_from="+str(from_timestamp)+"&date_to="+str(to_timestamp)

   prices_extras_tyres = requests.get(url = URL, headers = headers, data='')
   json_object_tyres = json.loads(prices_extras_tyres.text)


   tyres_price = json_object_tyres[0]['price']
   tyres_price_discount = json_object_tyres[0]['discount_percentage']
   extra_name_tyres = json_object_tyres[0]['extra_name']


   if tyres_price_discount != None:
      total_price_extra_tyres = float(day_num*float(tyres_price)*(100 - float(tyres_price_discount))/100)
   else:
      total_price_extra_tyres = float(day_num*tyres_price)


   return total_price_extra_tyres






######  SNOWCHAINS PRICES FROM WEB   ######

def getpricesnowchains():




    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    URL = "https://cheapcarhire.rent/wp-json/my/price/getpricesnowchain"

    prices_snowchain = requests.get(url = URL, headers = headers, data='')
    json_object_snowchain = json.loads(prices_snowchain.text)


    snowchain_price = json_object_snowchain[0]['price']


    total_price_snowchain = float(snowchain_price)



    return total_price_snowchain



######  INSURANCE PRICES FROM WEB   ######

def getpriceinsurancefromid(from_timestamp, to_timestamp, web_id):
   
   day_num = math.ceil((to_timestamp - from_timestamp)/86400)
   
   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

   URL = "https://cheapcarhire.rent/wp-json/my/price/getpriceinsurance?date_from="+str(from_timestamp)+"&date_to="+str(to_timestamp)+"&vehicle_id="+str(web_id)

   prices = requests.get(url = URL, headers = headers, data='')


   json_object_insurance = json.loads(prices.text)



   casco_price = json_object_insurance[0]['price']
   casco_discount = json_object_insurance[0]['discount_percentage']
   extra_id = json_object_insurance[0]['extra_id']


   total_casco_price = int(day_num)*float(casco_price)*(100-float(casco_discount))/100


   return total_casco_price




######  CHECK FOR WINTER SEASON   ######

def isWinter(from_timestamp, to_timestamp):

   is_winter = False
   winterMonths = [11,12,1,2,3]

   dt_object_from = datetime.fromtimestamp(from_timestamp)
   start_date_object = datetime.strptime(dt_object_from.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')
   start_month = start_date_object.month

   dt_object_to = datetime.fromtimestamp(to_timestamp)
   end_date_object = datetime.strptime(dt_object_to.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')
   end_month = end_date_object.month

   if start_month in winterMonths or end_month in winterMonths:
      is_winter = True

   return is_winter





######  GET CAR DEPOSIT    ######

def carDepositData(web_car_id):

   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
   URL = "https://cheapcarhire.rent/wp-json/my/price/cardeposit?car_id="+str(web_car_id)
   deposit_data = requests.get(url = URL, headers = headers, data='')

   carDepositData = json.loads(deposit_data.text)

   return carDepositData






######  PRICES EXTRA WEB ALL    ######

def pricesExtrasWebAll():

   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
   URL = "https://cheapcarhire.rent/wp-json/my/price/extras"
   extras_data = requests.get(url = URL, headers = headers, data='')
   extras_web = json.loads(extras_data.text)

   return extras_web