from rest_framework.exceptions import APIException


class ModerationError(APIException):
    status_code = 400
    default_detail = "Moderation error"
    default_code = "MOD_500"


class ModerationResubmitLimitExceededError(ModerationError):
    status_code = 400
    default_detail = "Maximum resubmission limit exceeded. Please contact support."
    default_code = "MOD_306"


ModerationResubmitLimitExceeded = ModerationResubmitLimitExceededError
