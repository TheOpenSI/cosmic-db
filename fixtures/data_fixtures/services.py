"""Essential service data. Reused by migrations and by tests."""
from datetime import datetime, timezone

SERVICES: list[dict] = [
    {
        "name": "chess",
        "desc": (
            "If it is a chess game, predict the next chess move by providing "
            "a sequence of moves or a FEN."
        ),
        "status": True,
        "memory_capability": False,
    },
    {
        "name": "memory",
        "desc": (
            "Update the vector database with a declarative sentence (not a "
            "question), or a PDF document."
        ),
        "status": True,
        "memory_capability": True,
    },
    {
        "name": "code_generation",
        "desc": (
            "Generate or improve a code or answer a question in order to "
            "generate or improve a code."
        ),
        "status": True,
        "memory_capability": False,
    },
    {
        "name": "general_question_answering",
        "desc": (
            "Answer a question or provide a reasoning, which cannot be "
            "achieved by the other services."
        ),
        "status": True,
        "memory_capability": False,
    },
    {
        "name": "academic_governance",
        "desc": "Answer question about Academic Governance.",
        "status": True,
        "memory_capability": True,
    },
]

SERVICE_NAMES: tuple[str, ...] = tuple(
    service["name"] for service in SERVICES
)


def service_rows() -> list[dict]:
    create_on = datetime.now(tz=timezone.utc)
    return [
        {"create_on": create_on, **service}
        for service in SERVICES
    ]
