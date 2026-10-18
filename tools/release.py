#!/usr/bin/env python3
"""Mirror an already posted I-D as a GitHub Release; never submit to IETF.

SPDX-License-Identifier: BSD-3-Clause
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REPO = "Witnessability/cbee-spec"
BASE = "draft-sergeev-claim-boundaries"
LIMIT = 3_000_000
LEGACY_XML_SHA256 = {
    "640d2f2804cd2d7aeb495ed1294a03908906aa10b6e8bfd1d848b73e97ee5076",
    "d59d0e4a85bff662a8f13c34cb1eb1297f2140a62a130ddd2fdedbbdcece0829",
}


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.PIPE, timeout=120).strip()


def identifiers(revision: str, commit: str) -> str:
    if not re.fullmatch(r"[0-9]{2}", revision):
        raise ValueError("Revision must be two digits, such as 00")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Use the full, lowercase 40-character source commit SHA")
    return BASE + "-" + revision


def verify_snapshot(tag: str, files: dict[str, bytes], sums: bytes) -> None:
    expected = {tag + ".xml", tag + ".txt"}
    if set(files) != expected:
        raise ValueError("Archive must contain exactly this revision's XML and TXT")
    source = files[tag + ".xml"]
    # Only the exact official -00/-01 bytes may carry their original internal
    # DTD (four numeric character entities). Never accept a new/modified DTD.
    if (re.search(br"<!\s*(?:DOCTYPE|ENTITY)\b", source, re.I)
            and hashlib.sha256(source).hexdigest() not in LEGACY_XML_SHA256):
        raise ValueError("External entities are not supported")
    root = ET.fromstring(source)
    # The official -00/-01 archives use legacy RFCXML. Preserve their bytes;
    # only the current working source is required to use RFCXML v3.
    if root.tag != "rfc" or root.get("version") not in (None, "2", "3") or root.get("docName") != tag:
        raise ValueError("RFCXML document identity does not match the release")
    checks = {}
    for line in sums.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (\S+)", line)
        if match is None or match[2] in checks:
            raise ValueError("Malformed or duplicate checksum entry")
        checks[match[2]] = match[1]
    if set(checks) != expected:
        raise ValueError("Checksums must cover exactly this revision's XML and TXT")
    for name, data in files.items():
        if hashlib.sha256(data).hexdigest() != checks[name]:
            raise ValueError("Frozen-file checksum mismatch: " + name)


def official_bytes(name: str) -> bytes:
    url = "https://www.ietf.org/archive/id/" + name
    req = urllib.request.Request(url, headers={"User-Agent": "cbee-github-release/1"})
    with urllib.request.urlopen(req, timeout=30) as response:
        final = urllib.parse.urlsplit(response.geturl())
        if (response.status != 200 or final.scheme != "https"
                or final.netloc not in {"www.ietf.org", "ietf.org"}
                or final.path != "/archive/id/" + name or final.query or final.fragment):
            raise ValueError("Unexpected official archive response")
        data = response.read(LIMIT + 1)
    if not data or len(data) > LIMIT:
        raise ValueError("Empty or oversized archive response")
    return data


def api(endpoint: str, missing_ok: bool = False):
    command = ["gh", "api", "--hostname", "github.com", f"repos/{REPO}/{endpoint}"]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
    if result.returncode:
        if missing_ok and "(HTTP 404)" in result.stderr:
            return None
        raise RuntimeError("GitHub request failed: " + result.stderr.strip())
    return json.loads(result.stdout)


def check_tag(tag: str, commit: str, required: bool = False) -> None:
    ref = api("git/ref/tags/" + tag, missing_ok=not required)
    if ref is None:
        return
    obj = ref["object"]
    for _ in range(4):
        if obj["type"] != "tag":
            break
        obj = api("git/tags/" + obj["sha"])["object"]
    if obj.get("type") != "commit" or obj.get("sha") != commit:
        raise ValueError("Existing tag points elsewhere; it will not be moved")


def publish(tag: str, commit: str, files: dict[str, bytes], out: Path) -> dict:
    check_tag(tag, commit)
    existing = api("releases/tags/" + tag, missing_ok=True)
    if existing is None:
        latest = api("releases/latest", missing_ok=True)
        later = latest and re.fullmatch(re.escape(BASE) + r"-[0-9]{2}", latest.get("tag_name", ""))
        latest_flag = "--latest=false" if later and latest["tag_name"] > tag else "--latest"
        run("gh", "release", "create", tag, "--repo", REPO, "--target", commit,
            "--title=-" + tag[-2:], "--notes-file", str(out / "release-notes.md"),
            latest_flag, *(str(out / name) for name in files))
    record = api("releases/tags/" + tag)
    check_tag(tag, commit, required=True)
    if (record["draft"] or record["prerelease"] or record["tag_name"] != tag
            or record["name"] != "-" + tag[-2:]):
        raise ValueError("Release metadata differs; nothing will be overwritten")
    assets = record["assets"]
    if len(assets) != len(files) or {a["name"] for a in assets} != set(files):
        raise ValueError("Release assets differ; inspect the release without overwriting it")
    with tempfile.TemporaryDirectory(prefix="cbee-release-readback-") as temporary:
        run("gh", "release", "download", tag, "--repo", REPO, "--dir", temporary)
        for name, data in files.items():
            if (Path(temporary) / name).read_bytes() != data:
                raise ValueError("Downloaded release asset differs: " + name)
    return {"url": record["html_url"], "id": record["id"], "tag": tag,
            "commit": commit, "assets_verified": True, "created": existing is None}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--notes", default="")
    parser.add_argument("--publish", action="store_true", help="Create the GitHub Release after verification")
    args = parser.parse_args()
    tag = identifiers(args.revision, args.commit)
    out = ROOT / "build/release" / args.revision
    out.mkdir(parents=True, exist_ok=True)
    report_path = out / "verification.json"
    report_path.unlink(missing_ok=True)
    # The archive commit must belong to the checked-out public main history.
    run("git", "merge-base", "--is-ancestor", args.commit, "HEAD")
    def at(path: str) -> bytes:
        return subprocess.check_output(["git", "show", args.commit + ":" + path], cwd=ROOT, timeout=30)
    folder = "published/" + args.revision + "/"
    files = {tag + "." + ext: at(folder + tag + "." + ext) for ext in ("xml", "txt")}
    sums = at(folder + "SHA256SUMS")
    verify_snapshot(tag, files, sums)
    for name, data in files.items():
        if official_bytes(name) != data:
            raise ValueError("IETF archive differs from the selected snapshot: " + name)
    files["SHA256SUMS"] = sums
    for name, data in files.items():
        (out / name).write_bytes(data)
    intro = args.notes.strip() or "Published IETF revision -" + args.revision + "."
    notes = (intro + f"\n\n[Published Internet-Draft](https://datatracker.ietf.org/doc/{BASE}/{args.revision}/)"
             + f" · [Official XML](https://www.ietf.org/archive/id/{tag}.xml)"
             + f" · [Official TXT](https://www.ietf.org/archive/id/{tag}.txt)\n\n"
             + "The attached XML and TXT match the IETF archive byte-for-byte; SHA256SUMS covers both.\n"
             + f"\nArchive commit: `{args.commit}`. Exact historical files are under `published/{args.revision}/`.\n\n"
             + "This tag records the public archive import; it does not reconstruct the original private editing history. "
             + "The root XML remains the current working source and may have a different revision.\n\n"
             + "This GitHub release records an existing individual Internet-Draft publication. "
             + "It is not a new IETF submission, a working-group adoption, or an IETF consensus statement.\n")
    (out / "release-notes.md").write_text(notes, encoding="utf-8")
    report = {"tag": tag, "archive_commit": args.commit, "ietf_archive_matches": True,
              "ietf_submission_performed": False,
              "sha256": {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}
    if args.publish:
        report["github_release"] = publish(tag, args.commit, files, out)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

