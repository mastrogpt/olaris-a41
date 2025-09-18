# Coding Task — Serverless REST Backend (Python)

## Context
You’re in a serverless environment. The app’s frontend (generated with Lovable) lives in the same site and **must not be modified**. Each backend **action** is an **independent, stateless, horizontally scalable** function exposed as a REST endpoint. **No shared code** between actions.

---

## Goals
- Implement the backend **REST actions** in Python only.
- Do **not** touch the frontend.
- Scope your changes to **`packages/*`** and **`tests/*`** only.

---

## Runtime Model
- Each action has a **`<package>`** and **`<name>`**.
- Deployed actions are reachable at:
  ```
  /api/my/<package>/<name>
  ```
- Each action exposes a `main(args: dict) -> dict` entrypoint.
  - Input: a **JSON object**.
  - Output: a **JSON object**.  
    (Never return arrays or primitives.)

- Create a new action:
  ```
  ops lv new <action> <package>
  ```

- File layout for an action:
  ```
  packages/<package>/<name>/__main__.py
  packages/<package>/<name>/<name>.py
  ```

- Put **all business logic** in `<name>.py`.  
  `__main__.py` is just a thin adapter plus annotations.

---

## Action Templates (copy/paste)

### `packages/<package>/<name>/__main__.py`
```python
#-- action metadata / params go here (see Secrets/Services below)
#-- Always keep these as comments prefixed with `#--`

import json
from . import <name>  # the module with your logic

def main(args):
    """
    Serverless entrypoint.
    Receives a dict `args` (parsed from the request).
    Must return a dict (JSON object).
    """
    # Validate input is a dict
    if not isinstance(args, dict):
        return {"error": "Invalid input, expected JSON object"}

    # Delegate to your action’s main and wrap in {"body": ...}
    try:
        payload = <name>.<name>(args)
        if not isinstance(payload, dict):
            return {"error": "Action returned non-object JSON"}
        return {"body": payload}
    except Exception as e:
        # Prefer structured, stable error surface
        return {"error": str(e)}
```

### `packages/<package>/<name>/<name>.py`
```python
import os
from typing import Dict, Any

