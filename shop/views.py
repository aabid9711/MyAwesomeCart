from django.shortcuts import render
from django.http import HttpResponse
from .models import product, Contact, Order, OrderUpdates
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from .PayTm import Checksum

Merchant_Key = 'ISafmNBmG_CV0axY'


# Create your views here.

def index(request):
    # products = product.objects.all()
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    # params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'product': products}
    # allprods = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]
    #             ]
    allprods = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nSlides), nSlides])

    params = {'allprods': allprods}
    return render(request, "shop/index.html", params)

def searchmatch(item,query):
    if query in item.product_name or query in item.product_desc or query in item.category:
        return True
    if query in item.product_name.lower() or query in item.product_desc.lower() or query in item.category.lower():
        return True
    if query in item.product_name.upper() or query in item.product_desc.upper() or query in item.category.upper():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allprods = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchmatch(item, query)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allprods.append([prod, range(1, nSlides), nSlides])

    params = {'allprods': allprods, 'msg': ""}
    if len(allprods) == 0:
        params = {'msg': 'Please enter the relevent search '}
    return render(request, "shop/search.html", params)



def about(request):
    return render(request,'shop/about.html')

def contactus(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
    return render(request,'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        email = request.POST.get('email')
        orderid = request.POST.get('orderId')
        # return HttpResponse(f"{orderid} and {email}")
        try:
            order = Order.objects.filter(order_id=orderid, email=email)
            # return HttpResponse(f"{len(order)}")
            if len(order) > 0:
                update = OrderUpdates.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc,'time': item.timestamp})
                    response = json.dumps([updates, order[0].item_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')

        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def productview(request,id):
    Product = product.objects.filter(id=id)
    print(Product)
    return render(request,'shop/productview.html', {'product': Product[0]})

def checkout(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        add1 = request.POST.get('address1')
        add2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipCode')
        phone = request.POST.get('phone')
        item_json = request.POST.get('item_json')
        order = Order(name=name, email=email, add1=add1, add2=add2, city=city, state=state, zipcode=zipcode, phone=phone, item_json=item_json,amount=amount)
        order.save()
        update = OrderUpdates(order_id=order.order_id, update_desc=" Your order has been placed .")
        update.save()
        thank = True
        id1 = order.order_id
        # return render(request, 'shop/checkout.html', {'thank': thank, 'id': id1})

        param_dict = {

            'MID': 'BlrtTn71675800767976',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/HandleReqst/',
        }

        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, Merchant_Key)

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,Merchant_Key)

        return render(request, 'shop/PayTm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')

@csrf_exempt
def HandleReqst(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, Merchant_Key, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


# bha id : 'BlrtTn71675800767976'

# key : 'ISafmNBmG_CV0axY'
