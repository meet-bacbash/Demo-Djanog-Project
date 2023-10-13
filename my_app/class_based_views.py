import http
from http.client import HTTPResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from my_app.models import Contact


class ContactLiestView(ListView):
    model = Contact
    template_name = "contact_list.html"

    
class ContactDetailView(DetailView):
    model = Contact

class ContactCreateView(CreateView):
    model = Contact
    fields = ["name", "email"]
    template_name = "contact_create.html"
    success_url = "/app/hi/"

class ContactUpdateView(UpdateView):
    model = Contact
    fields = ["name", "email", "address", "shipper"]


class ContactDelete(DeleteView):
    model = Contact
