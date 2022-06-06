from django.http import HttpResponseRedirect
from blogapp.forms import SNPostForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from blogapp.models import SNPosts, SNSections


class SNPostDetailView(ListView):
    """Показывает все посты пользователя"""
    model = SNPosts
    template_name = 'usersapp/all_users_post.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
