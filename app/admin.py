from django.contrib import admin
from .views import * 
# Register your models here.
admin.site.register([Album, Artist, Favorite])