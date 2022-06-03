import random

from django.shortcuts import render, get_object_or_404
from authapp.models import SNUser, SNUserProfile
from mainapp.models import SNSections, SNPosts
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect


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


"""Для клика по логотипу: Переход на случайную статью"""
class RandomSNPostDetailView(DetailView):
    model = SNPosts
    # Необходимо добавить шаблон для постов
    template_name = 'mainapp/post.html'

    def get_object(self, queryset=None):
        return random.sample(list(SNPosts.objects.exclude(is_active=False)), 1)[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links_menu'] = get_links_menu()
        return context


"""Отображение постов в категории (или всех) по дате создания"""
class SNPostsListView(ListView):
    model = SNPosts
    template_name = 'mainapp/index.html'

    def get_queryset(self):
        section_pk = self.kwargs.get('pk')
        if section_pk is None:
            section_pk = 0
        queryset = super().get_queryset().filter(is_active=True).order_by('-created_at')
        if section_pk != 0:
            queryset = queryset.filter(is_active=True, section__pk=section_pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section_pk = self.kwargs.get('pk')
        context['links_menu'] = get_links_menu()
        context['category'] = SNSections.objects.get(pk=section_pk)
        return context


# Думаю, лучше сразу начинать работу с CBV, поэтому закомментил
# def get_posts(section_id=None):
#     if section_id is not None:
#         return SNPosts.objects.filter(is_active=True).filter(section=section_id)
#     else:
#         return SNPosts.objects.filter(is_active=True)
# def section(request, pk=None):
#     links_menu = get_links_menu()
#     if pk is not None:
#         if pk == 0:
#             posts = get_posts()
#             context = {
#                 'title': 'Главная',
#                 'links_menu': links_menu,
#                 'posts': posts,
#             }
#             return render(request, 'mainapp/index.html', context=context)
#         else:
#             section_item = get_object_or_404(SNSections, pk=pk)
#             posts = get_posts(pk)
#             context = {
#                 'links_menu': links_menu,
#                 'title': section_item.title,
#                 'section': section_item,
#                 'posts': posts,
#             }
#             return render(request, 'mainapp/index.html', context=context)
#     else:
#         posts = get_posts()
#         context = {
#             'title': 'Главная',
#             'links_menu': links_menu,
#             'posts': posts,
#         }
#         return render(request, 'mainapp/index.html', context=context)

"""Отображение_поста"""
class SNPostDetailView(DetailView):
    model = SNPosts
    # Необходимо добавить шаблон для постов
    template_name = 'mainapp/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links_menu'] = get_links_menu()
        return context


# Все это лучше держать не здесь, а создать отдельный модуль, типа postapp, где пользователь
# сможет взаимодействовать с постами из ЛК или что-то в этом духе. Плюс посоздавать формы
"""Создание поста"""
@method_decorator(login_required, name='dispatch')
class SNPostCreateView(CreateView):
    model = SNPosts
    template_name = ''
    fields = []
    # success_url = reverse_lazy('')


"""Изменение поста"""
@method_decorator(login_required, name='dispatch')
class SNPostUpdateView(UpdateView):
    pass


"""Удаление поста"""
@method_decorator(login_required, name='dispatch')
class SNPostDeleteView(DeleteView):
    model = SNPosts
    template_name = ''
    # success_url = reverse_lazy('')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


