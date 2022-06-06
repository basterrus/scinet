from django.http import HttpResponseRedirect
from blogapp.forms import SNPostForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from blogapp.models import SNPosts, SNSections


class SNPostDetailView(DetailView):
    """Показывает пост"""
    model = SNPosts
    template_name = 'blogapp/post_crud/post_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['comments'] = SNSections.objects.filter(pk=self.kwargs['pk'])
        context['title'] = 'Пост'
        return context


class SNPostCreateView(CreateView):
    """Создание поста"""
    model = SNPosts
    template_name = 'blogapp/post_crud/post_form.html'
    success_url = reverse_lazy('index')
    form_class = SNPostForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Создание поста'
        return context

    def post(self, request, *args, **kwargs):
        """Автоматически делаем пользователя сессии автором поста"""
        if request.user.is_authenticated:
            form = self.form_class(request.POST)
            if form.is_valid():
                blog_post = form.save(
                    commit=False)
                blog_post.user = request.user
                blog_post.save()
                return HttpResponseRedirect(reverse("index"))


class SNPostUpdateView(UpdateView):
    """Редактирование поста"""
    model = SNPosts
    template_name = 'blogapp/post_crud/post_form.html'
    form_class = SNPostForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование поста'
        return context


class SNPostDeleteView(DeleteView):
    """Удаление поста"""
    model = SNPosts
    template_name = 'blogapp/post_crud/post_delete.html'

    def get_success_url(self):
        return reverse('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление поста'
        return context

    def form_valid(self, form, *args, **kwargs):
        """По умолчанию скрывает пост, если отметить чекбокс, то удалит пост полностью"""
        success_url = self.get_success_url()
        checkbox = self.request.POST.get('del_box', None)
        if checkbox:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        else:
            if self.object.is_active:
                self.object.is_active = False
            else:
                self.object.is_active = True
            self.object.save()
            return HttpResponseRedirect(success_url)
