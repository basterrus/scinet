from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from authapp import views as authapp

app_name = 'authapp'


urlpatterns = [
    path('login/', authapp.LoginView.as_view(), name='login'),
    path('logout/', authapp.LogoutView.as_view(), name='logout'),
    path('register/', authapp.RegisterView.as_view(), name='register'),
    path('edit/', authapp.EditView.as_view(), name='edit'),
    path('profile/', authapp.EditView.as_view(), name='profile_user'),
    path('posts/', authapp.SNPostDetailView.as_view(), name='posts_user_list'),
    path('subscribe/', authapp.SNSectionsDetailView.as_view(), name='section_subscribe'),
    path('subscribe/add/<int:pk>/', authapp.add_subscribe, name='subscribe_add'),
    # path('api/user_create/', authapp.SNUserCreateAPIView.as_view(), name='api_user_create'),
    # path('api/user_update/<int:pk>/', authapp.SNUserUpdateAPIView.as_view(), name='api_user_update'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
