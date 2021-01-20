import django_filters as filters
from django.db.models import Q

from .models import Test


class TestFilter(filters.FilterSet):
    is_passed = filters.BooleanFilter(
        field_name='results',
        label='Is passed',
        method='filter_passed'
    )
    name = filters.CharFilter(
        field_name='name',
        label='Search by name',
        method='search_by_name'
    )

    ordering = filters.OrderingFilter(
        fields=(
            ('created', 'created'),
        ),
        field_labels={
            'created': 'Date Created',
        }
    )

    def search_by_name(self, queryset, name, value):
        lookup = '__'.join([name, 'icontains'])
        return queryset.filter(**{lookup: value})

    def filter_passed(self, queryset, name, value):
        user = getattr(self.request, 'user', None)
        if user:
            if value is not None:
                lookup = '__'.join([name, 'user', 'exact'])
                if value:
                    return queryset.filter(**{lookup: user})
                else:
                    return queryset.filter(~Q(**{lookup: user}))
        return queryset


    class Meta:
        model = Test
        fields = ['is_passed', 'name']