def <name>(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Business logic. Return a JSON object (dict).
    """
    # example: echo back something
    user = args.get("user", "anonymous")
    return {"ok": True, "user": user}
```

**Rules:**
- **Never** put business code in `__main__.py`.  
- **Always** keep the adapter shape: `return {"body": <name>.<name>(args)}` (and ensure it’s a dict).

---

## Secrets
When you need a secret:
1. **Ask** to add it to `.env`. Do **not** add it yourself.
2. In `__main__.py`, add:
   ```
   #--param <SECRET> "$<SECRET>"
   ```
3. In your action (in `<name>.py`), read it with fallback:
   ```python
   import os
   SECRET = args.get("<SECRET>", os.getenv("<SECRET>"))
   ```
   *(fixed parentheses; previous version was missing a `)`)*

---

## Deployment
- Log in to the environment:
  ```
  ops ide login
  ```
- Deploy one action:
  ```
  ops ide deploy <package>/<name>
  ```
- Deploy all:
  ```
  ops ide deploy
  ```

---

## Services & Annotations

Add **only** these `#--param` lines to `__main__.py` when you actually use the service.

### Redis
```
#--param REDIS_URL $REDIS_URL
#--param REDIS_PREFIX $REDIS_PREFIX
```

**Snippet (fixes included):**
```python
# in <name>.py
import os
import redis  # see Libraries note below

def <name>(args):
    url = args.get("REDIS_URL", os.getenv("REDIS_URL"))
    prefix = args.get("REDIS_PREFIX", os.getenv("REDIS_PREFIX"))
    r = redis.from_url(url)
    # Always namespace keys with `prefix`
    key = f"{prefix}:example"
    r.set(key, "value")
    return {"ok": True}
```

### PostgreSQL
```
#--param POSTGRES_URL "$POSTGRES_URL"
```

**Snippet:**
```python
# in <name>.py
import os

def <name>(args):
    dburl = args.get("POSTGRES_URL", os.getenv("POSTGRES_URL"))
    # use your preferred client; see Libraries note
    return {"dburl_present": bool(dburl)}
```

### S3 (e.g., MinIO)
```
#--param S3_HOST $S3_HOST
#--param S3_PORT $S3_PORT
#--param S3_ACCESS_KEY $S3_ACCESS_KEY
#--param S3_SECRET_KEY $S3_SECRET_KEY
#--param S3_BUCKET_DATA $S3_BUCKET_DATA
```

**Snippet (fixes included):**
```python
# in <name>.py
import os
import boto3  # see Libraries note below

def <name>(args):
    host = args.get("S3_HOST", os.getenv("S3_HOST"))
    port = args.get("S3_PORT", os.getenv("S3_PORT"))
    url = f"http://{host}:{port}"
    key = args.get("S3_ACCESS_KEY", os.getenv("S3_ACCESS_KEY"))
    sec = args.get("S3_SECRET_KEY", os.getenv("S3_SECRET_KEY"))
    bucket = args.get("S3_BUCKET_DATA", os.getenv("S3_BUCKET_DATA"))

    s3 = boto3.client(
        "s3",
        region_name="us-east-1",
        endpoint_url=url,
        aws_access_key_id=key,
        aws_secret_access_key=sec,
    )
    # s3.put_object(Bucket=bucket, Key="example.json", Body=b'{}')
    return {"bucket": bucket}
```

### Milvus
```
#--param MILVUS_HOST $MILVUS_HOST
#--param MILVUS_PORT $MILVUS_PORT
#--param MILVUS_DB_NAME $MILVUS_DB_NAME
#--param MILVUS_TOKEN $MILVUS_TOKEN
```

**Snippet (fixes included):**
```python
# in <name>.py
import os
from pymilvus import MilvusClient  # see Libraries note below

def <name>(args):
    host = args.get("MILVUS_HOST", os.getenv("MILVUS_HOST"))
    port = args.get("MILVUS_PORT", os.getenv("MILVUS_PORT"))
    token = args.get("MILVUS_TOKEN", os.getenv("MILVUS_TOKEN"))
    db_name = args.get("MILVUS_DB_NAME", os.getenv("MILVUS_DB_NAME"))

    uri = f"http://{host}:{port}"
    client = MilvusClient(uri=uri, token=token, db_name=db_name)
    # client.create_collection(...)  # example
    return {"milvus_db": db_name}
```

---

## Testing Layout
- **Unit tests**: `tests/<package>/test_<name>.py`
- **Integration tests**: `tests/<package>/test_<name>_int.py`

Recommended unit test shape (pytest):
```python
from packages.<package>.<name> import <name>

def test_<name>_ok():
    out = <name>({"user": "alice"})
    assert out["ok"] is True
```

---

## Important Constraints & Clarifications

1. **Only Python code** for backend actions. (✅)
2. **Scope**: work inside `packages/*` and `tests/*`. Ignore other folders. (✅)
3. **Libraries contradiction (please resolve):**  
   Your brief bans `pip` and limits libraries to:
   ```
   requests
   openai
   ```
   …but your service snippets require **`redis`**, **`boto3`**, and **`pymilvus`** (and likely a Postgres client such as **`psycopg`**).

   **You must pick one of these options:**
   - **Option A (recommended):** Extend the allowed libraries to include:
     ```
     redis
     boto3
     pymilvus
     psycopg[binary]  (or psycopg2-binary)
     ```
     *(and ensure they’re available in the runtime; we won’t add requirements.txt)*
   - **Option B:** Provide HTTP or SDK-free alternatives that work with **only `requests`** (e.g., a REST proxy for Redis/S3/Milvus/Postgres). If you choose this, please also document the endpoints and auth scheme.

4. **Return shape:** Always return **objects**. If you need to return a list, wrap it (e.g., `{"items": [...]}`).

5. **Consistency fixes applied:**
   - Typos: “frontent” → **frontend**.
   - `return {"body": <action>.<action>(args)}` → ensure valid Python, no backticks, balanced braces.
   - Redis snippet fixed (single `from_url` arg; correct `prefix` line).
   - Milvus snippet now uses **`MILVUS_PORT`**.
   - Secrets retrieval fixed (missing `)`).

6. **CORS:** Endpoints are same-origin (`/api/my/...`) with the frontend, so CORS shouldn’t be required. If you later expose cross-origin, add CORS headers in your adapter.

7. **Error handling:** Catch exceptions in `__main__.py` and return a stable error object:
   ```python
   return {"error": "message", "code": "INTERNAL"}
   ```

8. **Idempotency & side effects:** Prefer idempotent semantics for GET-like operations. For mutations, validate inputs and return deterministic objects.

---

## Quick Checklist (per action)
- [ ] Created with `ops lv new <action> <package>`.
- [ ] `__main__.py` contains only adapter + `#--param` annotations.
- [ ] All logic in `<name>.py`, function `<name>(args) -> dict`.
- [ ] Input validated; output is a **dict**.
- [ ] Secrets declared via `#--param` and read via args/env.
- [ ] Service usage guarded (only if params provided).
- [ ] Tests in `tests/<package>/...` pass.
- [ ] Deployed with `ops ide deploy <package>/<name>` (or all).
