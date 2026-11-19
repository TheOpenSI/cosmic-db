### Core modules ###
import sys
from pathlib import Path


### Internal modules ###
# NOTE:
# FastAPI CLI imports this repo as the `app` package and only puts this
# directory's parent on `sys.path`, while Alembic imports `apis` and `cores`
# as top-level packages. Adding the repo root keeps absolute imports working
# for both entry points without touching the relative imports.
sys.path.insert(0, str(Path(__file__).resolve().parent))
