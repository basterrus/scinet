from django.shortcuts import render, get_object_or_404
from authapp.models import SNUser, SNUserProfile
from blogapp.models import SNSections, SNPosts
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse


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


def get_posts(section_id=None):
    if section_id is not None:
        return SNPosts.objects.filter(is_active=True).filter(section=section_id)
    else:
        return SNPosts.objects.filter(is_active=True)


def section(request, pk=None):
    links_menu = get_links_menu()
    if pk is not None:
        if pk == 0:
            posts = get_posts()
            context = {
                'title': 'Главная',
                'links_menu': links_menu,
                'posts': posts,
            }
            return render(request, 'mainapp/index.html', context=context)
        else:
            section_item = get_object_or_404(SNSections, pk=pk)
            posts = get_posts(pk)
            context = {
                'links_menu': links_menu,
                'title': section_item.title,
                'section': section_item,
                'posts': posts,
            }
            return render(request, 'mainapp/index.html', context=context)
    else:
        posts = get_posts()
        context = {
            'title': 'Главная',
            'links_menu': links_menu,
            'posts': posts,
        }
        return render(request, 'mainapp/index.html', context=context)


class SNPostDetailView(DetailView):
    model = SNPosts
    template_name = 'mainapp/post_crud/post_detail.html'


class SNPostCreateView(CreateView):
    model = SNPosts
    fields = []
    success_url = reverse_lazy('order:list')


class SNPostUpdateView(UpdateView):
    pass


class SNPostDeleteView(DeleteView):
    pass

