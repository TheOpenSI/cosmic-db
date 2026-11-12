"""Essential user data. Reused by migrations and by tests."""
from collections.abc import Mapping
from datetime import datetime, timezone
from uuid import UUID, uuid7

ADMIN_EMAIL: str = "opensi@canberra.edu.au"


def user_rows(role_ids: Mapping[str, UUID]) -> list[dict]:
    return [
        {
            "id": uuid7(),
            "role_id": role_ids["admin"],
            "name": "cosmic",
            "email": ADMIN_EMAIL,
            "create_on": datetime.now(tz=timezone.utc),
        }
    ]
