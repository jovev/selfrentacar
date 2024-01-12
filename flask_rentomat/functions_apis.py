import datetime
import json
import requests


def getAccesToken():
    response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

    response_data = json.loads(response.text)
    return response_data['access_token']







def getCarData(carId):

    access_token = getAccesToken()
    car_url = "http://23.88.98.237:8069/api/fleet.vehicle/"+carId

    header_data = {'Access-Token' : str(access_token)}

    response = requests.get(car_url, headers=header_data)

    return json.loads(response.text)


def getAllOptions():

    access_token = getAccesToken()
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

            allOptions.append(add_with_pricce)

    return allOptions


def getLocationNameFromId(location_id):
    access_token = getAccesToken()
    url = "http://23.88.98.237:8069/api/stock.location/"+location_id

    header_data = {'Access-Token' : str(access_token)}

    response_locationFromId = requests.get(url, headers=header_data)

    response_data_locationFromId = json.loads(response_locationFromId.text)
    return response_data_locationFromId['name']




def getContractData(contract_id):

    access_token = getAccesToken()
    url = "http://23.88.98.237:8069/api/fleet.rent/"+contract_id

    header_data = {'Access-Token' : str(access_token)}

    response = requests.get(url, headers=header_data)

    return json.loads(response.text)















def getOdooLocations():
    response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

    response_data = json.loads(response.text)
    return response_data['access_token']

def printContract():
    response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

    response_data = json.loads(response.text)
    return response_data['access_token']

def printKeyReturnConfirmation():
    response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

    response_data = json.loads(response.text)
    return response_data['access_token']



def update_odoo_rfid():
    response = requests.get("http://23.88.98.237:8069/api/auth/get_tokens",params={"username": "odoo@irvas.rs", "password": "irvasadm"})

    response_data = json.loads(response.text)
    return response_data['access_token']

