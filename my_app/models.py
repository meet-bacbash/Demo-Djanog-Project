from csv import list_dialects
import imp
from typing import Any
from django.db import models
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.core.signals import request_started
from django.core.handlers.wsgi import WSGIHandler

# Create your models here.

class Contact(models.Model):

    def __str__(self):
        return self.name
    
    list_display = ('name', 'email', 'is_shipper')

    name = models.CharField(verbose_name="Name", max_length=100)
    email = models.EmailField(verbose_name="Email", unique=True)
    address = models.TextField(verbose_name="Address", help_text="Please add street, landmark, city and state with zip code.", null=True)
    is_shipper = models.BooleanField(verbose_name="Is Shipper", default=False)


class Order(models.Model):

    @staticmethod
    def get_prifix():
        return "ORD_"
    
    def __str__(self):
        return f"{self.name}_{self.customer}"


    name = models.CharField(verbose_name="Name")
    customer = models.ForeignKey(Contact, verbose_name='customer_id', on_delete=models.SET_NULL, null=True)
    payload_size = models.CharField(verbose_name="Payload Size")
    payload_weight = models.FloatField(verbose_name="Payload weight (Lbs.)", validators=[MinValueValidator(1.0)])
    shipping_date = models.DateTimeField(verbose_name="Shipping Date")

    def save(self, *args, **kwargs):
        count = Order.objects.all().count()
        self.name = "%s%s" % (Order.get_prifix(), count)
        super(self.__class__, self).save(*args, **kwargs)


class Bid(models.Model):

    @staticmethod
    def get_prifix():
        return "BID_"

    def __str__(self):
        return self.name

    name = models.CharField(verbose_name="name")
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Order")
    shipper_id = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(verbose_name="Price")
    desctiption = models.TextField(verbose_name="Description", null=True)

    def save(self, *args, **kwargs):
        count = Bid.objects.all().count()
        self.name = "%s%s" % (Bid.get_prifix(), count)
        super(self.__class__, self).save(*args, **kwargs)



@receiver(pre_save, sender=Order)
def pre_save_order(sender, instance, *args, **kwargs):
    print(sender, instance, args, kwargs)
    # notifiy all the shippers,
    if not instance.id:
        print("notifing all the shippers...")


@receiver(post_save, sender=Bid)
def post_save_bid(sender, instance, created, *args, **kwargs):
    """
    Notify customer that he got a new or updated bid on order.
    """
    print(args, kwargs)
    if created:
        print(f"sending email to {instance.order_id.customer} >>> you got new bid: {instance.name} on order: {instance.order_id}")
    else:
        print(f"sending email to {instance.order_id.customer} >>> Bid Updated: {instance.name} on order: {instance.order_id}")


# @receiver(request_started, sender=WSGIHandler)
# def hello(sender, environ, *args,**kwargs):
#     print(args, kwargs)