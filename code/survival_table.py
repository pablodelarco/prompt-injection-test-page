"""Build the 'which payload survives which format' table from saved ScrapingBee outputs."""
import pathlib

from canaries import TECHNIQUES, found
from sanitize import strip_hidden

OUT = pathlib.Path("outputs")
raw = {m: (OUT / f"{m}.txt").read_text(encoding="utf-8") for m in ("html_nojs", "html_js", "text", "markdown")}
present = {m: found(t) for m, t in raw.items()}
stripped, flags = strip_hidden(raw["html_js"])
present["stripped"] = found(stripped)

cols = ["html_nojs", "html_js", "text", "markdown", "stripped"]
print("| # | Technique | " + " | ".join(cols) + " |")
print("|---|---|" + "---|" * len(cols))
for num, name in TECHNIQUES.items():
    cells = ["yes" if num in present[c] else "no" for c in cols]
    print(f"| {num} | {name} | " + " | ".join(cells) + " |")
print(f"\nStrip layer flagged {len(flags)} hidden snippets as instruction-like.")
