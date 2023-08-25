from django.contrib import admin
from .models import ModelChats , ModelGroup
# Register your models here.

class AdminGroup(admin.ModelAdmin):
    list_display = ["id", "name"]


class AdminChats(admin.ModelAdmin):
    list_display = ["id", "group", "user", "timestamp", "content"]
    
    
admin.site.register(admin_class=AdminGroup, model_or_iterable=ModelGroup)
admin.site.register(admin_class=AdminChats, model_or_iterable=ModelChats)
    