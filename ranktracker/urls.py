from django.contrib import admin
from django.urls import path
from home.views import *

urlpatterns = [
    path('', home, name="home"),
    path('form_submit/', form_submit, name='form_submit'),
    path('admin/', admin.site.urls),
]
