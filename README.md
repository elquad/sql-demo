## SQL-Demo: Tiny async PostgreSQL loader 

This repo contains a take-home project solution using the 2025 Python stack. 
The app ingests three public indicator of compromise (IOC) data sources and 
feeds them into a PostgreSQL database.

It’s deliberately small: no framework and no Alembic migration support, but
it is built from the packages used in real projects: psycopg3, async SQLAlchemy,
Pydantic, aiohttp, streaming, typed config, zero-dependency logging.

---

### What it does

| Feed                                      | Table | Validation                        | Insert strategy                   |
| ----------------------------------------- | ----- | --------------------------------- | --------------------------------- |
| **OpenPhish** <br>list of malicious URLs  | `url` | `UrlRow` (`HttpUrl`, enum source) | `INSERT … ON CONFLICT DO NOTHING` |
| **AlienVault** <br>reputation IPs         | `ip`  | `IpAddrRow` (`IPvAnyAddress`)     | same                              |
| **abuse.ch URLhaus** <br>malicious URLs   | `url` | `UrlRow`                          | same                              |

* Streaming download (`aiohttp`) → per-row Pydantic v2 validation → batch of 5000 rows → INSERT.
* Duplicate URLs/IPs are silently skipped by Postgres (`UNIQUE + ON CONFLICT DO NOTHING`), inserted row count is logged.

---

### Setup

```bash
# Create venv
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # sqlalchemy[asyncio] psycopg[binary] etc.

# Bootstrap database  (needs 'create' rights once)
export LOADER_DSN=postgresql://user:pw@localhost/demo
python -m loader init-db  # creates tables + pg_trgm extension

# Load the data
python -m loader
```

All settings can also live in a `.env` file:

```
LOADER_DSN=postgresql://user:pw@localhost/demo
LOADER_BATCH_SIZE=10000
```

