from django.contrib import auth
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.forms import SNUserLoginForm, SNUserRegisterForm, SNUserEditForm, SNUserProfileEditForm
from authapp.models import SNUser
from authapp.serializers import SNUserSerializer


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
