# Published CBEE revisions

The IETF archive is authoritative. This directory preserves every posted
revision of draft-sergeev-claim-boundaries, including superseded editions.
The root XML is the current working source; these XML/TXT snapshots are frozen.

| Revision | IETF posting event (UTC) | Document date | Downloads and checksums |
| --- | --- | --- | --- |
| [-02](https://datatracker.ietf.org/doc/draft-sergeev-claim-boundaries/02/) | 2026-10-15T22:59:21Z | 15 October 2026 | [Archive](02/) · [GitHub release](https://github.com/Witnessability/cbee-spec/releases/tag/draft-sergeev-claim-boundaries-02) |
| [-01](https://datatracker.ietf.org/doc/draft-sergeev-claim-boundaries/01/) | 2026-09-23T04:00:40Z | 23 September 2026 | [Archive](01/) · [GitHub release](https://github.com/Witnessability/cbee-spec/releases/tag/draft-sergeev-claim-boundaries-01) |
| [-00](https://datatracker.ietf.org/doc/draft-sergeev-claim-boundaries/00/) | 2026-09-16T23:37:06Z | 17 September 2026 | [Archive](00/) · [GitHub release](https://github.com/Witnessability/cbee-spec/releases/tag/draft-sergeev-claim-boundaries-00) |

## Changes between revisions

### -02

Adds the Certificate Transparency example and distinguishes an authorization-status report from evidence that its result was available to or used by a decision-maker. Clarifies reference time and consultations without a current answer, plus references and acknowledgments. See the published Changes from -01 to -02 appendix.

### -01

Clarifies independence as limits on forgery, concealment, and circumvention; defines support and separates evidence bases; adds non-inference rules 11–13 and revises reporting distinctions. See the published Changes from -00 appendix.

### -00

Initial individual Internet-Draft: the bounding principle, claim ceilings, non-inference rules, a control-topology test, and worked examples.

## Provenance and verification

Posting timestamps come from the [Datatracker revision events](https://datatracker.ietf.org/api/v1/doc/docevent/?doc__name=draft-sergeev-claim-boundaries&type=new_revision&limit=100&format=json). The -00 posting date in UTC is 16 September, while its document date is
17 September; these are different fields. GitHub release creation dates reflect
the later public archive import, not the original IETF posting dates.

All six XML/TXT files were downloaded directly from https://www.ietf.org/archive/id/
and their byte counts and SHA-256 hashes were checked on 18 October 2026.
See [revisions.json](revisions.json) and each revision’s SHA256SUMS.

The command make check verifies the full revision inventory against pinned hashes.
The release workflow additionally compares the selected pair with the live
IETF archive and verifies the uploaded GitHub assets. It does not submit to IETF.

Historical tags point to the public commit holding the frozen archive. The root
XML at that commit may belong to a later revision; the historical release assets
and published/NN/ directory identify the exact requested edition.

Earlier private development history and correspondence are not imported.

[Back to the project](../README.md)
