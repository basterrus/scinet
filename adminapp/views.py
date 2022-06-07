from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from adminapp.forms import SNPostAdminForm
from authapp.forms import SNUserRegisterForm, SNUserEditForm
from authapp.models import SNUser
from blogapp.models import SNPosts


class AccessMixin:
    """Делает view доступным только для суперпользователя"""

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DeleteMixin:
    """Даёт выбор для полного удаления через чекбокс"""

    def form_valid(self, form, *args, **kwargs):
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


"""CRUD для управления пользователями"""


class SNUserCreateView(AccessMixin, CreateView):
    model = SNUser
    template_name = 'adminapp/users_crud/user_form.html'
    success_url = reverse_lazy('index')
    form_class = SNUserRegisterForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Создание пользователя'
        return context


class SNUserListView(AccessMixin, ListView):
    model = SNUser
    template_name = 'adminapp/users_crud/users.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = SNUser.objects.all().order_by('-is_active')
        context['title'] = 'Список пользователей'
        return context


class SNUserUpdateView(AccessMixin, UpdateView):
    model = SNUser
    template_name = 'adminapp/users_crud/user_form.html'
    form_class = SNUserEditForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование пользователя'
        return context


class SNUserDeleteView(AccessMixin, DeleteMixin, DeleteView):
    model = SNUser
    template_name = 'adminapp/users_crud/user_delete.html'

    def get_success_url(self):
        return reverse('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление пользователя'
        return context


"""CRUD для управления постами"""


class SNPostCreateView(AccessMixin, CreateView):
    model = SNPosts
    template_name = 'adminapp/posts_crud/post_form.html'
    success_url = reverse_lazy('index')
    form_class = SNPostAdminForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Создание поста'
        return context


class SNPostsListView(AccessMixin, ListView):
    model = SNPosts
    template_name = 'adminapp/posts_crud/posts.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = SNPosts.objects.all().order_by('-is_active')
        context['title'] = 'Список всех постов'
        return context


class SNPostUpdateView(AccessMixin, UpdateView):
    model = SNPosts
    template_name = 'adminapp/posts_crud/post_form.html'
    form_class = SNPostAdminForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование поста'
        return context


class SNPostDeleteView(AccessMixin, DeleteMixin, DeleteView):
    model = SNPosts
    template_name = 'adminapp/posts_crud/post_delete.html'

    def get_success_url(self):
        return reverse('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление поста'
        return context