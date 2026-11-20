"""Layer 1 (Strip): remove content a human never sees and flag instruction-like text."""
import re

from bs4 import BeautifulSoup, Comment

ZERO_WIDTH = re.compile(r"[\u200b-\u200d\u2060\ufeff]")
HIDDEN_STYLE = re.compile(
    r"display\s*:\s*none|visibility\s*:\s*hidden|font-size\s*:\s*[01]px"
    r"|left\s*:\s*-\d{3,}px|color\s*:\s*(#fff\b|#ffffff|white)",
    re.I,
)
SUSPICIOUS = re.compile(
    r"ignore (all )?previous|system override|you are now|instruction|"
    r"\bassistant\b|language model|\bai (agent|model|assistant)s?\b|send_email",
    re.I,
)


def strip_hidden(html: str) -> tuple[str, list[str]]:
    """Return visible text and the hidden snippets that looked like instructions."""
    soup = BeautifulSoup(html, "lxml")
    removed: list[str] = []

    for node in soup.find_all(string=lambda s: isinstance(s, Comment)):
        removed.append(str(node))
        node.extract()
    for tag in soup(["script", "style", "noscript", "template", "head"]):
        tag.decompose()
    for tag in soup.find_all(True):
        if tag.decomposed:
            continue
        if (
            tag.has_attr("hidden")
            or tag.get("aria-hidden") == "true"
            or HIDDEN_STYLE.search(tag.get("style", ""))
        ):
            removed.append(tag.get_text(" ", strip=True))
            tag.decompose()
    for tag in soup.find_all(True):
        if tag.decomposed:
            continue
        for attr in ("alt", "title"):  # attributes models often see in HTML or markdown
            if tag.has_attr(attr):
                removed.append(tag[attr])
                del tag[attr]

    text = soup.get_text("\n", strip=True)
    text = ZERO_WIDTH.sub("", text)
    flags = [s for s in removed if SUSPICIOUS.search(ZERO_WIDTH.sub("", s))]
    return text, flags


def flag_text(text: str) -> list[str]:
    """Flag instruction-like lines in text that has no markup (text or markdown output)."""
    clean = ZERO_WIDTH.sub("", text)
    return [line for line in clean.splitlines() if SUSPICIOUS.search(line)]
