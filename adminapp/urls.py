from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from adminapp import views as adminapp

app_name = 'adminapp'


urlpatterns = [
    path('users/', adminapp.SNUserListView.as_view(), name='users_list'),
    path('user/create/', adminapp.SNUserCreateView.as_view(), name='user_create'),
    path('user/update/<int:pk>/', adminapp.SNUserUpdateView.as_view(),
         name='user_update'),
    path('user/delete/<int:pk>/', adminapp.SNUserDeleteView.as_view(),
         name='user_delete'),
    path('posts/', adminapp.SNPostsListView.as_view(), name='posts_list'),
    path('post/create/', adminapp.SNPostCreateView.as_view(), name='post_create'),
    path('post/update/<int:pk>/', adminapp.SNPostUpdateView.as_view(),
         name='post_update'),
    path('post/delete/<int:pk>/', adminapp.SNPostDeleteView.as_view(),
         name='post_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
