from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'


urlpatterns = [
    path('', mainapp.section, name='sections'),
    path('<int:pk>', mainapp.section, name='section'),
]

