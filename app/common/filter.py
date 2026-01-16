from datetime import datetime, time

import django_filters


class DateFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="created_at", method="filter_end")

    def __init__(self, start_field="created_at", end_field="created_at", **kwargs):
        super().__init__(**kwargs)
        self.start_date = django_filters.DateTimeFilter(field_name=start_field, lookup_expr="gte")
        self.end_date = django_filters.DateTimeFilter(field_name=end_field, method="filter_end")

    @staticmethod
    def filter_end(queryset, name, value):
        end_date = datetime.combine(value, time.max)
        f = {f"{name}__lte": end_date}
        return queryset.filter(**f)
