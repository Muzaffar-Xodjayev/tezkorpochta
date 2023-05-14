import json
import logging
from .utils import send_verify_code, hide_phone_number_nums,send_reset_password

import requests
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import *


# Create your views here.
def intro_page(request):
    data = Done_Jobs.objects.all()
    return render(request, "intro.html",{"data":data})

def register_page(request):
    context={}
    if request.method == 'POST':
        captcha_token = request.POST['g-recaptcha-response']
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_secret = "6LevaQAmAAAAAMipp_0WNE4hvou9KweWnZ8PAB27"
        captcha_data = {"secret":captcha_secret,"response":captcha_token}
        captcha_server_response = requests.post(url=captcha_url,data=captcha_data)
        captcha_json = json.loads(captcha_server_response.text)
        if captcha_json["success"] == False:
            context["msg"] = '"Я не робот" bo`limini tekshiring'
            context["status"] = "alert alert-danger"
        else:
            pwd = request.POST['pwd']
            phone_number = request.POST['phone_number']
            fname = request.POST["fname"]
            lname = request.POST["lname"]
            user = Account.objects.create_user(fname, lname, phone_number, pwd)
            user.save()
            code = random.randint(10000,99999)
            c = Code.objects.create(user=user,code=code)
            c.save()
            send_verify_code(phone_number, code)
            phone_number = hide_phone_number_nums(user.phone_number)
            request.session['phone_number'] = phone_number
            login(request=request,user=user)
            return redirect("phone-verify")

    return render(request, "register.html",context)

def login_page(request):
    context = {}
    user = None
    if request.method == "POST":  
        phone_number = request.POST["phone_number"] 
        pwd = request.POST["pwd"]
        user = authenticate(phone_number=phone_number,password=pwd)
        if user:
            login(request=request,user=user)
            if user.phone_verify:
                return redirect("intro-page")
            else:
                print(user)
                code = random.randint(10000,99999)
                c = Code.objects.get(user=user)
                c.code = code
                c.save()
                send_verify_code(phone_number, code)
                phone_number = hide_phone_number_nums(user.phone_number)
                request.session['phone_number'] = phone_number
                return redirect("phone-verify")
        else:
            context["msg"] = "Parol Yoki Telefon raqam xato !!!"
            context["status"] = "alert alert-danger"
            
    return render(request, "login.html",context)

def logout_page(request):
    logout(request)
    return redirect('intro-page')

def check_user(request):
    phone_number = request.GET['phone_number']
    check = Account.objects.filter(phone_number=phone_number)
    if len(check)>0:
        return HttpResponse('Exists')
    else:
        return HttpResponse('No Exists')


@login_required
def project_detail(request,pk):
    data = Done_Jobs.objects.get(id=pk)
    return render(request, "project_detail.html",{"data":data})

@login_required
def profile_page(request):
    data = Account.objects.get(id=request.user.id)
    return render(request, "profile.html",context={"data":data})

@login_required
def edit_profile(request):
    if request.method == "POST":
        user = Account.objects.get(phone_number=request.user.phone_number)
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        user.phone_number = request.POST.get('phone_number')
        user.save()
        return redirect('profile-page')
    data = Account.objects.get(id=request.user.id)
    return render(request,"edit_profile.html",context={"data":data})

@login_required
def edit_password(request):
    context={}
    if request.method == "POST":
        old_pwd = request.POST.get("old_pwd")
        new_pwd = request.POST.get("new_pwd")
        user = Account.objects.get(id=request.user.id)
        if user.check_password(old_pwd):
            user.set_password(new_pwd)
            user.save()
            login(request,user)
            context["msg"] = "Parol muvaffaqiyatli o'zgartirildi"
            context['status'] = "alert alert-success"
        else:
            context["msg"] = "Eski parol xato !!!"
            context['status'] = "alert alert-danger"
    return render(request,"edit_password.html",context)

@login_required
def order(request):
    if request.method == "POST":
        sender_name = request.POST["sender_name"]
        sender_phone_number = request.POST["sender_phone_number"]
        product_name = request.POST["product_name"]
        product_weight = request.POST["product_weight"]
        product_price = request.POST.get("product_price")
        client_name = request.POST["client_name"]
        client_phone_number = request.POST["client_phone_number"]
        address = request.POST["address"]
        user = get_object_or_404(Account, phone_number=sender_phone_number)
        data = Order.objects.create(
            sender_person_phone_number=user,
            sender_person_name=sender_name,
            product_name=product_name,
            product_weight=product_weight,
            product_price=product_price,
            address=address,
            client_name=client_name,
            client_phone_number=client_phone_number,
            product_status="Kutilmoqda"
        )
        data.save()
        return redirect("done-order-page")
    return render(request, "order.html")

@login_required
def done_order(request):
    return render(request,"done_order.html")

@login_required
def my_orders(request):
    data = Order.objects.filter(sender_person_phone_number=request.user)
    return render(request, "my_order.html",{"datas":data})

def phone_number_verify(request):
    context = {}
    user = request.user
    if request.method == 'POST':
        get_user_code = request.POST.get('verify_code')
        verify_code = Code.objects.get(user=user)
        if str(verify_code) == str(get_user_code):
            user = Account.objects.get(id=user.id)
            user.phone_verify = True
            user.save()
            login(request=request,user=user)
            return redirect("intro-page")
        else:
            context["msg"] = "Bir martalik parol xato !!!"
            context["status"] = "alert alert-danger"
    return render(request, 'phone_verify.html', context=context)

def forgot_password(request):
    context = {}
    if request.method == "POST":
        phone_number = request.POST["phone_number"]
        code = random.randint(100000, 999999)
        user = Account.objects.get(phone_number=phone_number)
        user.set_password(str(code))
        user.save()
        context["msg"] = "Siz kiritgan telefon raqamga saytga kirish uchun doimiy parol yuborildi"
        context["status"] = "alert alert-success"
        send_reset_password(phone_number,code)
    return render(request,"forgot_password.html",context)

def error_404(request, exception):
    return render(request,"error_404.html")