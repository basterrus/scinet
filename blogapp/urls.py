from django.urls import path
from blogapp import views as blogapp

app_name = 'blogapp'


urlpatterns = [
    path('post_create/', blogapp.SNPostCreateView.as_view(), name='post_create'),
    path('post_read/<pk>/', blogapp.SNPostDetailView.as_view(), name='post_read'),
    path('post_update/<pk>/', blogapp.SNPostUpdateView.as_view(), name='post_update'),
    path('post_delete/<pk>/', blogapp.SNPostDeleteView.as_view(), name='post_delete'),
]

