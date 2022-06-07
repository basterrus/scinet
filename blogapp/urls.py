from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blogapp import views as blogapp

app_name = 'blogapp'


urlpatterns = [
    path('post_create/', blogapp.SNPostCreateView.as_view(), name='post_create'),
    path('post_read/<pk>/', blogapp.SNPostDetailView.as_view(), name='post_read'),
    path('post_update/<pk>/', blogapp.SNPostUpdateView.as_view(), name='post_update'),
    path('post_delete/<pk>/', blogapp.SNPostDeleteView.as_view(), name='post_delete'),
    path('comment_create/<post_pk>', blogapp.CommentCreateView.as_view(), name='comment_create'),
    path('comment_delete/<post_pk>/<pk>', blogapp.CommentDeleteView.as_view(), name='comment_delete'),
    path('comment_update/<post_pk>/<pk>', blogapp.CommentUpdateView.as_view(), name='comment_update'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


