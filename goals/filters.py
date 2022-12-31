from django.db.models import DateTimeField
from django_filters import IsoDateTimeFilter, rest_framework

from goals.models import Goal


class GoalDateFilter(rest_framework.FilterSet):
    class Meta:
        model = Goal
        fields = {'category': ['exact', 'in'],
                  'priority': ['exact', 'in'],
                  'due_date': ['lte', 'gte'],
                  'status': ['exact', 'in']}
        filter_overrides = {
            DateTimeField: {'filter_class': IsoDateTimeFilter},
        }
