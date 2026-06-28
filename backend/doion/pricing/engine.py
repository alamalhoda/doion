from decimal import Decimal


def calculate_suggested_rate(
    face_amount: int,
    days_to_due: int,
    issuer_credit_score: int | None = None,
) -> tuple[Decimal, str]:
    """Calculate suggested discount rate and risk tier (stub implementation)."""
    base_rate = Decimal("8.0")

    if days_to_due > 90:
        risk_tier = "low"
        rate = base_rate - Decimal("4.0")
    elif days_to_due > 30:
        risk_tier = "medium"
        rate = base_rate - Decimal("2.0")
    else:
        risk_tier = "high"
        rate = base_rate

    if issuer_credit_score is not None and issuer_credit_score < 600:
        rate += Decimal("2.0")

    return rate, risk_tier
