from django.shortcuts import render

from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import ticket, Customer
from .forms import Ticket_input_form, reply_to_ticket_form
from .Scripts import get_ticket, get_all_tickets, Post_Ticket, Post_Attachment, Put_reply

class Create_ticket_view(View):
    """
    this view handles the posted tickets and prepares the tickets for showing to customer.
    """
    template_name= 'index.html'
    form = Ticket_input_form()
    def get(self, request):
        """
        this method prepares the curent ticket and all tickets of Customer .select
        """
        # IN PROGRESS
        return render(request, self.template_name, {'form':self.form})
    
    def post(self, request):
        user = request.POST['user']
        form = Ticket_input_form(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['title']
            message = form.cleaned_data['ticket_detail']
            attachment_file = request.FILES['attachment_file']
            if attachment_file:
                if attachment_file.size > 10 * 1024**2:
                    error_message = "File Size should be less than 10MB."
                    context = {'form': self.form, 'message' : error_message}
                    return render(request, self.template_name, context)
                else:
                    # create_new_ticket for current customer
                    current_customer = Customer.objects.get(user = user)
                    # get the Customer_ID
                    customer_id = current_customer.Helpical_Customer_ID
                    payload_new_ticket = {
                        "customer_id": f"{customer_id}",
                        "customer_username": "",
                        "customer_email": "",
                        "ticket_cat": 1,
                        "subject": f"{subject}",
                        "target_department_id": "1",# we have just 1 department
                        "message": f"{message}",
                        "importance": "n"
                        }
                    PTResponse = Post_Ticket(payload_new_ticket)
                    if PTResponse["status_code"] == 201:
                        ticket_id = PTResponse["returned_values"]["ticket_id"]
                        content_id = PTResponse["returned_values"]["content_id"]
                        message = ".تیکت شما با موفقیت ثبت شد ،کارشناسان ما در اسرع وقت پاسخ گو خواهند بود"
                        
                        if attachment_file:
                            # Post an attachment file
                            attachment_payload = {"content_id": content_id}
                            response = Post_Attachment(attachment_file, attachment_payload)
                            if response["status_code"] == 201:
                                pass
                            else:
                                message = "فایل بدرستی الصاق نشد لطفا چند دقیقه دیگر مجددا تلاش کنید"
                        context = {"message": message}
                        return render(request, self.template_name, context)
                    else:
                        context = {"message": "مشکلی پیش آمده است ،لطفا چند دقیقه دیگر مجدادا تلاش کنید",
                                   "status_code":PTResponse["status_code"], "error_code":PTResponse["status_code"],
                                     "error_description": PTResponse["error_description"]}
                        return render(request, self.template_name, context)            


class show_all_tickets_TemplateView(TemplateView):
    template_name = ""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(user = self.request.user)
        response = get_all_tickets(customer_id=customer.Helpical_Customer_ID)
        if response["status_code"] == 200:
            context["tickets"] = response["returned_values"]
        else:
            context["error": "مشکلی پیش آمده چند دقیقه دیگر دوباره تلاش کنید"]
        return context

class ticket_detail_TemplateView(TemplateView):
    """
    # Details of a ticket with url passed ticket_id
    Get:This Function prepares the detail of a ticket + its replies
    and attachment urls
    POST: requests to reply to current ticket and attachments
    """
    template_name = ""
    form_class = Ticket_input_form()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(user = self.request.user)
        ticket_id = self.kwargs["ticket_id"]
        response = get_ticket(ticket_id = ticket_id, 
                              customer_id=customer.Helpical_Customer_ID)
        context["ticket_details"] = response 
        context["form"] = self.form_class
        return context
    def post(self, request, *args, **kwargs):
        """
        get data from posted form
        request to create a reply to current ticket
        """
        customer = Customer.objects.get(user = self.request.user)
        customer_id = customer.Helpical_Customer_ID
        ticket_id = self.kwargs["ticket_id"]
        form = reply_to_ticket_form(request.POST, request.FILES)
        if form.is_valid():
            message = form.cleaned_data['reply_detail']
            attachment_file = request.FILES['attachment_file']
            if attachment_file:
                if attachment_file.size > 10 * 1024**2:
                    error_message = "File Size should be less than 10MB."
                    self.kwargs["error_message"] = error_message
                else:
                    payload={
                        "customer_id": customer_id,
                        "customer_username": "",
                        "customer_email": "",
                        "ticket_id": ticket_id,
                        "message": f"{message}",
                        "reply_and_close": "0"}
                    response = Put_reply(payload)
                    if response["status_code"] == 202:
                       content_id =  response["returned_values"]["content_id"]
                       attachment_payload = {"content_id": content_id}
                       response = Post_Attachment(attachment_file, attachment_payload)
                       if response["status_code"] == 201:
                          self.kwargs["message"] = "فایل بدرستی الصاق شد"
                       else:
                            message = "فایل بدرستی الصاق نشد لطفا چند دقیقه دیگر مجددا تلاش کنید"
            else:
                payload={
                        "customer_id": customer_id,
                        "customer_username": "",
                        "customer_email": "",
                        "ticket_id": ticket_id,
                        "message": f"{message}",
                        "reply_and_close": "0"}
                response = Put_reply(payload)
                if response["status_code"] == 202:
                    self.kwargs["message"] = "ریپلای با موفقیت انجام شد"
                else:
                    self.kwargs["message"] = "ارسال ریپلای شکست خورد، چند دقیقه بعد مجدد تلاش کنید"
        return self.get(request, *args, **kwargs)
    