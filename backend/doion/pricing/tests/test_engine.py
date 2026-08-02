"""Unit tests for pricing engine stub."""

from decimal import Decimal

from doion.pricing.engine import calculate_suggested_rate


class TestCalculateSuggestedRate:
    def test_long_due_date_is_low_risk(self):
        rate, risk = calculate_suggested_rate(face_amount=100_000_000, days_to_due=120)
        assert risk == "low"
        assert rate == Decimal("4.0")

    def test_medium_due_date_is_medium_risk(self):
        rate, risk = calculate_suggested_rate(face_amount=100_000_000, days_to_due=45)
        assert risk == "medium"
        assert rate == Decimal("6.0")

    def test_short_due_date_is_high_risk(self):
        rate, risk = calculate_suggested_rate(face_amount=100_000_000, days_to_due=10)
        assert risk == "high"
        assert rate == Decimal("8.0")

    def test_low_credit_score_adds_premium(self):
        rate, risk = calculate_suggested_rate(
            face_amount=100_000_000,
            days_to_due=45,
            issuer_credit_score=500,
        )
        assert risk == "medium"
        assert rate == Decimal("8.0")

    def test_good_credit_score_does_not_add_premium(self):
        rate, _ = calculate_suggested_rate(
            face_amount=100_000_000,
            days_to_due=45,
            issuer_credit_score=700,
        )
        assert rate == Decimal("6.0")
