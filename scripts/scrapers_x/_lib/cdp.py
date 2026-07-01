"""Chrome DevTools Protocol attach helpers for the X.com scraper.

We do NOT launch Chrome; the user keeps their own Chrome running with
``--remote-debugging-port=9228`` and the scraper attaches via
``playwright.chromium.connect_over_cdp``. Reusing the existing browser
is what inherits the X.com login session — we never see, store, or replay
cookies.

The two contracts enforced by this module:

1. Never tab-spam. We always reuse an existing x.com tab if one is open,
   and at most we will open ONE new tab in the user's browser.
2. Never block the user for long. Long waits use ``page.wait_for_timeout``
   with humane random delays.
"""

from __future__ import annotations

import contextlib
import logging
from typing import Iterator, Optional, Tuple

from playwright.sync_api import Browser, BrowserContext, Page

log = logging.getLogger("scrapers_x.cdp")

DEFAULT_CDP_URL = "http://localhost:9228"
X_HOST = "x.com"


class CDPError(RuntimeError):
    """Anything that goes wrong while attaching or picking a tab."""


def attach_chrome(cdp_url: str = DEFAULT_CDP_URL) -> Browser:
    try:
        from playwright.sync_api import sync_playwright as _sp
        p = _sp().__enter__()
    except Exception as e:
        raise CDPError(f"failed to start playwright: {e!r}") from e

    try:
        browser = p.chromium.connect_over_cdp(cdp_url)
    except Exception as e:
        with contextlib.suppress(Exception):
            p.stop()
        raise CDPError(
            f"cannot reach Chrome at {cdp_url}. "
            f"Relaunch Chrome with --remote-debugging-port=9228. Cause: {e!r}"
        ) from e

    browser._pw_handle = p  # type: ignore[attr-defined]
    log.info("attached to chrome at %s", cdp_url)
    return browser


def _stop(browser: Browser) -> None:
    pw = getattr(browser, "_pw_handle", None)
    if pw is not None:
        try:
            pw.stop()
        except Exception:
            pass


@contextlib.contextmanager
def scoped_chrome(cdp_url: str = DEFAULT_CDP_URL) -> Iterator[Browser]:
    browser = attach_chrome(cdp_url)
    try:
        yield browser
    finally:
        try:
            browser.close()
        except Exception:
            pass
        _stop(browser)


def _list_pages(browser: Browser) -> list[Page]:
    out: list[Page] = []
    for ctx in browser.contexts:
        out.extend(ctx.pages)
    return out


def find_x_page(browser: Browser) -> Optional[Page]:
    """The first open page whose URL contains x.com or twitter.com."""
    for page in _list_pages(browser):
        url = page.url or ""
        if X_HOST in url or "twitter.com" in url:
            return page
    return None


def open_or_reuse_x_page(
    browser: Browser, target_url: str
) -> Tuple[Page, bool]:
    existing = find_x_page(browser)
    if existing is not None:
        return existing, False

    contexts = browser.contexts
    if not contexts:
        raise CDPError(
            "Chrome has no default context. Close and relaunch Chrome with "
            "--remote-debugging-port=9228 --remote-allow-origins=*."
        )

    ctx: BrowserContext = contexts[0]
    page = ctx.new_page()
    page.goto(target_url, wait_until="domcontentloaded", timeout=30_000)
    return page, True


@contextlib.contextmanager
def x_page(
    target_url: str,
    cdp_url: str = DEFAULT_CDP_URL,
) -> Iterator[Tuple[Page, bool]]:
    with scoped_chrome(cdp_url) as browser:
        page, opened_new = open_or_reuse_x_page(browser, target_url)
        try:
            yield page, opened_new
        finally:
            if opened_new:
                with contextlib.suppress(Exception):
                    page.close()
