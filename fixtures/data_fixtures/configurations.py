"""Default configuration data. Reused by migrations and by tests.

Keep these values in sync with `apis/json_schemas.py`.
"""
from datetime import datetime, timezone
from uuid import uuid7

from cores.configs import cosmic_db_configs

CONFIG_NAME: str = "Default Configuration"


def configuration_rows() -> list[dict]:
    general = {
        "provider": "ollama",
        "model": "qwen2.5:7b",
        "is_quantised": False,
        "seed": 0,
        "default_knowledge_path": "/app/data/default/",
        "temp_knowledge_path": "/app/data/temp/",
        "api_key": cosmic_db_configs.get("OPENAI_API_KEY"),
    }

    return [
        {
            "id": uuid7(),
            "name": CONFIG_NAME,
            # The query analyser defaults to the same settings as general.
            "details": {
                "general": general,
                "query_analyser": dict(general),
            },
            "create_on": datetime.now(tz=timezone.utc),
        }
    ]
