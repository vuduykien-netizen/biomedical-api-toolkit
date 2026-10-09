#!/usr/bin/env python3
"""Make one bounded, read-only public API request and retain provenance."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

REGISTRY_PATH = Path(__file__).resolve().parents[1] / "references" / "registry.json"
MAX_RESPONSE_BYTES = 10 * 1024 * 1024
SENSITIVE_PARAMS = {"api_key", "apikey", "token", "access_token", "email", "mailto", "key", "authorization", "x-api-key"}
RETRY_CODES = {429, 500, 502, 503, 504}


class NoRedirect(HTTPRedirectHandler):
    """Do not forward query credentials or headers to a redirect destination."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def parse_params(items: list[str]) -> list[tuple[str, str]]:
    result = []
    for item in items:
        key, separator, value = item.partition("=")
        if not separator or not key:
            raise ValueError("Each --param must be a nonempty key followed by =value.")
        if key.casefold() in SENSITIVE_PARAMS:
            raise ValueError("Pass credentials and contact emails through the documented environment variables.")
        result.append((key, value))
    return result


def checked_path(path: str) -> str:
    decoded = path
    # Also reject double-encoded traversal and URL separators.
    for _ in range(3):
        decoded = unquote(decoded)
    parsed = urlsplit(decoded)
    if (parsed.scheme or parsed.netloc or parsed.query or parsed.fragment
            or decoded.startswith("/") or "\\" in decoded
            or any(part in {".", ".."} for part in decoded.split("/"))
            or any(ord(char) < 32 for char in decoded)):
        raise ValueError("--path must stay within the provider API; use --param for query arguments.")
    return quote(decoded, safe="/:@,;+-._~")


def prepare_request(provider: dict[str, Any], path: str, params: list[tuple[str, str]],
                    environ: dict[str, str] | None = None, dry_run: bool = False):
    env = os.environ if environ is None else environ
    base = provider["base_url"]
    parsed_base = urlsplit(base)
    if parsed_base.scheme != "https" or not parsed_base.netloc or parsed_base.query or parsed_base.fragment:
        raise ValueError("Provider registry requires a fixed HTTPS API base.")
    endpoint = base.rstrip("/") + "/" + checked_path(path)
    actual_params = list(params)
    public_params = list(params)
    headers = {"Accept": "application/json, application/xml;q=0.8, text/plain;q=0.5",
               "User-Agent": "biomedical-api-toolkit/1.0"}
    secrets = []
    auth = provider.get("credential")
    if auth:
        secret = env.get(auth["env"], "")
        if auth.get("required") and not secret and not dry_run:
            raise ValueError(f"Set {auth['env']} locally before querying this provider.")
        if secret:
            secrets.append(secret)
            if auth["location"] == "query":
                actual_params.append((auth["name"], secret))
                public_params.append((auth["name"], "REDACTED"))
            else:
                headers[auth["name"]] = auth.get("prefix", "") + secret
        elif auth.get("required") and dry_run:
            public_params.append((auth["name"], "REQUIRED_ENV"))
    actual_url = endpoint + ("?" + urlencode(actual_params) if actual_params else "")
    public_url = endpoint + ("?" + urlencode(public_params) if public_params else "")
    return Request(actual_url, headers=headers, method="GET"), public_url, secrets


def redact(value: Any, secrets: list[str]) -> Any:
    if isinstance(value, str):
        for secret in sorted(set(secrets), key=len, reverse=True):
            if secret:
                for form in {secret, quote(secret, safe=""), urlencode({"x": secret})[2:]}:
                    # Percent-escape hex digits may be lowercase in provider echoes.
                    value = re.sub(re.escape(form), "REDACTED", value, flags=re.IGNORECASE)
        return value
    if isinstance(value, list):
        return [redact(item, secrets) for item in value]
    if isinstance(value, dict):
        return {redact(key, secrets): redact(item, secrets) for key, item in value.items()}
    return value


