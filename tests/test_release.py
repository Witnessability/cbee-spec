"""Release safety tests; no network calls or GitHub writes.
SPDX-License-Identifier: BSD-3-Clause
"""
import hashlib
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release_tools", ROOT / "tools/release.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tag = release.BASE + "-00"
        self.sha = "a" * 40
        self.xml = f'<rfc version="3" docName="{self.tag}"><front/></rfc>'.encode()
        self.files = {self.tag + ".xml": self.xml, self.tag + ".txt": b"Published test fixture\n"}
        self.sums = "".join(hashlib.sha256(data).hexdigest() + "  " + name + "\n" for name, data in self.files.items()).encode()

    def test_identifiers(self):
        self.assertEqual(release.identifiers("00", self.sha), self.tag)

    def test_bad_revisions(self):
        for value in ("0", "-00", "000", "../00", "00;echo bad", "١٢"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                release.identifiers(value, self.sha)

    def test_exact_commit_required(self):
        for value in ("main", "HEAD", "a" * 39, "A" * 40, "x" * 40):
            with self.subTest(value=value), self.assertRaises(ValueError):
                release.identifiers("00", value)

    def test_snapshot(self):
        release.verify_snapshot(self.tag, self.files, self.sums)

    def test_real_historical_archives_preserved(self):
        for revision in ("00", "01", "02"):
            tag = release.BASE + "-" + revision
            directory = ROOT / "published" / revision
            files = {tag + "." + ext: (directory / (tag + "." + ext)).read_bytes() for ext in ("xml", "txt")}
            with self.subTest(revision=revision):
                release.verify_snapshot(tag, files, (directory / "SHA256SUMS").read_bytes())

    def test_wrong_document(self):
        xml = self.xml.replace(b"-00", b"-01")
        files = dict(self.files, **{self.tag + ".xml": xml})
        with self.assertRaises(ValueError):
            release.verify_snapshot(self.tag, files, self.sums)

    def test_mutated_archive(self):
        files = dict(self.files, **{self.tag + ".txt": b"Changed\n"})
        with self.assertRaises(ValueError):
            release.verify_snapshot(self.tag, files, self.sums)

    def test_duplicate_missing_or_extra_checksums(self):
        for sums in (self.sums + self.sums, b"", self.sums + b"0" * 64 + b"  extra.txt\n"):
            with self.subTest(sums=sums), self.assertRaises(ValueError):
                release.verify_snapshot(self.tag, self.files, sums)

    def test_external_entity(self):
        xml = b'<!DOCTYPE rfc [<!ENTITY e SYSTEM "file:///etc/passwd">]>' + self.xml
        with self.assertRaises(ValueError):
            release.verify_snapshot(self.tag, dict(self.files, **{self.tag + ".xml": xml}), self.sums)

    def test_matching_tag(self):
        with patch.object(release, "api", return_value={"object": {"type": "commit", "sha": self.sha}}):
            release.check_tag(self.tag, self.sha, required=True)

    def test_tag_must_not_move(self):
        with patch.object(release, "api", return_value={"object": {"type": "commit", "sha": "b" * 40}}):
            with self.assertRaises(ValueError):
                release.check_tag(self.tag, self.sha)

    def test_annotated_tag(self):
        with patch.object(release, "api", side_effect=[{"object": {"type": "tag", "sha": "c" * 40}}, {"object": {"type": "commit", "sha": self.sha}}]):
            release.check_tag(self.tag, self.sha, required=True)

    def test_archive_response(self):
        name = self.tag + ".xml"
        with patch.object(release.urllib.request, "urlopen") as opened:
            response = opened.return_value.__enter__.return_value
            response.status = 200
            response.geturl.return_value = "https://www.ietf.org/archive/id/" + name
            response.read.return_value = self.xml
            self.assertEqual(release.official_bytes(name), self.xml)

    def test_bad_archive_response(self):
        name = self.tag + ".xml"
        for url, status, data in (
            ("https://example.invalid/archive/id/" + name, 200, self.xml),
            ("http://www.ietf.org/archive/id/" + name, 200, self.xml),
            ("https://www.ietf.org/archive/id/wrong.xml", 200, self.xml),
            ("https://www.ietf.org/archive/id/" + name, 404, self.xml),
            ("https://www.ietf.org/archive/id/" + name, 200, b""),
            ("https://www.ietf.org/archive/id/" + name, 200, b"x" * (release.LIMIT + 1)),
        ):
            with self.subTest(url=url, status=status, size=len(data)), patch.object(release.urllib.request, "urlopen") as opened:
                response = opened.return_value.__enter__.return_value
                response.status, response.geturl.return_value, response.read.return_value = status, url, data
                with self.assertRaises(ValueError):
                    release.official_bytes(name)


if __name__ == "__main__":
    unittest.main()

