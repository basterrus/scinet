from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'


urlpatterns = [
    path('', mainapp.section, name='sections'),
    path('<int:pk>', mainapp.section, name='section'),
    path('read/<pk>/', mainapp.SNPostDetailView.as_view(), name='read'),
    path('create/', mainapp.SNPostCreateView.as_view(), name='create'),
    path('update/<pk>/', mainapp.SNPostUpdateView.as_view(), name='update'),
    path('delete/<pk>/', mainapp.SNPostDeleteView.as_view(), name='delete'),
]

