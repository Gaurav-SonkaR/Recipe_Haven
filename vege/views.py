from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login/')
def receipes(request):
    if request.method == "POST":
        data = request.POST
        receipe_name =  data.get('receipe_name')
        receipe_description =  data.get('receipe_description')
        receipe_image =  request.FILES.get('receipe_image')
        ingredients = data.get('ingredients')
        receipe_method = data.get('receipe_method')
        
        Receipe.objects.create(
            receipe_name = receipe_name,
            receipe_description = receipe_description ,
            receipe_image = receipe_image,
            ingredients = ingredients,
            receipe_method = receipe_method,
        )

        return redirect('/receipes/')

    queryset = Receipe.objects.all()

    if request.GET.get('search_reciepe'):
        queryset = Receipe.objects.filter(receipe_name__icontains = request.GET.get('search_reciepe'))

    context = {'receipes': queryset}    
    return render(request,'receipes.html',context)


@login_required(login_url='/login/')
def delete_receipe(request,id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect('/receipes/')


@login_required(login_url='/login/')
def update_receipe(request,id):
    queryset = Receipe.objects.get(id = id)

    if request.method == "POST":
        data = request.POST
        receipe_name =  data.get('receipe_name')
        receipe_description =  data.get('receipe_description')
        receipe_image =  request.FILES.get('receipe_image')
        ingredients = data.get('ingredients')
        receipe_method = data.get('receipe_method')
        
       
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description 
        queryset.ingredients = ingredients
        queryset.receipe_method = receipe_method

        if receipe_image:
            queryset.receipe_image = receipe_image

        queryset.save()
        return redirect('/receipes/')

    context = {'receipe': queryset} 
    return render(request,"update_receipe.html",context)


def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request,'Invalid User')
            return redirect('/login/')

        user = authenticate(username = username , password = password)

        if user is None:
            messages.error(request , 'Invalid Password')
            return redirect('/login/')
        else :
            login(request,user)
            return redirect('/receipes/')

    return render(request , "login.html")

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register_page(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request , 'Username already exists try with another username')
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )  # for regular save of data

        user.set_password(password) # to save password in encrypted form
        user.save()

        messages.info(request, 'Account Created Successfully')
        return redirect('/register/')

    return render(request , "register.html")

def receipe_about(request,id):
    queryset = Receipe.objects.get(id = id)

    ingredients = queryset.ingredients.split(',,')
    receipe_method = queryset.receipe_method.split(',,') 

    context = {'receipe': queryset,
               'ingredients' : ingredients,
               'receipe_method' : receipe_method} 
    return render(request , "receipeabout.html",context)
    
