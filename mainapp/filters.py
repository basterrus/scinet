import django_filters

from blogapp.models import SNPosts


class PostsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = SNPosts
        fields = ['name']
