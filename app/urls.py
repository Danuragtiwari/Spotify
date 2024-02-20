# from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf.urls import handler404
from .views import custom_404_view 
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',login_views,name='login'),
    path('signup',signup,name='signup'),
    path('mark_favorite',mark_favorite,name='mark_favorite'),
    path('logout',logout_views,name='logout'),

    path('search/',search,name='search'),
]

# handler404 = 'custom_404_view'