def fetch(request: Request, timeout: float = 20, retries: int = 2,
          opener=None, sleep=time.sleep) -> tuple[int, str, Any]:
    client = opener if opener is not None else build_opener(NoRedirect())
    for attempt in range(retries + 1):
        try:
            with client.open(request, timeout=timeout) as response:
                raw = response.read(MAX_RESPONSE_BYTES + 1)
                if len(raw) > MAX_RESPONSE_BYTES:
                    raise ValueError("Response exceeds 10 MiB; narrow the query or use provider export tools.")
                content_type = response.headers.get("Content-Type", "")
                charset = response.headers.get_content_charset() or "utf-8"
                text = raw.decode(charset, errors="replace")
                try:
                    data = json.loads(text)
                except json.JSONDecodeError:
                    data = {"raw_text": text}
                return response.status, content_type, data
        except HTTPError as error:
            status = error.code
            retry_after = error.headers.get("Retry-After", "") if error.headers else ""
            error.close()
            if status in RETRY_CODES and attempt < retries:
                try:
                    delay = max(0, float(retry_after))
                except ValueError:
                    delay = 2 ** attempt
                if delay > 30:
                    raise ValueError(f"HTTP {status}; provider requests a long wait. Retry later.") from None
                sleep(delay)
                continue
            # Do not expose HTTPError URLs/bodies, which may echo credentials.
            raise ValueError(f"HTTP {status}; check endpoint, credentials, quota and official documentation.") from None
        except (URLError, TimeoutError, OSError):
            if attempt < retries:
                sleep(2 ** attempt)
                continue
            raise ValueError("Network request failed after bounded attempts; retry later.") from None
    raise ValueError("Request could not be completed.")


def save_output(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as output:
        json.dump(value, output, ensure_ascii=False, indent=2)
        output.write("\n")


def main(argv: list[str] | None = None) -> int:
    providers = registry()["providers"]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("provider", choices=sorted(providers))
    parser.add_argument("--path", help="API-relative endpoint path, without query parameters")
    parser.add_argument("--param", action="append", default=[], metavar="KEY=VALUE")
    parser.add_argument("--demo", action="store_true", help="Use the registry's small example")
    parser.add_argument("--dry-run", action="store_true", help="Print a redacted plan; do not make a request")
    parser.add_argument("--output", type=Path, help="Save a provenance envelope to a new JSON file")
    parser.add_argument("--timeout", type=float, default=20)
    parser.add_argument("--retries", type=int, choices=range(3), default=2)
    args = parser.parse_args(argv)
    try:
        if not 0 < args.timeout <= 60:
            raise ValueError("--timeout must be greater than zero and at most 60 seconds.")
        if args.output and args.output.exists():
            raise ValueError("Output already exists; choose a new file to preserve previous results.")
        provider = providers[args.provider]
        params = list(provider["demo"]["params"].items()) if args.demo else []
        overrides = parse_params(args.param)
        overridden_keys = {key for key, _ in overrides}
        params = [(key, value) for key, value in params if key not in overridden_keys] + overrides
        path = args.path if args.path is not None else (provider["demo"]["path"] if args.demo else None)
        if path is None:
            raise ValueError("Provide --path or --demo.")
        request, public_url, secrets = prepare_request(provider, path, params, dry_run=args.dry_run)
        envelope = {"provider": args.provider, "request": {"method": "GET", "url": public_url},
                    "retrieved_at_utc": None, "http_status": None, "dry_run": args.dry_run}
        if not args.dry_run:
            status, content_type, data = fetch(request, timeout=args.timeout, retries=args.retries)
            envelope.update(retrieved_at_utc=datetime.now(timezone.utc).isoformat(),
                            http_status=status, content_type=content_type, data=data)
        envelope = redact(envelope, secrets)
        if args.output:
            save_output(args.output, envelope)
            print("Saved request envelope. Inspect the response body for provider-level errors and completeness.")
        else:
            print(json.dumps(envelope, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as error:
        # Never emit exception representations containing raw request objects.
        print(f"Error: {error}" if isinstance(error, ValueError) else "Error: Could not write output.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
