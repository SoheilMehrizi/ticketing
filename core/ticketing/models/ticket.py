from django.db import models


class ticket(models.Model):
    """
    this model will create when a ticket arrives .
    """
    # who's the question?
    Customer = models.ForeignKey("Customer", on_delete=models.CASCADE)

    # ticket id _ Comes from HELPICAL
    ticket_id = models.CharField(max_length=50, blank = True)
    
    is_closed = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    failed_to_create_ticket = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        f"{self.Customer.Helpical_Customer_ID}, {self.Ticket_id}"