# Verification and scope

## Source guide

- Official Hermes setup/configuration/fallback/cron/local-model documentation was retrieved.
- OpenRouter public model catalog was queried for zero listed pricing and advertised tool support.
- All 31 distinct shared source URLs returned HTTP 200 at the original check.
- Fifteen core configuration writes ran against a disposable `HERMES_HOME`; resulting YAML types and settings were asserted.
- The exact public catalog-discovery example ran successfully. Shell snippets passed Bash syntax checks and the YAML example parsed.

## Visual pack

- Eight PNGs at 1080 × 1350 pixels.
- Eight-page PDF with ten explicit resource-link annotations.
- Font-width wrapping and page-boundary assertions passed.
- Numbered card count, image integrity, PDF signature/page count, and ZIP integrity checked.
- A contact sheet and an actual rendered PDF page were opened for visual inspection.
- The portable repository build is exercised before the initial push.

## Setup helper and portable skill

- Offline regression tests cover explicit zero-price/tool validation, route resets, profile scope, required apply consent, network-failure refusal, unknown upstream routing refusal, rollback, backup permissions, locks/symlinks, CLI value serialization, and skill/package contracts.
- Real installed Hermes CLI was exercised only against disposable data homes: preview, initial apply, read-back, repeat application with identical config bytes, private backup equality, preservation of unrelated settings, and unchanged fixture `.env`/`auth.json` files.
- An injected failure during real CLI writes restores the original config and releases the setup lock.
- The skill includes three review scenarios; they are specifications, not a model-vs-model benchmark.
- **21 offline tests passed**, plus **7 real-CLI integration checks** across **19 discovered auxiliary slots**. Both downloadable archives were extracted and their entrypoints exercised; the setup kit's offline tests also passed after extraction.
- The portable skill passed the generic skill frontmatter validator. Rebuild its archives with `python3 scripts/package_setup.py` after editing.
- Setup does not need the visual-rendering pip dependencies. Platform validation was performed on Linux; native Windows/macOS remain untested.

## Not tested / not included

No fresh OS installation, authenticated benchmark of every suggested model, new local-model download, new Jev installation, live paid-escalation failure test, or real Telegram upload/compression test was performed. No automatic paid dispatcher is implemented. No CI workflow, public deployment, public release, or collaborator invitation is included.

The setup commands are instructions for readers, not changes applied to the author's active Hermes configuration. Availability, billing terms, and quotas can change after the source-check date of 20 October 2026.
