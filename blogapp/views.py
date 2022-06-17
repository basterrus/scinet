from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from adminapp.views import AccessMixin, DeleteMixin
from blogapp.forms import SNPostForm, CommentForm
from blogapp.models import SNPosts, Comments, LikeDislike

import json
from django.http import HttpResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType


class SNPostDetailView(DetailView):
    """Показывает пост"""
    model = SNPosts
    template_name = 'blogapp/post_crud/post_view.html'
    form_class = CommentForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        context['post'] = SNPosts.objects.get(pk=self.kwargs['pk'])
        context['comments'] = Comments.objects.filter(is_active=True, post__pk=self.kwargs['pk'])
        context['title'] = 'Пост'
        return context

    def get_success_url(self):
        return reverse('blogs:post_read', args=[self.kwargs['pk']])

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = self.form_class(request.POST)
            if form.is_valid():
                comment = form.save(
                    commit=False)
                comment.user = request.user
                comment.post = SNPosts.objects.get(pk=self.kwargs['pk'])
                comment.save()
                return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class SNPostCreateView(CreateView):
    """Создание поста"""
    model = SNPosts
    template_name = 'blogapp/post_crud/post_form.html'
    success_url = reverse_lazy('index')
    form_class = SNPostForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
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


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class CommentCreateView(CreateView):
    """Создание комментария"""
    model = Comments
    template_name = 'blogapp/comment_crud/comment_create.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blogs:post_read', args=[self.kwargs['post_pk']])

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = self.form_class(request.POST)
            if form.is_valid():
                post_pk = self.kwargs['post_pk']
                comment = form.save(
                    commit=False)
                comment.user = request.user
                comment.post = SNPosts.objects.get(pk=post_pk)
                comment.save()
                return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class CommentUpdateView(UpdateView):
    """Редактирование комментария"""
    model = Comments
    template_name = 'blogapp/comment_crud/comment_create.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blogs:post_read', args=[self.kwargs['post_pk']])


@method_decorator(login_required, name='dispatch')
class CommentDeleteView(DeleteView):
    """Удаление комментария"""
    model = Comments
    template_name = 'blogapp/comment_crud/comment_delete.html'

    def get_success_url(self):
        return reverse('blogs:post_read', args=[self.kwargs['post_pk']])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class VotesView(View):
    """Лайки"""
    model = None
    """Модель данных (лайк статьи или комментария)"""
    vote_type = None
    """Like or dislike"""

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        print(f'11111111111111111111111111111111111')
        """GenericForeignKey не поддерживает метод get_or_create"""
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )
