"""Cheque / issuer factories for tests and demo seeding."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from doion.checks.models import ChequeListing
from doion.checks.models import IssuerProfile
from doion.users.factories import UserFactory


class IssuerProfileFactory(DjangoModelFactory):
    class Meta:
        model = IssuerProfile

    national_or_company_id = factory.Sequence(lambda n: f"{1000000000 + n}")
    name = factory.Sequence(lambda n: f"Issuer {n}")
    credit_score = 700


class ChequeListingFactory(DjangoModelFactory):
    class Meta:
        model = ChequeListing

    owner = factory.SubFactory(UserFactory)
    issuer = factory.SubFactory(IssuerProfileFactory)
    bank_name = "بانک ملت"
    cheque_serial_number = factory.Sequence(lambda n: f"{1000000000000000 + n}")
    face_amount = Decimal("100000000")
    due_date = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=30))
    issuer_type = ChequeListing.IssuerType.LEGAL
    issuer_name = factory.LazyAttribute(lambda o: o.issuer.name)
    issuer_national_id = factory.LazyAttribute(lambda o: o.issuer.national_or_company_id)
    description = ""
    suggested_discount_rate = Decimal("5.00")
    risk_tier = "medium"
    status = ChequeListing.Status.PENDING_MODERATION

    class Params:
        published = factory.Trait(
            status=ChequeListing.Status.PUBLISHED,
            risk_tier="low",
            suggested_discount_rate=Decimal("3.50"),
        )
        pending = factory.Trait(status=ChequeListing.Status.PENDING_MODERATION)
        rejected = factory.Trait(
            status=ChequeListing.Status.REJECTED,
            rejection_code="MOD_101",
            rejection_reason="Incomplete information",
        )
        matched = factory.Trait(status=ChequeListing.Status.MATCHED)
        expired = factory.Trait(
            status=ChequeListing.Status.EXPIRED,
            due_date=factory.LazyFunction(lambda: timezone.now().date() - timedelta(days=1)),
        )
        high_risk = factory.Trait(risk_tier="high", suggested_discount_rate=Decimal("10.00"))
