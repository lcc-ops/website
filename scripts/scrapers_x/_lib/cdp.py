"""Chrome lifecycle for the X.com scraper.

Mirrors multi_publisher/src/multi_publisher/profile/launcher.py:

* If CDP is not reachable on 9228, launch a headless Chrome with the
  persistent profile (multi_publisher/profiles/profile-9228/Default) and
  the full headless flag set verified against Chrome 149.
* If CDP is already up (user keeps the port alive in the system tray),
  attach to it without spawning a new Chrome.
* On context exit, kill the Chrome we spawned (if any). User-owned Chrome
  is left alone.
"""

from __future__ import annotations

import contextlib
import json
import logging
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterator, Optional, Tuple

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

log = logging.getLogger("scrapers_x.cdp")

# Profile parent dir. Note: the proxy.json sits NEXT TO Default/, not inside
# it — that's the path multi_publisher uses (`profile-<port>/proxy.json`,
# not `profile-<port>/Default/proxy.json`).
PROFILE_PARENT: Path = Path(
    r"D:\LocalSystem\Code\ai_dev\multi_publisher\profiles\profile-9228"
)
PROFILE_DIR: Path = PROFILE_PARENT / "Default"
PROXY_CONFIG_PATH: Path = PROFILE_PARENT / "proxy.json"
DEFAULT_CDP_URL = "http://localhost:9228"
X_HOST = "x.com"

# Exact 5 flags multi_publisher uses for its headed Chrome (verified by
# `Get-CimInstance Win32_Process` against pid=6952 in the multi
# BrowserLauncher template). Do NOT add --headless or anti-detection
# flags — multi never does, and adding them breaks zsxq / x.com login
# state inheritance.
HEADLESS_FLAGS: list[str] = []  # kept as a no-op for backwards compat
LAUNCH_FLAGS = [
    "--no-first-run",
    "--no-default-browser-check",
    "--remote-allow-origins=*",
]

# Mirrors multi_publisher/src/multi_publisher/profile/launcher.py:launch_chrome
# headless=True block. Verified against Chrome 149 by multi_publisher's
# tests/headless_smoke.py.
HEADLESS_FLAGS = [
    "--headless",
    "--disable-blink-features=AutomationControlled",
    "--exclude-switches=enable-automation",
    "--disable-infobars",
    "--disable-gpu",
    "--window-size=1920,1080",
    "--window-position=-32000,-32000",
    "--disable-background-networking",
    "--disable-sync",
    "--disable-component-update",
    "--disable-breakpad",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--test-type",
]

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]


class CDPError(RuntimeError):
    """Anything that goes wrong while attaching or picking a tab."""


def find_chrome_exe() -> Optional[Path]:
    for p in CHROME_CANDIDATES:
        if p.exists():
            return p
    return None


def is_cdp_listening(port: int, timeout: float = 0.3) -> bool:
    try:
        with socket.create_connection(("localhost", port), timeout=timeout):
            return True
    except OSError:
        return False


def _wait_for_port(port: int, timeout: float = 10.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if is_cdp_listening(port):
            return True
        time.sleep(0.3)
    return False


def _load_proxy_flags() -> list[str]:
    """Read multi_publisher/profiles/profile-9228/proxy.json and emit
    --proxy-server= + --proxy-bypass-list= Chrome flags when enabled.

    Mirrors multi_publisher/src/multi_publisher/profile/launcher.py:88-91:
    `server` may be `socks5://host:port`; the launcher splits off the scheme
    and prefixes with `proxy_type` from the JSON's `type` field."""
    if not PROXY_CONFIG_PATH.exists():
        return []
    try:
        with open(PROXY_CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        log.warning("proxy.json unreadable, skipping proxy: %s", e)
        return []
    if not cfg.get("enabled"):
        return []
    server = cfg.get("server", "")
    ptype = cfg.get("type", "http")
    if not server:
        return []
    # multi splits on `://`; same approach.
    if "://" in server:
        hostport = server.split("://", 1)[1]
    else:
        hostport = server
    flags = [f"--proxy-server={ptype}://{hostport}"]
    bypass = cfg.get("bypass")
    if bypass:
        flags.append(f"--proxy-bypass-list={bypass}")
    log.info("proxy enabled: %s://%s (bypass=%s)", ptype, hostport, bypass)
    return flags


def launch_chrome_via_subprocess(port: int, profile_dir: Path) -> subprocess.Popen:
    chrome = find_chrome_exe()
    if not chrome:
        raise CDPError("chrome.exe not found")
    profile_dir = Path(profile_dir)
    profile_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(chrome),
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile_dir}",
        *LAUNCH_FLAGS,
        *HEADLESS_FLAGS,
        *_load_proxy_flags(),
        "about:blank",
    ]
    creationflags = 0x08000000 if sys.platform == "win32" else 0
    log.info("launching chrome (port=%d, profile=%s)", port, profile_dir)
    return subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
    )


def _kill_pid(pid: int) -> None:
    try:
        proc = subprocess.Popen(
            ["taskkill", "/F", "/PID", str(pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=0x08000000,
        )
        proc.wait(timeout=5)
    except Exception:
        pass


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
            f"cannot reach Chrome at {cdp_url}. Cause: {e!r}"
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
def scoped_chrome(
    cdp_url: str = DEFAULT_CDP_URL,
    profile_dir: Path = PROFILE_DIR,
    port: int = 9228,
) -> Iterator[Browser]:
    spawned: Optional[subprocess.Popen] = None
    if not is_cdp_listening(port):
        spawned = launch_chrome_via_subprocess(port, profile_dir)
        if not _wait_for_port(port, timeout=10):
            _kill_pid(spawned.pid)
            raise CDPError(f"Chrome launched but port {port} never came up")
    browser = attach_chrome(cdp_url)
    try:
        yield browser
    finally:
        try:
            browser.close()
        except Exception:
            pass
        _stop(browser)
        if spawned is not None:
            log.info("killing chrome pid=%d (we spawned it)", spawned.pid)
            _kill_pid(spawned.pid)


def _list_pages(browser: Browser) -> list[Page]:
    out: list[Page] = []
    for ctx in browser.contexts:
        out.extend(ctx.pages)
    return out


def find_x_page(browser: Browser) -> Optional[Page]:
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
        raise CDPError("Chrome has no default context")
    ctx: BrowserContext = contexts[0]
    page = ctx.new_page()
    page.goto(target_url, wait_until="domcontentloaded", timeout=30_000)
    return page, True


@contextlib.contextmanager
def x_page(
    target_url: str,
    profile_dir: Path = PROFILE_DIR,
) -> Iterator[Tuple[Page, bool]]:
    with scoped_chrome(DEFAULT_CDP_URL, profile_dir, port=9228) as browser:
        page, opened_new = open_or_reuse_x_page(browser, target_url)
        try:
            yield page, opened_new
        finally:
            if opened_new:
                with contextlib.suppress(Exception):
                    page.close()
