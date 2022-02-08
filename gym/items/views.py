from ast import Add
import json
from django.views.generic.edit import FormView 
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.views import LoginView
from .models import *
from django.contrib.auth import logout,login
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def home(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,is_completed=False)
        items=order.orderitems_set.all()
        cart_items=order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0}
        cart_items=order['get_cart_items']
    return render(request,'items/home.html',{
        'cart_items':cart_items
    })

class UserLoginView(LoginView):
    template_name='items/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('items:home')


def logoutview(request):
    if request.method == 'POST':
        logout(request)
        return redirect(reverse_lazy('items:home'))   
    return render(request,'items/logout.html')


def products(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,is_completed=False)
        items=order.orderitems_set.all()
        cart_items=order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0}
        cart_items=order['get_cart_items']
    products=Product.objects.all()

    context={
        'products':products,
        'cart_items':cart_items
    }

    return render(request,'items/products.html',context)


def workoutplans(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,is_completed=False)
        items=order.orderitems_set.all()
        cart_items=order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0}
        cart_items=order['get_cart_items']
    
    return render(request,'items/workoutplans.html',{
        'cart_items':cart_items
    })    

class RegisterPage(FormView):
    template_name = 'items/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('items:home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('items:home')
        return super(RegisterPage, self).get(*args, **kwargs)


def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,is_completed=False)
        items=order.orderitems_set.all()
        cart_items=order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0}
        cart_items=order['get_cart_items']

    return render(request,'items/cart.html',{
        'items':items,
        'order':order,
        'cart_items':cart_items
    })                

def updateitem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']

    print('Action:', action)
    print('Product:', productId)
    

    customer = request.user.customer
    product=Product.objects.get(id=productId)

    order,created = Order.objects.get_or_create(customer=customer,is_completed=False)
    orderItem,created = OrderItems.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)  

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item Was Added',safe=False)