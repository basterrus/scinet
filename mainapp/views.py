from django.shortcuts import render
from authapp.models import SNUser, SNUserProfile


def index(request):
    """Главная страница"""
    context = {
        'title': 'Главная',
        'users': SNUser.objects.filter(),
        'accounts': SNUserProfile.objects.filter(),
    }
    return render(request, 'mainapp/index.html', context)
