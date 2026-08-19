from doion.compliance.models import AuditEvent


def audit_event(  # noqa: PLR0913
    event_type,
    actor=None,
    object_type=None,
    object_id=None,
    metadata=None,
    request=None,
):
    ip_address = ""
    if request:
        ip_address = request.META.get("REMOTE_ADDR", "")

    AuditEvent.objects.create(
        actor=actor,
        event_type=event_type,
        object_type=object_type or "",
        object_id=object_id or "",
        metadata=metadata or {},
        ip_address=ip_address,
    )
