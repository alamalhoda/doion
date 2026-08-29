MAX_LISTING_RESUBMITS = 3


class RejectionCode:
    INCOMPLETE_INFO = "MOD_101"
    POOR_QUALITY_IMAGE = "MOD_102"
    INVALID_CHEQUE = "MOD_103"
    DUPLICATE_LISTING = "MOD_104"
    RISK_TOO_HIGH = "MOD_105"
    OTHER = "MOD_106"

    CHOICES = [
        (INCOMPLETE_INFO, "Incomplete information"),
        (POOR_QUALITY_IMAGE, "Poor quality image"),
        (INVALID_CHEQUE, "Invalid cheque"),
        (DUPLICATE_LISTING, "Duplicate listing"),
        (RISK_TOO_HIGH, "Risk too high"),
        (OTHER, "Other"),
    ]
