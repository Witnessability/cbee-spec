# Contributing

Questions, counterexamples, and proposed wording are welcome through an issue,
a pull request, or [email to the editor](mailto:mikhailsergeev369@gmail.com).
GitHub participation is optional.

## A useful contribution

Identify the draft revision and section or XML anchor. State the claim under
review, the evidence offered for it, and the boundary or assumption that needs
clarification. A short example and links to public sources help the editor
assess the proposal. You do not need an implementation or a patch to contribute.

For manuscript edits, change only `draft-sergeev-claim-boundaries.xml` and keep
the pull request focused on one issue. Describe the reason for the change and
the checks performed. Run `make review`, `make check`, `make test`, and,
with the formatter installed, `make build`. Include the regenerated
`review/editor-copy.md` in the PR; do not hand-edit it or the TXT/HTML outputs.
Keep every frozen `published/NN/` XML/TXT and checksum file unchanged.
Working renderings are review aids, rather than additional editable sources.

Use a short-lived topic branch for a focused change. After review and successful
checks, merge it into `main` and remove the merged branch. Published revisions
use immutable tags and archive directories, not long-lived release branches.

The editor records dispositions and retains material disagreement. A merge
does not establish IETF consensus, implementation behavior, or permission to
submit a new revision. See [PUBLICATION-PROCESS.md](PUBLICATION-PROCESS.md).

## IETF contribution terms

This repository develops an individual Internet-Draft. Material intended as
an IETF Contribution remains subject to the applicable IETF terms. Please read
the [IETF Note Well](https://www.ietf.org/about/note-well/),
[BCP 78](https://www.rfc-editor.org/info/bcp78),
[BCP 79](https://www.rfc-editor.org/info/bcp79), and the
[IETF Trust Legal Provisions](https://trustee.ietf.org/license-info).
Contribute material you are entitled to provide under those terms.
The manuscript retains its document notices; [LICENSE.md](LICENSE.md) also
identifies the separate BSD 3-Clause license for repository tooling.
There is no additional repository CLA or signed editorial form.

## Attribution and privacy

Preserve substantive attribution and the agreed scope of a contributor's
text. Discuss changes to authorship explicitly with the people concerned;
reviews and commit counts do not confer authorship or endorsement.

Use public references for public discussion. Keep private correspondence,
unpublished partner text, credentials, and sensitive operational evidence out
of issues and pull requests unless disclosure has been authorized. If an
example needs sensitive material to make its point, discuss a safe way to
present it with the editor first. Follow the participation guidance linked
from the IETF Note Well.


## External reports and dispositions

See [ISSUE-PROCESS.md](ISSUE-PROCESS.md) for response targets, review,
public dispositions, closure, and the distinction between working changes
and a posted I-D. Questions by issue or email are welcome without a patch.
