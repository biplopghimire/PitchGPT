import re
from typing import Optional

try:
    from ftfy import fix_text  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    def fix_text(x: str) -> str:  # fallback
        return x

try:
    from cleantext import clean  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    def clean(x: str, **kwargs):  # fallback passthrough
        return x

_WS_RE = re.compile(r"\s+")


def normalize(text: Optional[str]) -> str:
    """Normalize raw text for prompt context.

    Steps:
    1. Unicode fixes (ftfy) to handle mojibake / smart quotes.
    2. Remove URLs/emails/phones & collapse line breaks (clean-text) if available.
    3. Collapse all remaining whitespace to single spaces.
    """
    if not text:
        return ""
    t = fix_text(text)
    try:
        t = clean(
            t,
            lower=False,
            no_urls=False,
            no_emails=False,
            no_phone_numbers=False,
            no_line_breaks=True,
            no_emoji=True,
        )
    except Exception:
        # If clean-text not installed or errors, continue with partially cleaned text
        pass
    t = _WS_RE.sub(" ", t).strip()
    return t


def truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1] + "…"

__all__ = ["normalize", "truncate"]
