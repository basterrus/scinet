from django.urls import path
from authapp import views as authapp
from usersapp import views as usersapp
app_name = 'usersapp'


urlpatterns = [
    path('profile/', authapp.EditView.as_view(), name='profile_user'),
    path('posts/', usersapp.SNPostDetailView.as_view(), name='posts_user_list'),
    # path('post_read/<pk>/', blogapp.SNPostDetailView.as_view(), name='post_read'),
    # path('post_update/<pk>/', blogapp.SNPostUpdateView.as_view(), name='post_update'),
    # path('post_delete/<pk>/', blogapp.SNPostDeleteView.as_view(), name='post_delete'),
]

