from django.shortcuts import render, redirect
from .models import ModelGroup,ModelChats

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import Custom_UserCreationForm
from django.contrib.auth import login, authenticate
# from django.contrib.auth.models import User
import logging
# Create your views here.




def chat_view(request, group_name):
    
    print(group_name)
    chats = []
    
    
    if request.user.is_authenticated:
       
        group = ModelGroup.objects.filter(name = group_name).first()
        
        if group :
            chats = ModelChats.objects.filter(group = group)
        else:
            # group = ModelGroup.objects.create(name = group_name)
            # group.save()
            return redirect("chattingapp:index")

    
        return render(request, "chattingapp/chat.html", {"group_name": group_name, "chats": chats})
    
    
    else:
        # group = ModelGroup.objects.filter(name = group_name).first()
        
        # if group :
        #     chats = ModelChats.objects.filter(group = group)
        # else:
        #     group = ModelGroup.objects.create(name = group_name)
        #     group.save()
    
        # return render(request, "chattingapp/chat.html", {"group_name": group_name, "chats": chats})
        
            return redirect("chattingapp:login")


def index_view(request):
    
     
    if request.user.is_authenticated:
        
        groups = ModelGroup.objects.all()
        # g_dict = {"group": groups}
        # print(g_dict)
    
        return render (request, "chattingapp/index.html", {"groups": groups})
    
    else:
        return redirect("chattingapp:login")



def new_country_view(request):
    
    if request.method == "POST":
        
        country_name = request.POST.get('country_name')
        
        if country_name == "":
            return redirect("chattingapp:index")

        
        if  ModelGroup.objects.filter(name = country_name).exists():
            return redirect("chattingapp:index")
        
        else:
            group = ModelGroup.objects.create(name=country_name)
            group.save()
            print("Country Name is ::: ", country_name)
            return redirect("chattingapp:index")
    
       
        
        # else:
        #     group = ModelGroup.objects.create(name = country_name)
        #     group.save()
        #     return redirect("chattingapp:index")
        
        # print("Country Name is ::: ",country_name)
        

    
    














##############################



def _loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(username = username, password= password)
            
            if user is not None:
                login(request, user)
                return redirect('chattingapp:index')
            
            else : 
                pass
        else:
            print(ValueError)
    else:
        form = AuthenticationForm()
    return render(request, 'chattingapp/login.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form =  Custom_UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print ("register successfully")
            return redirect('chattingapp:login')
    else:
        form =  Custom_UserCreationForm()
    return render(request, 'chattingapp/register.html', {'form': form})