from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import json, asyncio
from asgiref.sync import async_to_sync

from .models import ModelChats,ModelGroup
from django.contrib.auth.models import  User

from channels.db import database_sync_to_async
from django.core.serializers.json import DjangoJSONEncoder

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        # print ("Websocket Connected . . . .", event)
        # print("My Channel Layer . . . ", self.channel_layer)
        # print("My chanel name ", self.channel_name)
        
        self.send({
            "type": "websocket.accept"
        })
          
          
        
        # group name coming from routing file
        self.groupname = self.scope['url_route']['kwargs']['groupKaNam']
        print(f"You Join the '{self.groupname}' Group")
        
          
          
        # make group to add channel in 1 group
        async_to_sync(self.channel_layer.group_add)(
            # "programmers", 
            self.groupname,
            self.channel_name
            )
        
    
    
    def websocket_receive(self, event):
        print("Websocket recieve msgs", event)
        # this text is recieving as a string     
        # event is DICTIONARY, thats why event['text'] can access
        # but in event["text"] is String  //    " {"msg": "msg"} "" 
        # in event dictionary ===> text attribute is string
        print("MESSAGE FROM CLIENT IS : ",event['text'])
        
        
        # First implement   auth_midware_stack     in ASGi file
        print("User is : ", self.scope['user'])
        
        if self.scope['user'].is_authenticated:
            
        
        
        # saving receiving data to database
            
            data = json.loads(event["text"])
            print (self.scope['user'].username)
            
            user = User.objects.get(username = self.scope['user'].username )
            group = ModelGroup.objects.get(name = self.groupname)
            chat = ModelChats.objects.create(group = group, content = data['msg'], user = user )
            chat.save()
            
         
        
            # we sending data to client through database
            
    
            chats =  ModelChats.objects.filter(group = group).last()
            print("My msg is : ",chats.content)
            print("My TIME is : ",chats.timestamp)
            time = chats.timestamp

        
            my_data = json.dumps({
                "msg": chats.content,
                "user": self.scope['user'] ,
                "time":time.strftime('%b. %d, %Y, %I:%M %p') 
                }, default=str)
            
            print("my json data", my_data)
            
            
        else:
            my_data = json.dumps({
                "msg": "Login First",
                "user": "Guest" ,
                "time":""})
            
            print("my json data", my_data)

        
        
        async_to_sync(self.channel_layer.group_send)(
            self.groupname,{
            "type": "chat.message",  # creating custom event
            # "message": event['text']
            "message": my_data
            
        })
        
   
   
    # writing own handler for chat.message 
    def chat_message(self, event):
        print("My OWN EVENT:  ",event)
        # event is dict but === message in event   event['message] is string  '{"msg": "  "}'
        # we send same string to client
        
        self.send({
            "type" : "websocket.send",
            "text": event["message"]
        })
    
    
    def websocket_disconnect(self, event):
        print ("websocket disconnect", event)
        
        
        # discard group when disconnect
        async_to_sync(self.channel_layer.group_discard)(self.groupname, self.channel_name)
        raise StopConsumer
    
    
    
    
    
    
    
    ###############################
    
    
    
    
    
    
    
class MyAsyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        # print ("Websocket Connected . . . .", event)
        # print("My Channel Layer . . . ", self.channel_layer)
        # print("My chanel name ", self.channel_name)
        
        
        
        self.groupNamee =  self.scope['url_route']['kwargs']['mygroupname']
        print(self.groupNamee)
        
        await self.send({
            "type": "websocket.accept"
        })
          
          
        # make group to add channel in 1 group
        await self.channel_layer.group_add(
            self.groupNamee, 
            self.channel_name
            )
        
    
    
    async def websocket_receive(self, event):
        print("Websocket recieve msgs", event)
        # this text is recieving as a string     
        # event is DICTIONARY, thats why event['text'] can access
        # but in event["text"] is String  //    " {"msg": "msg"} "" 
        # in event dictionary ===> text attribute is string
        print("MESSAGE FROM CLIENT IS : ",event['text'])
        
        
        # saving receiving data to database 
        # USE     await database_sync_to_async 
         
        data = json.loads(event["text"])
        group = await database_sync_to_async (ModelGroup.objects.get)(name = self.groupNamee)
        chat = await database_sync_to_async (ModelChats.objects.create)(group = group, content = data['msg'])
        await database_sync_to_async (chat.save)()
        
        
        
        
        # # we sending data to client through database
        
  
        # chats =  await database_sync_to_async(ModelChats.objects.filter)(group = group)
        # print("My msg is : ",chats.content)
        # print("My TIME is : ",chats.timestamp)
        # time = chats.timestamp
        
        # # my_data = json.dumps({
        # #     "msg": chats.content, 
        # #     "time":time.strftime('%d-%m-%YT%H:%M:%S') 
        # #     })  #time is not serializable thats why we use strftime
        
        # my_data = json.dumps({
        #     "msg": chats.content, 
        #     "time":time.strftime('%b. %d, %Y, %I:%M %p') 
        #     }, default=str)
        
        
        
        
        
        # we sending direct string to client
        
        await self.channel_layer.group_send(
            self.groupNamee,{
            "type": "chat.message",  # creating custom event
            "message": event['text']
        })
        
   
   
    # writing own handler for chat.message 
    async def chat_message(self, event):
        print("My OWN EVENT:  ",event)
        # event is dict but === message in event   event['message] is string  '{"msg": "  "}'
        # we send same string to client
        
        await self.send({
            "type" : "websocket.send",
            "text": event["message"]
            
        })
    
    
    async def websocket_disconnect(self, event):
        print ("websocket disconnect", event)
        
        
        # discard group when disconnect
        await self.channel_layer.group_discard(self.groupNamee, self.channel_name)
        raise StopConsumer
       