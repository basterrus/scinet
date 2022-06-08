from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.forms import SNUserLoginForm, SNUserRegisterForm, SNUserEditForm, SNUserProfileEditForm
from authapp.models import SNUser, SNUserProfile
from blogapp.models import SNPosts, SNSections, SNSubscribe
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


class SNPostDetailView(ListView):
    """Показывает все посты пользователя"""
    model = SNPosts
    template_name = 'authapp/user_auth/all_users_post.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class SNSectionsDetailView(ListView):
    """Показывает все разделы для подписки и отписки"""
    model = SNSections
    template_name = 'authapp/user_auth/section_subscribe.html'

    def get_queryset(self):
        return super().get_queryset()


def add_subscribe(request, pk):
    user = SNUser.objects.get(username=request.user)
    section = SNSections.objects.get(id=pk)
    if not SNSubscribe.objects.filter(Q(user=user) & Q(section=section)):
        subscribe = SNSubscribe(user=user, section=section)
        subscribe.save()
    return HttpResponseRedirect(reverse('authapp:section_subscribe'))


def del_subscribe(request, pk):
    user = SNUser.objects.get(username=request.user)
    section = SNSections.objects.get(id=pk)
    SNSubscribe.objects.filter(Q(user=user) & Q(section=section)).delete()
    return HttpResponseRedirect(reverse('authapp:section_subscribe'))
