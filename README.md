# Claim Boundaries for Execution Evidence (CBEE)

An individual Internet-Draft on what logs, receipts, signatures, attestations,
and other execution evidence can establish about an action.

[![Build and check draft](https://github.com/Witnessability/cbee-spec/actions/workflows/build.yml/badge.svg?branch=main&event=push)](https://github.com/Witnessability/cbee-spec/actions/workflows/build.yml)

Editing workspace for **draft-sergeev-claim-boundaries**, an individual
Internet-Draft by **Mikhail Sergeev**, with intended status **Informational**.
It is not an adopted working-group document or an IETF consensus statement.

**Published baseline: -02**, posted on **15 October 2026 (UTC)**.
The working XML currently matches that publication exactly.
All published revisions, **-00, -01, and -02**, are preserved below.
Changes to the working source remain editorial work until a new revision is
submitted and posted by the IETF.

## Read, review, and contribute

**To read or comment, no installation is needed.** Start with the
[published HTML](https://www.ietf.org/archive/id/draft-sergeev-claim-boundaries-02.html)
or the [editor's reading copy](review/editor-copy.md), then
[open a feedback issue](https://github.com/Witnessability/cbee-spec/issues/new?template=feedback.md)
or [email the editor](mailto:mikhailsergeev369@gmail.com). A section reference,
a claim to examine, and a question or counterexample are enough.

| Resource | Purpose |
| --- | --- |
| [Published -02](https://datatracker.ietf.org/doc/draft-sergeev-claim-boundaries/02/) | The authoritative current IETF revision |
| [Publication history](published/README.md) | Every posted revision, dates, summaries, and official links |
| [GitHub releases](https://github.com/Witnessability/cbee-spec/releases) | Revision tags, notes, exact XML/TXT, and SHA256SUMS |
| [Editor's reading copy](review/editor-copy.md) | GitHub-readable working text generated from the XML |
| [Working RFCXML](draft-sergeev-claim-boundaries.xml) | The only editable manuscript source |
| [Published archives](published/) | Frozen -00/-01/-02 files and checksums |
| [Issues](https://github.com/Witnessability/cbee-spec/issues) / [pull requests](https://github.com/Witnessability/cbee-spec/pulls) | Questions, counterexamples, and proposed edits |
| [Builds and review artifacts](https://github.com/Witnessability/cbee-spec/actions/workflows/build.yml) | Working XML/TXT/HTML, diff from -02, hashes, and logs |
| [Contribution guidance](CONTRIBUTING.md) | Review, attribution, and IETF contribution terms |
| [Preparation and submission](PUBLICATION-PROCESS.md) | Preflight, exact-file approval, and publication verification |

Feedback by email is equally welcome; GitHub participation is optional.
Repository merges record editorial decisions, without implying contributor
endorsement or a working-group decision.

## Published revisions

| Revision | IETF posting date (UTC) | Main changes | Files |
| --- | --- | --- | --- |
| [-02](https://datatracker.ietf.org/doc/draft-sergeev-claim-boundaries/02/) | 2026-10-15 | Certificate Transparency example; authorization-status evidence, availability, and decision-time use | [Archive](published/02/) · [Release](https://github.com/Witnessability/cbee-spec/releases/tag/draft-sergeev-claim-boundaries-02) |
| [-01](https://datatracker.ietf.org/doc/draft-sergeev-claim-boundaries/01/) | 2026-09-23 | Independence capabilities; support and evidence bases; non-inference rules 11–13; reporting distinctions | [Archive](published/01/) · [Release](https://github.com/Witnessability/cbee-spec/releases/tag/draft-sergeev-claim-boundaries-01) |
| [-00](https://datatracker.ietf.org/doc/draft-sergeev-claim-boundaries/00/) | 2026-09-16 | Initial claim-boundary discipline, control-topology test, and worked examples | [Archive](published/00/) · [Release](https://github.com/Witnessability/cbee-spec/releases/tag/draft-sergeev-claim-boundaries-00) |

The [history index](published/README.md) separates IETF posting timestamps
from document dates and the later creation of this GitHub mirror.
The IETF archive remains authoritative.

## Scope

CBEE examines the boundary between an execution-related claim and the evidence
offered in support of it. It distinguishes authorization, invocation, execution,
completion, and external effect; identifies non-inferences from signatures,
receipts, timestamps, and transparency records; and examines the control and
observation dependencies behind prevention and detection claims.

The document states a claim-appraisal discipline. It defines no protocol,
record format, registry, or universal evidence-production mechanism. Its
reporting distinctions describe what available evidence supports; they are
not a protocol-conformance test suite.

## Edit and build

**This is a document repository.** The Python tools generate a reading copy,
check source links and archive integrity, run the official xml2rfc formatter,
and compare the working source with published -02. The build badge reports
editorial checks, not validation of the model or approval to publish.

Python **3.12** is the CI environment. xml2rfc is pinned in `requirements.txt`;
the reading-copy, integrity, and regression commands use the standard library.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
# Edit draft-sergeev-claim-boundaries.xml, then:
make review     # refresh review/editor-copy.md
make check      # source anchors/xrefs, all archive hashes, reading copy
make test       # editorial and release-tool regressions
make build      # official xml2rfc TXT/HTML, repeated in one environment
```

Open `build/index.html` locally. CI artifacts contain the exact working XML,
TXT/HTML renderings, source diff from -02, output hashes, formatter logs, and
resolved package versions. Generated build files are not committed. Dependency
installation uses the network; rendering disables network reference resolution
and rejects local-file includes.

These checks do not establish semantic correctness, interoperability, legal
clearance, IETF acceptance, or a fresh online idnits result. Preparing a new
submission still requires the review and current preflight in
[PUBLICATION-PROCESS.md](PUBLICATION-PROCESS.md).

## GitHub releases

Release titles follow the I-D revision (`-00`, `-01`, ...); tags use the full
document name, such as `draft-sergeev-claim-boundaries-02`. Every release
records an already posted IETF revision and includes XML, TXT, and SHA256SUMS.

The initial history is imported after -02 was published. Historical tags point
to the public archive-import commit, not reconstructed private development
commits. For a historical revision, use its `published/NN/` directory or release
assets; the root XML remains the current working source.

To mirror a future **already published** revision, preserve its exact files and
checksums under `published/NN/`, update the pinned archive inventory and history,
and merge the reviewed change. Run
[Release a published IETF revision](https://github.com/Witnessability/cbee-spec/actions/workflows/release.yml)
on `main`, supplying the two-digit revision and full archive commit SHA.
The workflow compares the files with the live IETF archive, creates the GitHub
release, and downloads its assets to verify them again. It refuses to move an
existing tag or overwrite conflicting assets. A matching rerun only verifies
the existing release. No release runs automatically on a push or merge.

## Branch and revision policy

`main` is the single ongoing development branch. Use short-lived topic branches
for focused PRs and delete them after their commits are merged. Retain an
additional branch only for active work with a stated purpose. Tags and frozen
archive directories preserve published revisions without release branches.

Keep one editable root XML and immutable published XML/TXT snapshots. The
official -00 and -01 XML use older RFCXML syntax and are intentionally preserved
without conversion; the working -02 XML uses RFCXML v3.

Ordinary CI has read-only repository permissions. Only the manually invoked
GitHub release job has contents-write permission for tags, releases, and assets.
No workflow submits to Datatracker, sends mail, or merges a PR. Submitting a new
I-D requires the author's decision for the exact package and intended actions.

The public Git history starts with -02 and the contribution process; older
publications are imported as frozen artifacts. Private Git history and
correspondence are not imported. See [LICENSE.md](LICENSE.md) for the document
notices and the separate tooling license.
