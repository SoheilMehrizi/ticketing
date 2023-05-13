
from django.contrib.auth import get_user_model
from ..models import Customer
import requests
import json
from decouple import config
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



def Get_Customer_Id_API(self, context):
    """
    post an api to helpical for creating an ticketing customer
    and returns an customer id.
    """

    url = "https://{{url}}/api/v1/customer/"

    payload = json.dumps(context)
    headers = {
      'X-Api-Key': config("Helpical_Secret_Key"),
      'Content-Type': 'application/json'
    }
    try:
      response = requests.request("POST", url, headers=headers, data=payload)
      if response.status_code == 201:
        return response["returned_values"][0]['id'], response["returned_values"][0]["password"]
      else:
        return ("failed", "failed")   
    except Exception:
      return ("failed", Exception.message)

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
    for obj in new_objects:
        # Create the Context and call the get_customer_id to create the ticketing Customer
        context={"fname":obj.F_name, "lname":obj.L_name, "email":obj.user.email, 
                "password":obj.phone, "position": "Student"}
        response = Get_Customer_Id_API(self, context)
        if response[0] == "failed" :
          obj.failed_to_create_customer = True
          obj.save()
        else:
          obj.Helpical_Customer_ID = response[0]
          obj.Helpical_Password = response[1]
          obj.processed = True
          obj.save()
  
    remaining_new_objects = Customer.objects.filter(processed = False).exists()
    if remaining_new_objects:
        schedule_Customer_Generation().apply_async(countdown=60)

