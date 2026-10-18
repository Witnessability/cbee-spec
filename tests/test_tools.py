"""Editorial-tool regressions, not protocol conformance tests.
SPDX-License-Identifier: BSD-3-Clause
"""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("draft_tools", ROOT / "tools/draft.py")
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)


class EditorialTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = tools.SOURCE.read_bytes()

    def test_current_source(self):
        self.assertEqual(tools.parse_source(self.data).get("version"), "3")

    def test_archive(self):
        tools.verify_archive()

    def test_archive_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "00"
            shutil.copytree(tools.ARCHIVES, copy)
            file = copy / "00" / next(iter(tools.POSTED["00"]))
            file.write_bytes(file.read_bytes() + b"\n")
            with self.assertRaises(ValueError):
                tools.verify_archive(copy)

    def test_checksum_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "00"
            shutil.copytree(tools.ARCHIVES, copy)
            (copy / "02" / "SHA256SUMS").write_text("bogus\n")
            with self.assertRaises(ValueError):
                tools.verify_archive(copy)

    def test_wrong_identity_rejected(self):
        with self.assertRaises(ValueError):
            tools.parse_source(self.data.replace(tools.BASE.encode(), b"draft-other", 1))

    def test_external_entity_rejected(self):
        with self.assertRaises(ValueError):
            tools.parse_source(b'<!DOCTYPE rfc [<!ENTITY x SYSTEM "file:///etc/passwd">]>' + self.data)

    def test_xinclude_rejected(self):
        node = ET.fromstring(self.data)
        ET.SubElement(node, "{http://www.w3.org/2001/XInclude}include", {"href": "file.xml"})
        with self.assertRaises(ValueError):
            tools.parse_source(ET.tostring(node))

    def test_local_source_rejected(self):
        node = ET.fromstring(self.data)
        ET.SubElement(node, "artwork", {"src": "file.xml"})
        with self.assertRaises(ValueError):
            tools.parse_source(ET.tostring(node))

    def test_duplicate_anchor_rejected(self):
        node = ET.fromstring(self.data)
        anchor = next(e.get("anchor") for e in node.iter() if e.get("anchor"))
        ET.SubElement(node, "section", {"anchor": anchor})
        with self.assertRaises(ValueError):
            tools.parse_source(ET.tostring(node))

    def test_missing_xref_rejected(self):
        node = ET.fromstring(self.data)
        ET.SubElement(node, "xref", {"target": "missing-anchor"})
        with self.assertRaises(ValueError):
            tools.parse_source(ET.tostring(node))

    def test_working_revision_can_advance(self):
        original = ET.fromstring(self.data)
        original.set("docName", tools.BASE + "-03")
        self.assertTrue(tools.parse_source(ET.tostring(original)).get("docName").endswith("-03"))

    def test_reading_copy_matches(self):
        self.assertEqual(tools.READING.read_text(), tools.render_reading(self.data))

    def test_reading_copy_includes_every_section_and_reference(self):
        root = ET.fromstring(self.data)
        reading = tools.render_reading(self.data)
        for node in root.iter():
            if node.tag in ("section", "reference") and node.get("anchor"):
                self.assertIn(f'id="{node.get("anchor")}"', reading)
        for details in root.iter("refcontent"):
            self.assertIn(tools.inline(details), reading)

    def test_reading_copy_preserves_definition_terms_and_nested_definitions(self):
        root = ET.fromstring(self.data)
        reading = tools.render_reading(self.data)
        for term in root.iter("dt"):
            self.assertIn("**" + " ".join(tools.inline(term).split()) + "**", reading)
        sample = ET.fromstring('<dl><dt>Outer</dt><dd><t>Meaning.</t><dl><dt>Inner</dt><dd><t>Detail.</t></dd></dl></dd></dl>')
        rendered = tools.block(sample)
        for text in ("**Outer**", "Meaning.", "**Inner**", "Detail."):
            self.assertIn(text, rendered)

    def test_missing_historical_revision_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "published"
            shutil.copytree(tools.ARCHIVES, copy)
            shutil.rmtree(copy / "01")
            with self.assertRaises(ValueError):
                tools.verify_archive(copy)

    def test_artwork_indentation(self):
        node = ET.fromstring("<artwork>  A\n    |\n    B</artwork>")
        self.assertEqual(tools.block(node), "```text\n  A\n    |\n    B\n```\n\n")

    def test_reference_section(self):
        node = ET.fromstring('<xref target="RFC9334" section="12.2"/>')
        paragraph = ET.Element("t")
        paragraph.append(node)
        self.assertIn("Section 12.2 of [RFC9334](#RFC9334)", tools.block(paragraph))

    def test_no_published_claim_in_reading_copy(self):
        reading = tools.render_reading(self.data)
        self.assertIn("not a separate IETF publication", reading)
        self.assertIn(tools.sha256(self.data), reading)


if __name__ == "__main__":
    unittest.main()

