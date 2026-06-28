from datetime import date
from datetime import timedelta

import django_filters

from doion.checks.models import ChequeListing


class MarketplaceFilter(django_filters.FilterSet):
    risk_tier = django_filters.ChoiceFilter(choices=ChequeListing._meta.get_field("risk_tier").choices)
    issuer_type = django_filters.ChoiceFilter(choices=ChequeListing.IssuerType.choices)
    min_amount = django_filters.NumberFilter(field_name="face_amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="face_amount", lookup_expr="lte")
    max_days_to_due = django_filters.NumberFilter(method="filter_max_days_to_due")
    bank_name = django_filters.CharFilter(field_name="bank_name", lookup_expr="icontains")

    class Meta:
        model = ChequeListing
        fields = ["risk_tier", "issuer_type", "bank_name"]

    def filter_max_days_to_due(self, queryset, name, value):
        today = date.today()
        max_due_date = today + timedelta(days=int(value))
        return queryset.filter(due_date__lte=max_due_date)
