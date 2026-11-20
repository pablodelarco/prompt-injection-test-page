"""Fetch the test page through ScrapingBee in four output modes and save each response."""
import os
import pathlib

import requests
from dotenv import load_dotenv

load_dotenv()  # reads SCRAPINGBEE_API_KEY and TEST_PAGE_URL from .env

TEST_URL = os.environ["TEST_PAGE_URL"]  # the page you control, never a third-party site
OUT = pathlib.Path("outputs")
OUT.mkdir(exist_ok=True)

MODES = {
    "html_js": {"render_js": "true"},
    "html_nojs": {"render_js": "false"},
    "text": {"render_js": "true", "return_page_text": "true"},
    "markdown": {"render_js": "true", "return_page_markdown": "true"},
}

for name, extra in MODES.items():
    response = requests.get(
        "https://app.scrapingbee.com/api/v1/",
        headers={"Authorization": f"Bearer {os.environ['SCRAPINGBEE_API_KEY']}"},
        params={"url": TEST_URL, **extra},
        timeout=120,
    )
    response.raise_for_status()
    path = OUT / f"{name}.txt"
    path.write_text(response.text, encoding="utf-8")
    print(f"{name:<10} {response.status_code}  {len(response.text):>6} chars  -> {path}")
