from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'


urlpatterns = [
    # path('', mainapp.SNPostsListView.as_view(), name='sections'),
    path('<int:pk>', mainapp.SNPostsListView.as_view(), name='section'),
    path('random', mainapp.RandomSNPostDetailView.as_view(), name='read_random'),
    path('read/<pk>/', mainapp.SNPostDetailView.as_view(), name='read'),
    # Это стоит вынести в отдельный модуль
    # path('create/', mainapp.SNPostCreateView.as_view(), name='create'),
    # path('update/<pk>/', mainapp.SNPostUpdateView.as_view(), name='update'),
    # path('delete/<pk>/', mainapp.SNPostDeleteView.as_view(), name='delete'),
]

