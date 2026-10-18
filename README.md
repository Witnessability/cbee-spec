# Claim Boundaries for Execution Evidence (CBEE)

An individual Internet-Draft on what logs, receipts, signatures, attestations,
and other execution evidence can establish about an action.

Editing workspace for **draft-sergeev-claim-boundaries**, an individual
Internet-Draft by **Mikhail Sergeev**, with intended status **Informational**.
The document is an individual contribution; repository activity does not
establish working-group adoption or IETF consensus.

**Published baseline:** revision **-02**. This workspace starts from the exact
published XML and TXT. Changes to the working source remain editorial work
until a new revision is submitted and posted by the IETF.

## Read, review, and contribute

**To read or comment, no installation is needed.** Start with the
[published HTML](https://www.ietf.org/archive/id/draft-sergeev-claim-boundaries-02.html),
then [open a feedback issue](https://github.com/Witnessability/cbee-spec/issues/new?template=feedback.md)
or [email the editor](mailto:mikhailsergeev369@gmail.com). A section reference,
a claim to examine, and a question or counterexample are enough.

| Resource | Purpose |
| --- | --- |
| [Published -02](https://datatracker.ietf.org/doc/draft-sergeev-claim-boundaries/02/) | The authoritative IETF revision |
| [Document and revision history](https://datatracker.ietf.org/doc/draft-sergeev-claim-boundaries/) | Official status and subsequent posted revisions |
| [Published HTML](https://www.ietf.org/archive/id/draft-sergeev-claim-boundaries-02.html) | Read the published document in a browser |
| [Working RFCXML](draft-sergeev-claim-boundaries.xml) | The single editable manuscript source |
| [Frozen XML/TXT and checksums](published/02/) | Published baseline for comparisons |
| [Issues](https://github.com/Witnessability/cbee-spec/issues) / [pull requests](https://github.com/Witnessability/cbee-spec/pulls) | Questions, counterexamples, and proposed changes |
| [Contribution guidance](CONTRIBUTING.md) | Review, attribution, and applicable IETF contribution terms |
| [Revision preparation and submission](PUBLICATION-PROCESS.md) | Review, preflight, exact-file approval, and publication verification |

Feedback by email is equally welcome; GitHub participation is optional.
Repository merges record editorial decisions, without implying contributor
endorsement or a working-group decision.

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

## Edit and review

Edit `draft-sergeev-claim-boundaries.xml` for manuscript changes. Keep a focused
change, identify the affected section or XML anchor, and explain how the
wording changes the claim or its evidence boundary. Follow
[CONTRIBUTING.md](CONTRIBUTING.md) when opening a pull request.

The files under `published/02/` are frozen. Check their integrity locally with:

```sh
cd published/02
sha256sum -c SHA256SUMS
```

Render working TXT/HTML with xml2rfc into a local build directory, recording
the formatter version and commands used. Generated renderings are review aids;
the root XML remains the manuscript source. The publication checklist in
[PUBLICATION-PROCESS.md](PUBLICATION-PROCESS.md) covers the current preflight
and exact files required for an author's submission decision.

## Revision policy

Preserve already posted revisions under `published/NN/`. A future revision
gets its own identity and archive; preparing it does not change the -02
snapshot. The IETF archive is authoritative for posted revisions.

Submission requires the author's decision for the exact package and intended
actions. A GitHub release, when separately authorized, records a revision
already posted by the IETF. This repository currently has no build, submission,
or release workflow; the documented manual process applies.

The repository history begins with the published -02 files and the public
contribution process. Earlier private Git history and correspondence are not
part of this home. See [LICENSE.md](LICENSE.md) for the document notices.
