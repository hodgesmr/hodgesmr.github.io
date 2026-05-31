"""
generate-security-txt.py

Quarto post-render script that writes docs/.well-known/security.txt
(RFC 9116). The file is generated rather than hand-maintained so the
required `Expires` field is always stamped one year ahead of the build
and never silently goes stale.

Usage in _quarto.yml:
    project:
      post-render:
        - "python generate-security-txt.py"
"""

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUTPUT_DIR = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))

SITE_URL = "https://matthodges.com"
CONTACT = "mailto:matt@iliumstrategies.com"


def main():
    expires = (datetime.now(timezone.utc) + timedelta(days=365)).strftime(
        "%Y-%m-%dT%H:%M:%S.000Z"
    )
    lines = [
        f"Contact: {CONTACT}",
        f"Expires: {expires}",
        "Preferred-Languages: en",
        f"Canonical: {SITE_URL}/.well-known/security.txt",
        "",
    ]

    well_known = OUTPUT_DIR / ".well-known"
    well_known.mkdir(parents=True, exist_ok=True)
    path = well_known / "security.txt"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {path} (expires {expires})")


if __name__ == "__main__":
    main()
