"""Layer 5 (Pin): record where every document came from before it is indexed."""
import hashlib
import json
import pathlib
from datetime import datetime, timezone

from sanitize import strip_hidden

STORE = pathlib.Path("provenance.jsonl")


def pin(url: str, raw_html: str) -> dict:
    text, flags = strip_hidden(raw_html)
    record = {
        "url": url,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(raw_html.encode("utf-8")).hexdigest(),
        "flag_count": len(flags),
        "text": text,
    }
    with STORE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return record


def last_record(url: str) -> dict | None:
    if not STORE.exists():
        return None
    records = [json.loads(line) for line in STORE.read_text(encoding="utf-8").splitlines()]
    matches = [r for r in records if r["url"] == url]
    return matches[-1] if matches else None


def needs_review(url: str, raw_html: str) -> bool:
    """True when the page changed since the last pin (possible split-view poisoning)."""
    previous = last_record(url)
    new_hash = hashlib.sha256(raw_html.encode("utf-8")).hexdigest()
    return previous is not None and previous["sha256"] != new_hash
