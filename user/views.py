from django.http import HttpResponseBadRequest
from django.shortcuts import render,redirect
from django.urls import reverse
from fisrtbook.models import *
from .models import*
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from django.contrib import messages,auth
from django.contrib.auth.models import User
import stripe
from django.conf import settings

# Create your views here.

def listBook(req):
    books=Book.objects.all()
    paginator=Paginator(books,4)
    pagenumber=req.GET.get('page')  

    try:
        page=paginator.get_page(pagenumber)
    except EmptyPage:
        page=paginator.page(pagenumber.num_pages)

    return render(req,'users/booklist.html',{'books':books,'page':page})

def detailsview(req,book_id):
    book=Book.objects.get(id=book_id)

    return render(req,'users/bookdetails.html',{'book':book})

def search_book(req):
    query=None
    books=None

    if 'q' in req.GET:

        query=req.GET.get('q')
        books=Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))

    else:
        books=[]
    context={'books':books,'query':query}

    return render(req,'users/search.html',context)

def register(req):

    if req.method=='POST':
        username=req.POST.get('username')

        password=req.POST.get('password')
        cpassword=req.POST.get('password1')

        if password==cpassword:

            if User.objects.filter(username=username).exists():
                messages.info(req,'This username already exits')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,password=password)
            return redirect('login')
        
        else:
            messages.info(req,'This password not matching')
            return redirect('register')
        


    return render(req,'account/register.html')

def login(req):

    if req.method=='POST':
        username=req.POST.get('username')
        password=req.POST.get('password')
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(req,user)
            return redirect('listbook')
        else:
            messages.info(req,'please provide proper credential')
            return redirect('login')

    return render(req,'account/login.html')

def logout(req):
    auth.logout(req)

    return redirect('login')

def add_to_cart(req,book_id):
    book=Book.objects.get(id=book_id)

    if book.quantity > 0:
        cart,created=Cart.objects.get_or_create(user=req.user)
        cart_item,item_created=CartItem.objects.get_or_create(cart=cart,book=book)

        if not item_created:

            cart_item.quantity+=1
            cart_item.save()

    return redirect('viewcart')


def view_cart(req):

    cart,created=Cart.objects.get_or_create(user=req.user)
    cart_items=cart.cartitem_set.all()
    cart_item=CartItem.objects.all()
    total_price=sum(item.book.price * item.quantity for item in cart_items)
    total_items=cart_item.count()
    item_totals = [item.book.price * item.quantity for item in cart_items]

    context={
        'cart_item':cart_item,
        'cart_items':cart_items,
        'total_price':total_price,
        'total_items':total_items,
        'item_totals': item_totals,
    }
    print(item_totals)

    return render(req,'users/cart.html',context)

def increase_quantity(req,item_id):
    cart_item=CartItem.objects.get(id=item_id)
    if cart_item.quantity < cart_item.book.quantity:
        print(cart_item.quantity)

        cart_item.quantity += 1
        cart_item.save()
    return redirect('viewcart')

def decrease_quantity(req,item_id):
    cart_item=CartItem.objects.get(id=item_id)
    print(cart_item.quantity)

    if cart_item.quantity > 1:
        print(cart_item.quantity)

        cart_item.quantity -= 1

        cart_item.save()
    return redirect('viewcart') 

def remove_from_cart(req,item_id):

    try:

        cart_item=CartItem.objects.get(id=item_id)
        cart_item.delete()
    except cart_item.DoesNotExist:
        pass
    return redirect('viewcart')


def create_checkout_session(req):
    cart_items=CartItem.objects.all()
    

    if cart_items:
        stripe.api_key=settings.STRIPE_SECRET_KEY

        if req.method == 'POST':
            quantity = int(req.POST.get('quantity', 1))
            line_items=[]
            for cart_item in cart_items:

                if cart_item.book:
                    line_item={
                        'price_data':{
                            'currency':'INR',
                            'unit_amount':int(cart_item.book.price * 100),
                            'product_data':{
                                'name':cart_item.book.title
                            },

                        },
                        'quantity':quantity,
                    }
                    line_items.append(line_item)
            checkout_session = None
            if line_items:
                checkout_session=stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=req.build_absolute_uri(reverse('success')),
                    cancel_url=req.build_absolute_uri(reverse('cancel'))

                )

                return redirect(checkout_session.url,code=303)
            

        
            
def success(req):
    cart_items=CartItem.objects.all()

    for cart_item in cart_items:
        product=cart_item.book
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()


    cart_items.delete()

    return render(req,'users/success.html')

def cancel(req):
    return render(req,'users/cancel.html')            