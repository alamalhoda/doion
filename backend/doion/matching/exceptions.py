from rest_framework.exceptions import APIException


class MatchNotAllowed(APIException):
    status_code = 400
    default_detail = "You are not allowed to perform this action"
    default_code = "MATCH_NOT_ALLOWED"


class InvalidMatchStatus(APIException):
    status_code = 400
    default_detail = "Invalid match status for this action"
    default_code = "INVALID_MATCH_STATUS"
