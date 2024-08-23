from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .models import Product,User,Cart
# Create your views here.
def home(request):
    return render(request,'home.html')


def add_user(request):
    if request.method=='POST':
        f=UserCreationForm(request.POST)
        f.save()
        return redirect('/')
    else:
        f=UserCreationForm
        context={'form':f}
        return render(request,'adduser.html',context)


def login_view(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        passw=request.POST.get('password')
        user=authenticate(request,username=uname,password=passw)
        if user is not None:
            request.session['uid']=user.id
            login(request,user)
            return redirect('/')
        else:
            return render(request,'login.html') 
    else:
        return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')


def product_view(request):
    pl=Product.objects.all()
    context={'pl':pl}
    return render(request,'product.html',context)


def add_to_cart(request,pid):
    product_id=Product.objects.get(id=pid)
    uid=request.session.get('uid')
    user_id=User.objects.get(id=uid)
    c=Cart()
    c.product=product_id
    c.user=user_id
    c.save()
    return redirect('/product')

