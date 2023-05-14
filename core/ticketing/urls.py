from django.urls import path, include
from . import views
app_name = "ticketing"
urlpatterns = [
    path("create_ticket/", views.Post_Ticket_View.as_view(),name = "create_ticket"),
    path("show_all_tickets/", views.show_all_tickets_TemplateView.as_view(), name="show_all_tickets"),
    path("ticket_detail/<int:ticket_id>/", views.ticket_detail_TemplateView.as_view(), name= "ticket_detail"),
    # path("reply_on_ticket/<int:ticket_id>", views.reply_on_ticket.as_view(), name= "reply_on_ticket"),

]