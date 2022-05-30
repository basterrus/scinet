from django.shortcuts import render, get_object_or_404
from authapp.models import SNUser, SNUserProfile
from mainapp.models import SNSections


# def index(request):
#     """Главная страница"""
#     context = {
#         'title': 'Главная',
#         'users': SNUser.objects.filter(),
#         'accounts': SNUserProfile.objects.filter(),
#     }
#     return render(request, 'mainapp/index.html', context)


def get_links_menu():
    return SNSections.objects.filter(is_active=True)


def index(request):
    links_menu = get_links_menu()
    context = {
        'title': 'Главная',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/index.html', context=context)


def section(request, pk=None):
    links_menu = get_links_menu()
    if pk is not None:
        if pk == 0:
            context = {
                'title': 'Главная',
                'links_menu': links_menu,
            }
            return render(request, 'mainapp/index.html', context=context)
        else:
            section_item = get_object_or_404(SNSections, pk=pk)
            context = {
                'links_menu': links_menu,
                'title': section_item.title,
                'section': section_item,
            }
            return render(request, 'mainapp/index.html', context=context)
    else:
        context = {
            'title': 'Главная',
            'links_menu': links_menu,
        }
        return render(request, 'mainapp/index.html', context=context)
