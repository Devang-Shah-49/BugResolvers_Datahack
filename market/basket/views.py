import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer
from .models import User, Product, Order, OrderItem, Coupon

from django.core.mail import EmailMessage
from django.conf import settings

import datetime
import random
import string

def generate_code(format, length):
    coupon_code = ''
    if format == 'numeric':
        while True:
            coupon_code = ''.join(random.choices(string.digits, k=length))
            checkk = Coupon.objects.filter(code=coupon_code).exists()
            if checkk == False:
                break
    elif format == 'alphabetic':
        while True:
            coupon_code = ''.join(random.choices(string.ascii_uppercase, k=length))
            checkk = Coupon.objects.filter(code=coupon_code).exists()
            if checkk == False:
                break

    elif format == 'alphanumeric':
        while True:
            coupon_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            checkk = Coupon.objects.filter(code=coupon_code).exists()
            if checkk == False:
                break
    return coupon_code

def send_email(data):
    email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[
                         data['to_email']], from_email=settings.EMAIL_HOST_USER)
    email.send()

@api_view(['GET'])
def get_user(request):
    reader = pd.read_csv(r'C:\Users\savla\DjangoProjects\BugResolvers_Datahack\market\jetson-sample-data.csv')
    for i in range(len(reader["client_id"])):
        slist = reader["date"][i].split("-")
        sdate = datetime.date(int(slist[0]),int(slist[1]),int(slist[2]))
        user,k = User.objects.get_or_create(client_id=reader["client_id"][i], email='devangvshah16@gmail.com', first_name="User")
        if k:
            user.set_password("12345678")
            user.last_name=i
        user.last_transaction=sdate
        user.save()
        if slist[1] in ["01","02","03"]:
            season = "Winter"
        elif slist[1] in ["04","05","06"]:
            season = "Summer"
        elif slist[1] in ["07","08","09"]:
            season = "Spring"
        else:
            season = "Fall"
        product,k = Product.objects.get_or_create(item_name=reader["item_name"][i])
        if k:
            product.price = reader["price"][i]
            product.season = season
            product.save()
        order,k = Order.objects.get_or_create(order_id=reader["order_id"][i], client_id=user, order_date=sdate)
        if k:
            order.save()
        order_item,k = OrderItem.objects.get_or_create(order=order, item_name=product)
        if k:
            order_item.quantity = 0
        order_item.quantity += reader["quantity"][i]
        order_item.save()
    return Response({"success":"success"})

@api_view(['GET'])
def send_codes(request):
    sent = 0
    inactive_users = User.objects.filter(last_transaction__lte=datetime.date.today()-datetime.timedelta(days=30))
    #print(inactive_users.values_list('last_transaction', flat=True))
    for user in inactive_users:
        coupon = Coupon.objects.create(user=user, code=generate_code('alphanumeric', 6), discount_value=random.randint(10, 50), expiry_date=datetime.date.today()+datetime.timedelta(days=30))
        data = {
            'to_email': user.email,
            'email_subject': 'Coupon Code for your next order!',
            'email_body': f'Your coupon code is {coupon.code} and it is valid till {coupon.expiry_date}.'
        }
        send_email(data)
        sent = 1
        if sent == 1:
            return Response({"Inactive Count":f"{len(inactive_users)}", "Sent":f"{sent}"})
    return Response({"success":"success"})