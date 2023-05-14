from django import forms


class Ticket_input_form(forms.Form):
    """
    # Form for user to enter the Ticket and its attachments.
    """
    subject = forms.CharField(max_length=200)
    ticket_detail = forms.CharField(max_length=350)
    # attachment_file = forms.FileField()


class reply_to_ticket_form(forms.Form):
    """
    # Form for user to reply to ticket and its attachments.
    """
    reply_detail = forms.CharField(max_length=300)
    # ticket_detail = forms.CharField(max_length=350)
    # attachment_file = forms.FileField()
