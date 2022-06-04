from blogapp.forms import SNPostForm
from blogapp.models import SNPosts
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from blogapp.models import SNPosts


class SNPostDetailView(DetailView):
    model = SNPosts
    template_name = 'blogapp/post_crud/post_detail.html'


class SNPostCreateView(CreateView):
    model = SNPosts
    template_name = 'blogapp/post_crud/post_detail.html'
    success_url = reverse_lazy('index')
    form_class = SNPostForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Создание поста'
        return context


class SNPostUpdateView(UpdateView):
    pass


class SNPostDeleteView(DeleteView):
    pass


