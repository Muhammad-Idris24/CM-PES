from .models import AuditLog


def write_audit(actor, action, entity, summary, request=None, metadata=None):
    ip_address = None
    if request is not None:
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        ip_address = forwarded_for.split(",")[0].strip() if forwarded_for else request.META.get("REMOTE_ADDR")
    return AuditLog.objects.create(
        actor=actor if getattr(actor, "is_authenticated", False) else None,
        action=action,
        entity_type=entity.__class__.__name__ if entity is not None else "System",
        entity_id=str(getattr(entity, "pk", "")),
        summary=summary,
        metadata=metadata or {},
        ip_address=ip_address,
    )
