from email import header
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from django.views.generic import TemplateView, ListView
import time
from my_app.models import Order
from django.forms.models import model_to_dict

# Create your views here.


# @cache_page(200)
def sayhello(req):
    time.sleep(0.5)
    return HttpResponse("<h1>Hello</h1>")


class AboutPage(TemplateView):

    template_name = "about.html"


class OrderListView(ListView):
    model = Order


    def head(self, *args, **kwargs):
        last_order = self.get_queryset().latest("pk")
        return HttpResponse(
            headers = {
                "Leatest Order": last_order.name
            }
        )
    
    def get(self, request):
        data = map(lambda o: o.__dict__,Order.objects.all())
        return HttpResponse(content=data)
    