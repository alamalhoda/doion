"""Bank catalog API serializers."""

from __future__ import annotations

from rest_framework import serializers

from doion.banks.models import Bank


def build_logo_url(bank: Bank, request) -> str | None:
    if not bank.logo:
        return None
    url = bank.logo.url
    if request is not None:
        return request.build_absolute_uri(url)
    return url


class BankSummarySerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Bank
        fields = [
            "code",
            "display_name",
            "logo_url",
            "brand_color_light",
            "brand_color_dark",
        ]

    def get_logo_url(self, obj: Bank) -> str | None:
        return build_logo_url(obj, self.context.get("request"))


class BankSerializer(BankSummarySerializer):
    class Meta(BankSummarySerializer.Meta):
        fields = [
            *BankSummarySerializer.Meta.fields,
            "aliases",
        ]
