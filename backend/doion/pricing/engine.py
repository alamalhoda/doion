from decimal import Decimal

LOW_RISK_DAYS_THRESHOLD = 90
MEDIUM_RISK_DAYS_THRESHOLD = 30
LOW_CREDIT_SCORE_THRESHOLD = 600


def calculate_suggested_rate(
    face_amount: int,
    days_to_due: int,
    issuer_credit_score: int | None = None,
) -> tuple[Decimal, str]:
    """Calculate suggested discount rate and risk tier (stub implementation)."""
    base_rate = Decimal("8.0")

    if days_to_due > LOW_RISK_DAYS_THRESHOLD:
        risk_tier = "low"
        rate = base_rate - Decimal("4.0")
    elif days_to_due > MEDIUM_RISK_DAYS_THRESHOLD:
        risk_tier = "medium"
        rate = base_rate - Decimal("2.0")
    else:
        risk_tier = "high"
        rate = base_rate

    if issuer_credit_score is not None and issuer_credit_score < LOW_CREDIT_SCORE_THRESHOLD:
        rate += Decimal("2.0")

    return rate, risk_tier
