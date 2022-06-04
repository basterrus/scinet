from django.http import HttpResponseRedirect
from blogapp.forms import SNPostForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from blogapp.models import SNPosts


class SNPostDetailView(DetailView):
    """Показывает список постов, надо переделать на один пост"""
    model = SNPosts
    template_name = 'blogapp/post_crud/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = SNPosts.objects.all().order_by('-is_active')
        context['title'] = 'Список постов'
        return context


class SNPostCreateView(CreateView):
    """Единственное 100% рабочее"""
    model = SNPosts
    template_name = 'blogapp/post_crud/post_detail.html'
    success_url = reverse_lazy('index')
    form_class = SNPostForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Создание поста'
        return context


class SNPostUpdateView(UpdateView):
    """Возможно тоже работает"""
    model = SNPosts
    template_name = 'blogapp/post_crud/post_detail.html'
    form_class = SNPostForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование поста'
        return context


class SNPostDeleteView(DeleteView):
    """Нужно переписать под is_аctive"""
    model = SNPosts
    template_name = 'authapp/users_crud/user_delete.html'

    def get_success_url(self):
        return reverse('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление поста'
        return context

    def form_valid(self, form, *args, **kwargs):
        """Этот кусок позволяет при отметке на чекбоксе с id del_box
        удалить полностью пост из базы (такой вариант теперь используется
        начиная с Django 4"""
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
