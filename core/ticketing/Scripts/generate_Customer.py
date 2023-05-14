
from django.contrib.auth import get_user_model
from ..models import Customer
import requests
import json
from decouple import config
import urllib.parse
import csv
from celery import shared_task
# import request
def generate_user(users_data_file_path):
    """
    Using this Method we can generate user objects via csv file
    """
    User = get_user_model()
    user_manager = User.objects
    with open(users_data_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Access data using data column names
            email = row['email']
            phone_number = row['phone_number']

            F_name = row['first_name']
            L_name = row['last_name']

            user = user_manager.create_user(email = email, password=phone_number)
            customer = Customer.get(user=user)
            customer.phone = phone_number
            customer.F_name = F_name
            customer.L_name = L_name
            customer.save()

            print(f"user with this mail : {user.email} added to database")


##########################################################################################

import os

def Get_Customer_Id_API(context):
    """
    post an api to helpical for creating an ticketing customer
    and returns an customer id.
    """
    address = "cs50xiran.helpical.ir"
    url = f"https://{address}/api/v1/customer/"
    payload = json.dumps(context)
    headers = {
      'X-Api-Key':os.environ.get('Helpical_Secret_Key'),
      'Content-Type': 'application/json'
    }
    try:
      response = requests.request("POST", url, headers=headers, data=payload)
      return json.loads(response.text)
  
    except Exception as e:
      return ("failed", e)

@ shared_task  
def schedule_Customer_Generation():
    """
    # Schedule the Customer generation based on Helpical Request Limit.
    This script will post a request to helpical for generatig costomers
    this request includes 50 customer data each time .
    
    """
    batch_size= 50

    # filter the Customers Flaged by processed equal to false and count them 
    customers = Customer.objects.filter(processed = False)
    obj_count = customers.count() 
    # Seperate in the number of batch_size new objects
    if obj_count >= batch_size:
      new_objects = customers[:batch_size]
    else:
       new_objects = customers
    for obj in list(new_objects):
        # Create the Context and call the get_customer_id to create the ticketing Customer
        context = {"fname": obj.F_name,
                "lname": obj.L_name,
                "email": obj.user.email,
                "org_id": "1",
                "mobile": "",
                "password": obj.phone,
                "info": "",
                "level": "3",
                "expire_date": "",
                "tel": "",
                "internal_code": "",
                "position": "student",
                "username": "",
                "org_admin": "1"
              }
        response = Get_Customer_Id_API(context)
        if response["status_code"] != 201:
          obj.failed_to_create_customer = True
          obj.save()
        else:
          obj.Helpical_Customer_ID = response["returned_values"][0]["id"]
          obj.Helpical_Password = response["returned_values"][0]["password"]
          obj.processed = True
          obj.save()
  
    remaining_new_objects = Customer.objects.filter(processed = False).exists()
    if remaining_new_objects:
        schedule_Customer_Generation().apply_async(countdown=10)
        print("remaining")

