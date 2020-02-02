from django.contrib.auth import authenticate,logout,login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import *

def login_req(request):
    user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
    if user is not None:
        login(request, user)
        return HttpResponseRedirect("/lk")
    else:
        messages.success(request, 'Проверьте введенные данные')
        return HttpResponseRedirect('/login')


def reg_req(request):
    print(request.POST)
    email = request.POST.get('email')

    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    # data = {'email': email, 'phone': phone, 'password2': password2, 'password1': password1, 'isOfferRent':isOfferRent}
    data = request.POST.copy()

    form = SignUpForm(data)

    if not form.errors:
        new_user = form.save(data)
        login(request, new_user)
        return HttpResponseRedirect("/lk")
    else:
        print(form.errors)
        data, errors = {}, {}
        messages.success(request, form.errors)
    return HttpResponseRedirect("/login?tab=reg")

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def update_req(request):
    print(request.POST)
    form = UpdateForm(request.POST, request.FILES, instance=request.user)
    print(form.errors)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/lk')
    else:
        form = UpdateForm()
    return HttpResponseRedirect("/lk")