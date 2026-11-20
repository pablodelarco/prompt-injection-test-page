"""Find which canary payloads are present in a piece of text."""
import html
import re

ZW = re.compile(r"[​-‍⁠﻿]")
CANARY = re.compile(r"CANARY-7F3A-(\d{2})")

TECHNIQUES = {
    "01": "display:none (inline)",
    "02": "visibility:hidden (inline)",
    "03": "hidden attribute",
    "04": 'aria-hidden="true"',
    "05": "HTML comment",
    "06": "white 1px text",
    "07": "off-screen position",
    "08": "zero-width characters",
    "09": "img alt attribute",
    "10": "title attribute",
    "11": "meta description",
    "12": "hidden by external CSS class",
    "13": "JS cloaking (automated browsers only)",
    "14": "visible text addressed to AI",
}


def found(text: str) -> set[str]:
    return set(CANARY.findall(ZW.sub("", html.unescape(text))))
