import requests
import json
from decouple import config

# Api's to Helpical 
# Requests ,Post: Create_new_tickets , Create_attachment an attachment
# Put, Put an reply 
# GET, all related Tickets of an specific Customer.

# Post A new Ticket
def Post_Ticket(context):
    """
    this function will post a request to create a new ticket
    and returns 2 value : ticket_id(usage in reply consequences) and 
    Content_id(using for adding attachments)
    """
    address = "cs50xiran.helpical.ir"
    url = f"https://{address}/api/v1/ticket/customer-new/"
    payload = json.dumps(context)

    headers = {
       'X-Api-Key': config("Helpical_Secret_Key"),
       'Content-Type': 'application/json'
    }
    response = json.loads(requests.request("POST", url, headers=headers, data=payload))
    return response

def Post_Attachment(file_address, context):
    """
    this function sends a request to the Helpical for attaching files to a specific content
    """
    
    # the Url of request
    address = "cs50xiran.helpical.ir"  
    url = f"https://{address}/api/v1/ticket/attachment"
    # headers of the request
    headers = {
       'X-Api-Key': config("Helpical_Secret_Key"),
       'Content-Type': 'application/json'
    }
    # payload just includes the content_id
    payload = json.dumps(context)
    # attached_files
    files=[
        ('attachment[]',('file',open(file_address,'rb'),'application/octet-stream'))
    ]
    response = json.loads(requests.request("POST", url, headers=headers, data=payload, files=files))
    return response

# PUT Modules

def Put_reply(context):
    """
    this function makes an request for creating a content on a specific open ticket
    """
    # url of the customer
    address = "cs50xiran.helpical.ir"
    url = f"https://{address}/api/v1/ticket/customer-reply/"

    # headers of the request
    headers = {
       'X-Api-Key': config("Helpical_Secret_Key"),
       'Content-Type': 'application/json'
    }
    # the generated message include data;s such as customer_id and ticket_id
    payload = json.dumps(context)

    response = json.loads(requests.request("PUT", url, headers=headers, data=payload))
    return response

def close_ticket(context):
    """
    this function requests to close a ticket .
    useless for now , the operator closes the session
    """
    headers = {
       'X-Api-Key': config("Helpical_Secret_Key"),
       'Content-Type': 'application/json'
    }

    address = "cs50xiran.helpical.ir"
    url = f"https://{address}/api/v1/ticket/customer-close/"
    payload = json.dumps(context)

    response = json.loads(requests.request("PUT", url, headers=headers, data=payload))
    if response.get("status_code") == 202:
        return response.get("status_code"), response.get("status_title")
    else:
        return response.get("status_code"), response.get("error"), response.get("status_title")
    
# GET API's

def get_ticket(customer_id, ticket_id):
    """
    this function returns a specific ticket that belongs to a specific customer.
    and we can see the ticket and its replies and its attachments.
    this function's url needs : customer_id and ticket_id.
    """
    address = "cs50xiran.helpical.ir"
    url =  f"https://{address}/api/v1/ticket/customer-ticket/{customer_id}/{ticket_id}/"
    headers = {
       'X-Api-Key': config("Helpical_Secret_Key"),
       'Content-Type': 'application/json'
    }
    payload = {}

    response = json.loads(requests.request("GET", url, headers=headers, data=payload))
    return response

def get_all_tickets(customer_id):
    """
    this function returns a specific customer's all tickets
    so Customer can see tickets and their replies and attachments.
    sample:
    "returned_values": [
    {
      "ticket_id": 19,
      "title": "Sample title 2",
      "cat_id": 3,
      "cat_title": "Software issues",
      "status": "o",
      "create_date_time": "2019-08-01 18:39:56",
      "importance": "l",
      "seen": "0",
      "satisfaction": "3",
      "update_date_time": "2019-08-01 18:39:56",
      "owner_department_name": "Customers",
      "owner_user_name": "Sample Customer",
      "owner_username": "username1",
      "owner_user_id": 4,
      "target_department_name": "Support department",
      "target_user_name": "Mohammad Saberi",
      "targer_username": "username2"
    },]
    """

    address = "cs50xiran.helpical.ir"
    url =  f"https://{address}/api/v1/ticket/customer-tickets/{customer_id}/"
    headers = {
       'X-Api-Key': config('Helpical_Secret_Key'),
       'Content-Type': 'application/json'
    }
    payload = {}
    response = json.loads(requests.request("GET", url, headers=headers, data=payload))
    return response
    


