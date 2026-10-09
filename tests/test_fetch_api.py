import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from email.message import Message
from urllib.error import HTTPError, URLError
from urllib.request import Request

spec = importlib.util.spec_from_file_location("fetch_api", Path(__file__).resolve().parents[1] / "scripts" / "fetch_api.py")
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


class Response:
    status = 200

    def __init__(self, body=b'{"results": [1]}', content_type="application/json"):
        self.body = body
        self.headers = Message()
        self.headers["Content-Type"] = content_type

    def read(self, size):
        return self.body[:size]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class SequenceOpener:
    def __init__(self, *items):
        self.items = iter(items)
        self.calls = 0

    def open(self, *args, **kwargs):
        self.calls += 1
        item = next(self.items)
        if isinstance(item, Exception):
            raise item
        return item


class HelperBehaviorTests(unittest.TestCase):
    def test_query_encoding_keeps_search_syntax(self):
        provider = api.registry()["providers"]["pubmed"]
        request, _, _ = api.prepare_request(provider, "esearch.fcgi", [("term", 'diabetes[MeSH Terms] AND "type 2"')], environ={})
        from urllib.parse import parse_qs, urlsplit
        self.assertEqual(parse_qs(urlsplit(request.full_url).query)["term"], ['diabetes[MeSH Terms] AND "type 2"'])

    def test_credentials_are_sent_but_not_in_provenance_or_echo(self):
        provider = api.registry()["providers"]["unpaywall"]
        request, public, secrets = api.prepare_request(provider, "10.1/example", [], environ={"UNPAYWALL_EMAIL": "private@example.invalid"})
        self.assertIn("private%40example.invalid", request.full_url)
        self.assertNotIn("private", public)
        value = api.redact({"echo": request.full_url, "nested": ["private@example.invalid"]}, secrets)
        self.assertNotIn("private", json.dumps(value))

    def test_header_credentials_not_in_public_url(self):
        provider = api.registry()["providers"]["semanticscholar"]
        request, public, secrets = api.prepare_request(provider, "paper/search", [], environ={"S2_API_KEY": "fake-test-secret"})
        self.assertEqual(request.get_header("X-api-key"), "fake-test-secret")
        self.assertNotIn("fake-test-secret", public)
        self.assertEqual(secrets, ["fake-test-secret"])

    def test_percent_encoded_echo_redaction_is_case_insensitive(self):
        secret = "Fake+Token/Contact@Example.invalid"
        value = {"echo": "Fake%2bToken%2fContact%40Example.invalid"}
        self.assertEqual(api.redact(value, [secret]), {"echo": "REDACTED"})

    def test_missing_contact_blocks_network_plan_but_allows_dry_run(self):
        provider = api.registry()["providers"]["unpaywall"]
        with self.assertRaisesRegex(ValueError, "UNPAYWALL_EMAIL"):
            api.prepare_request(provider, "10.1/example", [], environ={})
        _, public, _ = api.prepare_request(provider, "10.1/example", [], environ={}, dry_run=True)
        self.assertIn("REQUIRED_ENV", public)

    def test_unsafe_paths_cannot_escape_provider(self):
        for path in ["https://example.invalid/", "//example.invalid", "../private", "%252e%252e/private", "x?api_key=secret", "x#fragment", "x\\private"]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                api.checked_path(path)
        self.assertEqual(api.checked_path("works/10.1038/nature12373"), "works/10.1038/nature12373")

    def test_sensitive_cli_params_are_rejected(self):
        for param in ["api_key=secret", "email=private@example.invalid", "Token=secret"]:
            with self.assertRaises(ValueError):
                api.parse_params([param])

    def test_429_retries_then_parses_json(self):
        headers = Message()
        headers["Retry-After"] = "1"
        error = HTTPError("https://example.invalid/?api_key=secret", 429, "rate", headers, io.BytesIO(b"secret"))
        opener = SequenceOpener(error, Response())
        waits = []
        status, _, data = api.fetch(Request("https://example.invalid"), opener=opener, sleep=waits.append)
        self.assertEqual((status, data), (200, {"results": [1]}))
        self.assertEqual(waits, [1])
        self.assertEqual(opener.calls, 2)

    def test_http_error_does_not_expose_url_or_body(self):
        error = HTTPError("https://example.invalid/?api_key=private-secret", 403, "private-secret", Message(), io.BytesIO(b"private-secret"))
        with self.assertRaises(ValueError) as caught:
            api.fetch(Request("https://example.invalid"), opener=SequenceOpener(error))
        self.assertNotIn("private-secret", str(caught.exception))

    def test_network_retries_are_bounded(self):
        opener = SequenceOpener(URLError("secret"), URLError("secret"), URLError("secret"))
        with self.assertRaisesRegex(ValueError, "bounded"):
            api.fetch(Request("https://example.invalid"), opener=opener, sleep=lambda _: None)
        self.assertEqual(opener.calls, 3)

    def test_non_json_body_is_preserved(self):
        _, _, data = api.fetch(Request("https://example.invalid"), opener=SequenceOpener(Response(b"<records/>", "application/xml")))
        self.assertEqual(data, {"raw_text": "<records/>"})

    def test_previous_results_are_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "result.json"
            api.save_output(output, {"original": 1})
            with self.assertRaises(FileExistsError):
                api.save_output(output, {"replacement": 2})
            self.assertEqual(json.loads(output.read_text()), {"original": 1})


if __name__ == "__main__":
    unittest.main()
