# Database Migrations

Schema and seed data are versioned with [Alembic](https://alembic.sqlalchemy.org/). There are 2 independent environments:

| Config | Revisions | Version table | Purpose |
| --- | --- | --- | --- |
| `initial-alembic.ini` | `migrations/initial_versions/` | `alembic_version` | Schema + essential data |
| `demo-alembic.ini` | `migrations/demo_versions/` | `alembic_version_demo` | Optional demo/test data |

Run both from the `cosmic-db/` directory with the project's environment active.

## Initial (baseline) migrations

Revisions are intentionally small: one per table, then one per essential-data
fixture set. This keeps future schema changes isolated to a single revision.

1. Schema, in dependency order: `roles → users → user_identities → chatboxes → emissions → services → configurations`
2. Essential data, one revision per fixture: `roles → users → services → configurations`

```bash
# Linux/MacOS
.venv/bin/alembic -c initial-alembic.ini upgrade head    # create everything and seed essential data
.venv/bin/alembic -c initial-alembic.ini downgrade base  # drop everything
```
```ps1
# Windows
.venv/Scripts/alembic -c initial-alembic.ini upgrade head    # create everything and seed essential data
.venv/Scripts/alembic -c initial-alembic.ini downgrade base  # drop everything
```

Add a schema change as a new revision instead of editing existing ones:

```bash
# Linux/MacOS
.venv/bin/alembic -c initial-alembic.ini revision --autogenerate -m "add <thing>"
```
```ps1
# Windows
.venv/Scripts/alembic -c initial-alembic.ini revision --autogenerate -m "add <thing>"
```

## Fixtures

1. `fixtures/data_fixtures/`: essential data used by the pre-populate revisions (`roles.py`, `users.py`, `services.py`, `configurations.py`). Each module exposes row builders plus the natural keys used to revert its own rows.

2. `fixtures/test_fixtures/`: demo/test data (`emissions.py`, `chatboxes.py`).

## Demo/test data

Demo data lives in its own revision lineage and version table, so it never affects the baseline history. Apply the baseline first, then:

```bash
# Linux/MacOS
.venv/bin/alembic -c demo-alembic.ini upgrade head
```
```ps1
# Windows
.venv/Scripts/alembic -c demo-alembic.ini upgrade head
```

Tune the generated data with `-x` arguments (defaults shown):

```bash
# Linux/MacOS
.venv/bin/alembic -c demo-alembic.ini -x rows=50 -x users=1 \
  -x days-back=180 -x chatboxes=6 -x messages=10 upgrade head
```
```ps1
# Windows
.venv/Scripts/alembic -c demo-alembic.ini -x rows=50 -x users=1 \
  -x days-back=180 -x chatboxes=6 -x messages=10 upgrade head
```

| Option | Default | Meaning |
| --- | --- | --- |
| `rows` | `50` | Number of fake emissions rows |
| `users` | `1` | Number of existing users to spread data across |
| `days-back` | `180` | Timestamp spread for the dashboard charts |
| `chatboxes` | `6` | Number of fake chatbox sessions |
| `messages` | `10` | Chat history items per chatbox (with token counts) |

Revert demo data (clears the `emissions` and `chatboxes` tables entirely; this is intended for demo databases):

```bash
# Linux/MacOS
.venv/bin/alembic -c demo-alembic.ini downgrade base
```
```ps1
# Windows
.venv/Scripts/alembic -c demo-alembic.ini downgrade base
```
