# Free-first setup: humans and AI agents

This package has two parts: a standard-library Python configuration script and a portable AI skill that handles discovery, installation guidance, credential handoff, optional local inference, and verification. It is not a hidden paid router or an unattended account-signup system.

## Quick start from the repository

Requires Python 3.10+ and Hermes on PATH. Install Hermes through its official instructions first if necessary: https://hermes-agent.nousresearch.com/docs/getting-started/installation. The setup script itself needs no pip packages, model API key, or paid model call.

First preview the intended profile explicitly:

```bash
python3 scripts/setup_free_first.py --home "$HOME/.hermes"
```

After reviewing the plan, stop relevant active automation/configuration editors and apply:

```bash
python3 scripts/setup_free_first.py --home "$HOME/.hermes" --apply --yes
```

The script defaults to dry-run. `--yes` is deliberately insufficient without `--apply`, and apply refuses without `--yes`. On Windows, use the available Python launcher and an explicit native Hermes data path; `$HOME` shell examples above are POSIX examples, not PowerShell instructions.

Use the actual target data directory, not the repository directory. Named profiles and remote backends have their own data homes; discover them rather than assuming the examples fit. When `HERMES_HOME` is set it is the default, otherwise the script defaults to `~/.hermes`. Explicit `--home` is recommended.

Choose a specific model only by its exact current catalog ID:

```bash
python3 scripts/setup_free_first.py --home "$HOME/.hermes" --model openrouter/free
```

The script verifies all listed price components are finite zero, checks advertised tool support, requires the free router to be available, and uses an image-capable free route for vision. If the preferred Nemotron free model is absent, it chooses the free router. A requested unavailable or priced model is rejected rather than normalized or silently substituted.

## What changes

- Main model/provider/endpoint/API mode and managed `free` / `freerouter` aliases.
- Main automatic fallback list; removes legacy `fallback_model`.
- Delegation routing: free model, no paid fallback, two concurrent children, no automatic subagent command approval.
- Cron fleet default model/provider; existing per-job pins are untouched.
- Every auxiliary task route discovered through the installed CLI, including compression, titles, approvals, vision, review, and maintenance tasks. Old custom endpoints, inline route credentials, extra request bodies, and per-task fallback chains are cleared. Explicit task `enabled` flags are retained; other task-specific settings are reset to defaults.
- `auxiliary.free_only` is enabled as an additional OpenRouter safeguard, not treated as a universal billing firewall.

Other top-level configuration remains. Existing manual alias names remain, so explicit paid aliases can still be selected. The script uses documented CLI section replacement (`--force` only for the deliberately replaced mapping sections), not YAML editing to bypass a refusal. It verifies the resulting values afterward.

Custom `providers.openrouter`, `provider_routing`, or top-level request overrides cause a stop for manual review. Do not delete credentials or disable safety mechanisms just to make that check pass.

## What does not change

The script does not install Hermes, create provider accounts, store/read API keys, open `.env`/`auth.json`, download models, install Jev/MCP, install the skill, modify runtime instruction files, edit pinned jobs/other profiles, pause services, or execute authenticated model completions. The skill guides those follow-ups within the person's permission.

Plugins, MCP sampling, per-call/worker overrides, cloud browser/search/image/speech services, and existing pinned cron jobs can still spend separately. Audit them. Specialized voice/media slots pinned to a free text model may be unsupported; this is not a promise of free multimodal feature compatibility.

## Credentials

Create a key through https://openrouter.ai/settings/keys and enter it only in a trusted local Hermes key/provider UI or a documented secret-source integration. Do not pass a secret as a setup flag, paste it into an AI chat, or commit it. If using VaultKnox or another vault, verify the installed adapter and injection path; storing a value in a generic vault is not enough to connect Hermes.

`hermes model` can authenticate a provider but also change the selected model. If you use it after applying this preset, deliberately select a verified free model, then preview/reapply the script if needed. Never assume the last wizard choice was free.

## Install/use the AI skill

The folder is `skills/hermes-free-first-setup/`. Copy that whole folder to the active agent's skill directory, keeping `SKILL.md`, `scripts/`, and `references/` together. Inspect it first. Refuse to overwrite an existing skill until its contents have been compared and the replacement approved.

For a POSIX Hermes default data directory, a guarded manual example is:

```bash
TARGET="${HERMES_HOME:-$HOME/.hermes}/skills/hermes-free-first-setup"
test ! -e "$TARGET" && mkdir -p "$(dirname "$TARGET")" && cp -R skills/hermes-free-first-setup "$TARGET"
```

No shell command here installs into every profile. Start a new agent session to discover it. Other AI clients can load the same `SKILL.md` and run its bundled Python helper; they do not need Hermes' own skill tools, but the machine still needs the Hermes CLI being configured.

Alternatively, while inside the cloned repository, give an AI this prompt without installing a skill globally:

> Read `skills/hermes-free-first-setup/SKILL.md`. Set up free-first Hermes for me using the bundled script. Discover my installation and intended profile. Show the dry-run first, obtain permission before applying, keep secrets out of chat, audit background billing, and verify an actual tool call. Do not enable automatic paid escalation.

The private repository requires access. The downloadable skill ZIP can be handed to someone without sharing repo permissions. Extract it and review the files; this is a portable folder archive, not a claim that every AI client has a universal ZIP importer.

## Backups and rollback

Existing config is copied before changes to a private file under the target home's `backups/free-first/<unique-id>/config.yaml`. The report gives its exact path. Permissions are restricted on POSIX; keep the backup private because old configs may contain inline credentials. Windows ACLs depend on the owning user's data directory.

On command failure, failed read-back, or a catchable interruption, the script attempts to restore the exact original config. For a fresh home it removes the partial config. It does not undo Hermes' incidental cache/bootstrap files. CLI writes are sequential, not atomic to running gateways. Stop the relevant automation before applying.

To restore later, stop relevant services/editors, inspect the private backup locally, and copy the selected backup back over that target's `config.yaml`. Preserve it as a private file. Restart/reopen the relevant session and read back the intended settings. Do not copy a backup from another profile or use raw edits to evade an unrelated security refusal.

A forced process kill/power loss cannot be rolled back automatically. If a setup lock remains, confirm no setup process is still running before removing it. The lock coordinates this installer only; it does not lock every other Hermes process or editor.

## Verification

The JSON report distinguishes configuration read-back from actual model use. Successful configuration does not prove the key, quota, provider availability, tool reliability, or zero external-tool spend.

After credentials and the intended free model are selected, ask in an empty test directory:

> Use a terminal or file tool to list this directory. Report the actual tool result. Do not modify files.

Check actual provider/model metadata and https://openrouter.ai/activity. Do not trust generated identity claims. This request consumes free quota. If it was not run, say so.

Offline regression tests from the repository:

```bash
python3 -m unittest discover -s tests -v
```

The optional real-CLI integration test is in `tests/integration_setup.py`. It uses only disposable data homes and the public model catalog; no credentials or inference. Linux was exercised here. Native macOS/Windows behavior needs target-machine validation.

## Useful references

- https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models
- https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers
- https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
- https://hermes-agent.nousresearch.com/docs/user-guide/local-models
- https://hermes-agent.nousresearch.com/docs/user-guide/secrets
- https://openrouter.ai/docs/guides/routing/routers/free-router
- https://openrouter.ai/docs/api/reference/limits
