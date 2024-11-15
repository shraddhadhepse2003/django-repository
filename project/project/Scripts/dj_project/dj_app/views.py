from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .models import Product,Cart,Category
from django.views.generic import DeleteView
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay

from django.contrib.auth.hashers import make_password 
# Create your views here.
def home(request):
    return render(request,'home.html')


def add_user(request):
    if request.method=='POST':
        #f=UserCreationForm(request.POST)
        uname=request.POST.get('username')
        passw=request.POST.get('password')
        c_pass=request.POST.get('cpassword')
        u=User()
        u.username=uname
        u.password=passw

        user=User.objects.filter(username=uname)
        if len(uname) >10:
            messages.error(request,"Username must be under 10 characters")
            return redirect('/adduser')
        if passw != c_pass:
            messages.error(request,"Passwords do not match")
            return redirect('/adduser')
        if user.exists():
            messages.info(request, "Username is already taken")
            return redirect('/adduser')

        u = User(username=uname)
        u.set_password(passw)  # This hashes the password correctly
        u.save()
        #u.save()
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
        user1=User.objects.filter(username=uname)
        if user1.exists():
            if user is not None:
                if user.is_active:
                    request.session['uid']=user.id
                    login(request,user)
                    return redirect('/')
                else:
                    messages.error(request, "Your account is inactive.")
                    return redirect('/login')
            else:
                return render(request,'login.html')
                
        else:
            messages.info(request, "You are not register")
            return redirect('/login') 
    else:
        return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')


def product_view(request):
    #pl=Product.objects.all()
    #context={'pl':pl}
    #return render(request,'product.html',context)

    #pl=Product.objects.filter()
    #inc=set()
    #for i in pl:
        #inc.add(i.category.c_name)
    #context={'pl':pl,'inc':inc}
    #return render(request,'product.html',context)

    
    cate=Category.objects.all()
    pl=Product.objects.all()
    context={'Cate':cate,'pl':pl}
    return render(request,'product.html',context)


def add_to_cart(request,pid):
    product_id=Product.objects.get(id=pid)
    uid=request.session.get('uid')
    user_id=User.objects.get(id=uid)
    if Cart.objects.filter(user_id=uid,product=product_id).exists():
        return redirect('/product')
    c=Cart()


    c.product=product_id
    c.user=user_id
    c.save()
    return redirect('/product')

def cart_list(request):
    uid=request.session.get('uid')
    user_id=User.objects.get(id=uid)
    cl=Cart.objects.filter(user_id=uid)

    total_price= sum((item.product.p_price)*item.quantity for item in cl)
    final_price=total_price * 100

    if final_price < 100 :
        return render(request,'cart.html', {
            'cl':cl,
            'error':'order amount is too low.Please add more items to your cart.'
        })

    client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    payment=client.order.create({'amount':final_price,'currency':'INR','payment_capture':'1'})
    print(payment)

    request.session['razorpay_order_id']=payment['id']
    context={'cl':cl,'total_price':total_price,
        'final_price':final_price,'razorpay_key_id':settings.RAZORPAY_KEY_ID,
        'razorpay_order_id':payment['id']}

    return render(request,'cart.html',context)


def remove_view(request,pro):
    remo=Cart.objects.get(id=pro)
    remo.delete()
    return redirect('/clist')


def Search(request):

    uid=request.session.get('uid')
    srch=request.POST.get('srch')
    pl=Product.objects.filter(p_name__contains=srch)
    context={'pl':pl}
    return render(request,'product.html',context)



def category_page(request,category_name):
    #fname=request.session.get('fname',None)
    cate=Category.objects.all()
    pl=Product.objects.all()
    filtered_product=Product.objects.filter(category_name=category_name)
    context={'Cate':cate,'f_product':filtered_product,'pl':pl}
    return render(request,'product.html',context)

def filter_cate(request,pid):
    #uid=request.session.get('uid')
    #user=User.objects.get(id=uid)
    # cateid=Category.objects.get(id=pid)
    
    product=Product.objects.filter(category_id=pid)
    cate=Category.objects.all()
    pl=Product.objects.all()
    context={'Cate':cate,'product':product,'pl':pl}
    return render(request,'cat.html',context)

def sidebar(request):
    cate=Category.objects.all()
    context={'Cate':cate}
    return render(request,'category_list.html',context)


def update_cart(request,item_id,action):
    cart_item=get_object_or_404(Cart,id=item_id,user=request.user)

    if action=='increase':
        cart_item.quantity += 1
    elif action=='decrease':
        cart_item.quantity -= 1
        if cart_item.quantity < 1:
            cart_item.delete()
            return redirect('/clist')

    cart_item.save()
    return redirect('/clist')
    
@csrf_exempt
def success_view(request):
    if request.method=='POST':
        a=request.POST
        print(a)
        return render(request,'success.html')
    else:
        return render(request,'success.html')
