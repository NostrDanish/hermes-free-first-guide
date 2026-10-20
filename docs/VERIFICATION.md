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
- **22 offline tests passed**, plus **9 real-CLI integration checks** across **19 discovered auxiliary slots**. Both downloadable archives were extracted and their entrypoints exercised; the setup kit's offline tests also passed after extraction.
- The portable skill passed the generic skill frontmatter validator. Rebuild its archives with `python3 scripts/package_setup.py` after editing.
- Setup does not need the visual-rendering pip dependencies. Platform validation was performed on Linux; native Windows/macOS remain untested.

## Expanded full-stack edition

- The complete PDF contains 31 pages with selectable text and 97 explicit link annotations; its 18 numbered chapters include Hermes basics, Nous Portal Free, OpenRouter, FreeLLMAPI, other installed provider families, additional upstream signup paths, and using APIs outside Hermes.
- The eight overview cards were rebuilt around that broader stack. Their PDF is a quick-start companion, not the whole handbook.
- Current Nous/OpenRouter catalogs were read without credentials. The Nous public catalog contained seven explicitly zero-priced, tool-advertising free routes at the check.
- The default-provider configuration was inspected only for non-secret provider/endpoint/model metadata. FreeLLMAPI was running and required authentication; local Ollama model listing responded. This is not an authenticated gateway completion test.
- 74 external handbook source links were checked: 70 returned HTTP 200 in the raw checker; four had redirect/bot-wall/rate-limit behavior. The Mistral and Cloudflare login pages were recovered through web extraction; both Nous pages had already supplied their live content earlier in the run. `docs/LINK-CHECKS.json` preserves the results rather than claiming all requests returned 200.
- Bash snippets and Python examples passed syntax checks. Text extraction checked the expanded provider sections. Rendered Nous, FreeLLMAPI, and dense provider-matrix pages were opened for visual review, alongside the full card contact sheet.
- The helper now supports explicit `--provider nous` and `--provider openrouter` presets. Both were applied and read back in disposable homes; repeat application and rollback checks passed. Generic gateway chains still require a separate entitlement audit.

## Not tested / not included

No fresh OS installation, authenticated benchmark of every suggested model, new local-model download, new Jev installation, live paid-escalation failure test, or real Telegram upload/compression test was performed. No automatic paid dispatcher is implemented. No CI workflow, public deployment, public release, or collaborator invitation is included.

The setup commands are instructions for readers, not changes applied to the author's active Hermes configuration. Availability, billing terms, and quotas can change after the source-check date of 20 October 2026.
