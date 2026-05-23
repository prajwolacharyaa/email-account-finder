"""Core OSINT scanning logic for Email Account Finder.

This module only uses public, legal lookups. It does not attempt login,
password reset abuse, bypassing, scraping private data, or rate-limit evasion.
Some websites intentionally prevent account enumeration, so those checks are
reported as "Protected" instead of pretending to be certain.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import requests


HISTORY_FILE = Path("history.json")
EXPORT_DIR = Path("exports")
REQUEST_TIMEOUT = 8


@dataclass
class ScanResult:
    website: str
    status: str
    link: str
    method: str
    note: str


def is_valid_email(email: str) -> bool:
    """Return True when the input looks like a normal email address."""
    pattern = r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def fetch_url(url: str, method: str = "GET") -> requests.Response | None:
    """Fetch a public URL with a short timeout and friendly user agent."""
    headers = {
        "User-Agent": (
            "EmailAccountFinder/1.0 "
            "(public OSINT educational project; no login or bypass attempts)"
        )
    }
    try:
        if method == "HEAD":
            return requests.head(url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        return requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True)
    except requests.RequestException:
        return None


def check_gravatar(email: str) -> ScanResult:
    """Check Gravatar's public hash endpoint for a profile."""
    email_hash = hashlib.md5(email.strip().lower().encode("utf-8")).hexdigest()
    profile_url = f"https://www.gravatar.com/{email_hash}.json"
    response = fetch_url(profile_url)

    if response and response.status_code == 200:
        return ScanResult(
            website="Gravatar",
            status="Found",
            link=f"https://www.gravatar.com/{email_hash}",
            method="Public email hash lookup",
            note="A public Gravatar profile exists for this email hash.",
        )

    return ScanResult(
        website="Gravatar",
        status="Not Found",
        link="-",
        method="Public email hash lookup",
        note="No public Gravatar profile was returned.",
    )


def check_github_email(email: str) -> ScanResult:
    """Use GitHub's public user search as a weak email signal."""
    api_url = f"https://api.github.com/search/users?q={email}+in:email"
    response = fetch_url(api_url)

    if response and response.status_code == 200:
        payload = response.json()
        items = payload.get("items", [])
        if items:
            profile = items[0].get("html_url", "-")
            return ScanResult(
                website="GitHub",
                status="Found",
                link=profile,
                method="GitHub public user search",
                note="GitHub returned a public profile for this email search.",
            )
        return ScanResult(
            website="GitHub",
            status="Not Found",
            link="-",
            method="GitHub public user search",
            note="No public GitHub user email match was returned.",
        )

    if response and response.status_code in {403, 429}:
        note = "GitHub rate-limited the request. Try again later or add your own API workflow."
    else:
        note = "GitHub could not be checked from this network."

    return ScanResult(
        website="GitHub",
        status="Unknown",
        link="https://github.com/search?q=" + email,
        method="GitHub public user search",
        note=note,
    )


MANUAL_REVIEW_SITES = [
    ("Facebook", "https://www.facebook.com/login/identify"),
    ("Instagram", "https://www.instagram.com/accounts/password/reset/"),
    ("YouTube", "https://accounts.google.com/signin/recovery"),
    ("TikTok", "https://www.tiktok.com/login/phone-or-email/email"),
    ("Snapchat", "https://accounts.snapchat.com/accounts/password_reset_request"),
    ("Reddit", "https://www.reddit.com/password"),
    ("X (formerly Twitter)", "https://twitter.com/account/begin_password_reset"),
    ("Pinterest", "https://www.pinterest.com/password/reset/"),
    ("LinkedIn", "https://www.linkedin.com/uas/request-password-reset"),
    ("Threads", "https://www.threads.net/login"),
    ("Discord", "https://discord.com/login"),
    ("Quora", "https://www.quora.com/forgot_password"),
    ("Twitch", "https://www.twitch.tv/user/account-recovery"),
    ("Telegram", "https://web.telegram.org/"),
]


def manual_review_results() -> list[ScanResult]:
    """Return safe links for services that block reliable automated checks."""
    return [
        ScanResult(
            website=name,
            status="Protected",
            link=link,
            method="Official account recovery or login page",
            note=(
                "This platform does not provide a safe public API to confirm accounts by email. "
                "Use the official page only for your own email or authorized work."
            ),
        )
        for name, link in MANUAL_REVIEW_SITES
    ]


def scan_email(email: str) -> list[ScanResult]:
    """Run all legal public checks for one email address."""
    clean_email = email.strip().lower()
    if not is_valid_email(clean_email):
        raise ValueError("Please enter a valid email address.")

    results = [check_gravatar(clean_email), check_github_email(clean_email)]
    results.extend(manual_review_results())
    save_history(clean_email, results)
    return results


def load_history() -> list[dict]:
    """Load saved searches from disk."""
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_history(email: str, results: Iterable[ScanResult]) -> None:
    """Append one scan to the local search history."""
    entry = {
        "email": email,
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "results": [asdict(result) for result in results],
    }
    history = load_history()
    history.insert(0, entry)
    HISTORY_FILE.write_text(json.dumps(history[:50], indent=2), encoding="utf-8")


def export_csv(email: str, results: Iterable[ScanResult]) -> Path:
    """Export scan results to a CSV file."""
    EXPORT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = EXPORT_DIR / f"email-account-finder-{timestamp}.csv"

    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["website", "status", "link", "method", "note"])
        writer.writeheader()
        for result in results:
            writer.writerow(asdict(result))

    return path


def export_pdf(email: str, results: Iterable[ScanResult]) -> Path:
    """Export results to a simple PDF when reportlab is installed."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise RuntimeError("PDF export requires reportlab. Run: pip install reportlab") from exc

    EXPORT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = EXPORT_DIR / f"email-account-finder-{timestamp}.pdf"

    pdf = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Email Account Finder Report")
    y -= 25

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"Email: {email}")
    y -= 18
    pdf.drawString(50, y, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30

    for result in results:
        if y < 90:
            pdf.showPage()
            y = height - 50
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(50, y, f"{result.website}: {result.status}")
        y -= 14
        pdf.setFont("Helvetica", 8)
        pdf.drawString(65, y, f"Link: {result.link[:95]}")
        y -= 12
        pdf.drawString(65, y, f"Note: {result.note[:95]}")
        y -= 18

    pdf.save()
    return path
