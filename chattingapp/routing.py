from django.urls import path, include
from .consumers import MySyncConsumer,MyAsyncConsumer
websocket_urlpatterns = [
    path("ws/sc/<str:groupKaNam>/", MySyncConsumer.as_asgi()),
    path("ws/ac/<str:mygroupname>/", MyAsyncConsumer.as_asgi()),

    
]