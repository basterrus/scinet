import random
from blogapp.models import SNSections, SNPosts
from django.views.generic import ListView, DetailView


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
        context['posts'] = SNPosts.objects.all()
        context['links_menu'] = get_links_menu()
        context['category'] = SNSections.objects.filter(pk=section_pk)
        return context


"""Отображение_поста"""
class SNPostDetailView(DetailView):
    model = SNPosts
    # Необходимо добавить шаблон для постов
    template_name = 'mainapp/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links_menu'] = get_links_menu()
        return context
