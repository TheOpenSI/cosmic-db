"""Fake chatbox sessions (chat history, token counts) for dashboard demos and tests."""
from collections.abc import Sequence
from datetime import datetime, timedelta, timezone
from random import choice, randint
from uuid import UUID, uuid7

CHATBOX_NAMES: list[str] = [
    "Carbon footprint",
    "Scope 3 questions",
    "Model comparison",
    "Energy report",
    "Research session",
    "Weekly review",
]

CHAT_TURNS: list[tuple[str, str]] = [
    (
        "What is my carbon footprint this month?",
        "Your recent compute sessions produced a small amount of CO2. Check the dashboard trend for the exact kg value.",
    ),
    (
        "How many tokens did the last query use?",
        "Token counts are stored per inquiry in the chat history. Input tokens are usually larger than output tokens.",
    ),
    (
        "Compare CPU and GPU power for my last run.",
        "CPU and GPU power are recorded per emissions row. GPU may be zero if the run had no GPU.",
    ),
    (
        "Show a 6 month emissions trend.",
        "Use the dashboard 6M range. Months with no rows appear as gaps rather than zeros.",
    ),
    (
        "What region is the grid intensity based on?",
        "Seeded rows use Australian regions. Intensity is an approximation for local testing only.",
    ),
]


def _random_backdated_timestamp(days_back: int) -> datetime:
    """Random timestamp within the last `days_back` days, timezone-aware UTC."""
    now = datetime.now(tz=timezone.utc)
    delta_seconds = randint(0, days_back * 24 * 60 * 60)
    return now - timedelta(seconds=delta_seconds)


def _build_history(query_at: datetime) -> dict:
    user_query, llm_response = choice(CHAT_TURNS)
    respond_at = query_at + timedelta(seconds=randint(2, 30))

    return {
        "inquiry_cycle_id": str(uuid7()),
        "user_role": "user",
        "user_query": user_query,
        "query_create_on": query_at.isoformat(),
        "llm_role": "assistant",
        "llm_response": llm_response,
        "response_create_on": respond_at.isoformat(),
        "input_token": randint(120, 2500),
        "output_token": randint(20, 400),
    }


def _build_chatbox(
    user_id: UUID,
    days_back: int,
    num_messages: int,
    index: int,
) -> dict:
    timestamps = sorted(
        _random_backdated_timestamp(days_back) for _ in range(num_messages)
    )
    details = [_build_history(query_at) for query_at in timestamps]
    create_on = timestamps[0] - timedelta(seconds=randint(1, 60))

    return {
        "id": uuid7(),
        "user_id": user_id,
        "name": f"{choice(CHATBOX_NAMES)} {index + 1}",
        "details": details,
        "create_on": create_on,
    }


def build_chatbox_rows(
    user_ids: Sequence[UUID],
    num_chatboxes: int,
    num_messages: int,
    days_back: int,
) -> list[dict]:
    return [
        _build_chatbox(
            user_id=choice(user_ids),
            days_back=days_back,
            num_messages=num_messages,
            index=i,
        )
        for i in range(num_chatboxes)
    ]
