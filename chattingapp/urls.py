from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


# this is important
# all names called after this name 

# i.e.    chattingapp:chat_app    

app_name = 'chattingapp'

urlpatterns = [
    
    path("login/", views._loginView, name= 'login'),
    path("register/", views.register , name= "register"),
    path("logout/" , LogoutView.as_view(next_page = "chattingapp:login")),  
      
    path("", views.index_view, name= 'index'),
    path ("<str:group_name>/", views.chat_view, name= "chat_apps"),
    # path ("", views.chat_view, name= "chat_app"),

    path('/group/', views.new_country_view, name='new_group'),

]
