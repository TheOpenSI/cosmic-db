"""Essential role data. Reused by migrations and by tests."""
from datetime import datetime, timezone
from uuid import uuid7

ROLES: list[dict] = [
    {
        "name": "admin",
        "desc": (
            "Has full administrative rights to configure CoSMIC, including "
            "selecting and managing models, adjusting RAG thresholds, and "
            "enabling or disabling available services."
        ),
    },
    {
        "name": "user",
        "desc": "Can use CoSMIC but cannot change its configuration",
    },
]

ROLE_NAMES: tuple[str, ...] = tuple(role["name"] for role in ROLES)


def role_rows() -> list[dict]:
    create_on = datetime.now(tz=timezone.utc)
    return [
        {"id": uuid7(), **role, "create_on": create_on}
        for role in ROLES
    ]
