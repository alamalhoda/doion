from datetime import date
from datetime import timedelta

import django_filters
from django.db.models import Q

from doion.checks.models import ChequeListing


class MarketplaceFilter(django_filters.FilterSet):
    risk_tier = django_filters.ChoiceFilter(choices=ChequeListing._meta.get_field("risk_tier").choices)
    issuer_type = django_filters.ChoiceFilter(choices=ChequeListing.IssuerType.choices)
    min_amount = django_filters.NumberFilter(field_name="face_amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="face_amount", lookup_expr="lte")
    max_days_to_due = django_filters.NumberFilter(method="filter_max_days_to_due")
    bank = django_filters.CharFilter(field_name="bank__code", lookup_expr="exact")
    bank_name = django_filters.CharFilter(method="filter_bank_name")

    class Meta:
        model = ChequeListing
        fields = ["risk_tier", "issuer_type", "bank", "bank_name"]

    def filter_max_days_to_due(self, queryset, name, value):
        today = date.today()
        max_due_date = today + timedelta(days=int(value))
        return queryset.filter(due_date__lte=max_due_date)

    def filter_bank_name(self, queryset, _name, value):
        if self.data.get("bank"):
            return queryset
        return queryset.filter(
            Q(bank_name__icontains=value)
            | Q(bank__display_name__icontains=value)
            | Q(bank__aliases__icontains=value),
        )
