from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authapp.forms import SNUserLoginForm, SNUserRegisterForm, SNUserEditForm, SNUserProfileEditForm
from authapp.models import SNUser, SNUserProfile
from authapp.serializers import SNUserSerializer
from django.views.generic import View


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


class LoginView(View):
    """Страница логина"""
    model = SNUser
    template_name = 'authapp/user_auth/login.html'
    form_class = SNUserLoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form,
                                                            'title': 'Логин'})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class()
        return render(request, self.template_name, context={'form': form,
                                                            'title': 'Логин',
                                                            'error_text': 'Введён неправильный логин или пароль'})


class LogoutView(View):
    """View для логаута"""

    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(CreateView):
    """Страница регистрации пользователя"""
    model = SNUser
    template_name = 'authapp/user_auth/register.html'
    success_url = reverse_lazy('index')
    form_class = SNUserRegisterForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class EditView(View):
    """Страница редактирования профиля"""
    model = SNUser
    template_name = 'authapp/users_crud/user_form.html'
    form_class = SNUserEditForm
    success_url = reverse_lazy('authapp:users_list')

    def get(self, request):
        edit_form = SNUserEditForm(instance=self.request.user)
        edit_profile_form = SNUserProfileEditForm(instance=self.request.user.snuserprofile)
        context = {
            'title': 'Редактирование пользователя',
            'edit_form': edit_form,
            'edit_profile_form': edit_profile_form,
        }
        return render(self.request, 'authapp/user_auth/edit.html', context)

    def post(self, request, *args, **kwargs):
        edit_form = SNUserEditForm(request.POST, request.FILES, instance=request.user)
        edit_profile_form = SNUserProfileEditForm(request.POST, instance=request.user.snuserprofile)
        if edit_form.is_valid() and edit_profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))


"""CRUD для управления пользователями"""


class SNUserCreateView(AccessMixin, CreateView):
    model = SNUser
    template_name = 'authapp/users_crud/user_form.html'
    success_url = reverse_lazy('authapp:users_list')
    form_class = SNUserRegisterForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Создание пользователя'
        return context


class SNUserListView(AccessMixin, ListView):
    model = SNUser
    template_name = 'authapp/users_crud/users.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = SNUser.objects.all().order_by('-is_active')
        context['title'] = 'Список пользователей'
        return context


class SNUserUpdateView(AccessMixin, UpdateView):
    model = SNUser
    template_name = 'authapp/users_crud/user_form.html'
    form_class = SNUserEditForm
    success_url = reverse_lazy('authapp:users_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование пользователя'
        return context


class SNUserDeleteView(AccessMixin, DeleteMixin, DeleteView):
    model = SNUser
    template_name = 'authapp/users_crud/user_delete.html'

    def get_success_url(self):
        return reverse('authapp:users_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление пользователя'
        return context


class SNUserCreateAPIView(APIView):
    """API Создание пользователя"""

    def get(self, request):
        item = SNUser.objects.all()
        serializer = SNUserSerializer(item, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SNUserSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SNUserUpdateAPIView(APIView):
    """API Изменение пользователя"""

    def get_object(self, pk):
        try:
            return SNUser.objects.get(pk=pk)
        except SNUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = SNUserSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = SNUserSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
