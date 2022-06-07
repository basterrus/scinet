from django.urls import path
from authapp import views as authapp

app_name = 'authapp'


urlpatterns = [
    path('login/', authapp.LoginView.as_view(), name='login'),
    path('logout/', authapp.LogoutView.as_view(), name='logout'),
    path('register/', authapp.RegisterView.as_view(), name='register'),
    path('edit/', authapp.EditView.as_view(), name='edit'),
    path('users/', authapp.SNUserListView.as_view(), name='users_list'),
    path('user/create/', authapp.SNUserCreateView.as_view(), name='user_create'),
    path('user/update/<int:pk>/', authapp.SNUserUpdateView.as_view(),
         name='user_update'),
    path('user/delete/<int:pk>/', authapp.SNUserDeleteView.as_view(),
         name='user_delete'),
    path('profile/', authapp.EditView.as_view(), name='profile_user'),
    path('posts/', authapp.SNPostDetailView.as_view(), name='posts_user_list'),
    path('subscribe/', authapp.SNSectionsDetailView.as_view(), name='section_subscribe'),
    # path('api/user_create/', authapp.SNUserCreateAPIView.as_view(), name='api_user_create'),
    # path('api/user_update/<int:pk>/', authapp.SNUserUpdateAPIView.as_view(), name='api_user_update'),
]

