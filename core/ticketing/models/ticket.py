from django.db import models



class ticket(models.Model):
    """
    this model will create when a ticket arrives .
    """
    # who's the question?
    Customer_id = models.ForeignKey("Customer", on_delete=models.CASCADE)

    # ticket id _ Comes from HELPICAL
    ticket_id = models.CharField(max_length=50)

    # ticket detail
    ticket = models.TextField()
    
    # attachment's urls
    attachment = models.URLField(max_length= 250, blank=True)

    processed = models.BooleanField(default=False)
    failed_to_create_ticket = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        f"{self.Customer_id.Helpical_Customer_ID}, {self.Ticket_id}"


class post_ticket(models.Model):
    """
    this model will create when a ticket arrives .
    """
    # who's the question?
    Customer_id = models.ForeignKey("Customer", on_delete=models.CASCADE)

    # ticket id _ Comes from HELPICAL
    ticket_id = models.CharField(max_length=50)

    # ticket detail
    ticket = models.TextField()
    
    # attachment's urls
    attachment = models.URLField(max_length= 250, blank=True)

    processed = models.BooleanField(default=False)
    failed_to_create_ticket = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        f"{self.Customer_id.Helpical_Customer_ID}, {self.Ticket_id}"



class answer (models.Model):
    """
    The answer to a specific ticket.
    """
    ticket= models.ForeignKey(ticket, on_delete=models.CASCADE)

    # answer detail 
    answer = models.TextField()

    # attachment's url
    attachment = models.URLField(max_length=250, blank=True)

    processed = models.BooleanField(default=False)
    failed_to_get_answer= models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        f"{self.Customer_id.Helpical_Customer_ID}, {self.Ticket_id}"
