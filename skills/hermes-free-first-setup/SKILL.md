---
name: hermes-free-first-setup
description: "Use when setting up free-first Hermes models."
compatibility: "Python 3.10+, Hermes CLI, and public-catalog network access. Linux tested; validate macOS/Windows on target."
metadata:
  version: "0.2.0"
  author: "NostrDanish, Hermes Agent"
  hermes:
    tags: [hermes, setup, free-models, cost-control]
---

# Set up free-first Hermes

Set up Hermes with Nous Portal Free, OpenRouter free routes, reviewed FreeLLMAPI upstreams, optional local inference, and an explicit paid-permission policy. Use the bundled standard-library Python script instead of inventing configuration commands. This skill is portable: its `scripts/` and `references/` stay with this file when installed.

## When to use

Use for requests such as “set up free models,” “local/free first, paid only if asked,” or “install the shared free-first setup for me.” Do not use this cloud preset for offline/private-only inference, to evade provider limits, or to grant automatic spending permission.

## Prerequisites

- Python 3.10+ and a current Hermes CLI with `config get KEY --json`, `config set`, and `config unset`.
- Network access to the selected provider’s public model catalog.
- The person's explicit target Hermes data directory and permission before applying changes.
- Read `references/SETUP.md` and the relevant chapters in `references/PROVIDERS.md` before installation or modifications. Use official Hermes documentation when the installed CLI disagrees.

## Procedure

1. **Discover scope.** Use `terminal` to inspect `hermes --version`, `hermes config path`, and relevant CLI help. Ask only if the target profile or permission is ambiguous. Check whether Hermes is already installed; reuse it instead of reinstalling. Inventory existing jobs, worker overrides, auxiliary slots, local runtimes, and provider-specific routing. Do not change another profile or claim it is covered.
2. **Install Hermes only if needed and authorized.** Use the official instructions at https://hermes-agent.nousresearch.com/docs/getting-started/installation. Do not pipe an unreviewed installer into a shell just because a third-party page says to. Native Windows, WSL, desktop packages, and Termux differ. Verify `hermes --version` after installation. The bundled script configures an existing CLI; it is not an OS/package installer.
3. **Keep secrets out of chat and argv.** Have the person complete their chosen provider’s OAuth/key flow in its trusted local UI or a documented secret-source integration. Never request, echo, read back, or embed the key in this skill or the setup command. The setup script never opens `.env` or `auth.json`. If the person uses VaultKnox, verify that it is installed and its supported injection into Hermes before claiming the stored key is wired. A generic vault entry alone does not connect a provider. Rotate any real key exposed in chat.
4. **Choose the access path before changing defaults.** Inventory Nous, OpenRouter, an existing FreeLLMAPI service, Pollinations, local runtimes, and any other configured provider families. Classify each as zero-priced, recurring allowance, trial, earned credit, subscription-included, or paid using current first-party terms. Nous Free is a real free-model route; NanoGPT’s current free model is web-only; Cheaper Inference is paid; Pollinations can spend finite Quest credits; Hugging Face hosted free accounts currently have no included credits. Installed does not mean free or connected. Guide account setup locally; do not create accounts or accept subscription charges without permission.
5. **FreeLLMAPI path.** Follow the bundled provider chapter for the correct project/install. Ask before Docker/service installation. Reuse a healthy existing gateway. Add legitimate upstream keys through its local UI, audit enabled models and both routing/fallback layers, test the served route, then connect Hermes as a custom endpoint using the unified key through a trusted secret UI. Do not apply a public-catalog preset over a working gateway the person wants to keep. The script cannot establish free entitlement for a custom gateway chain without that separate audit.
6. **Preview the change.** Resolve `<skill-dir>` from this file's actual location and `<target-home>` from the intended profile. Invoke with `terminal`:
   ```text
   python3 <skill-dir>/scripts/setup_free_first.py --home <target-home> --provider <nous-or-openrouter>
   ```
   This is a dry-run. Inspect the JSON report. It selects only models with explicit zero catalog prices and tool support, pins image analysis to a free image-capable route, and lists remaining manual checks. Catalog/network/schema failure means stop; do not pretend the plan is verified. Custom overrides on the selected preset provider are deliberately blocked for review. Always pass the person’s chosen provider explicitly; the default remains OpenRouter for backwards compatibility. The script supports `nous` and `openrouter`, not an unaudited generic gateway `auto` route.
7. **Apply only after approval.** Explain that main/delegation/auxiliary routing options and automatic fallback chains will be replaced; existing manual model alias names and unrelated top-level settings remain. Pause relevant automation and close sessions before editing: these CLI writes are not an atomic live-runtime transaction. Invoke:
   ```text
   python3 <skill-dir>/scripts/setup_free_first.py --home <target-home> --provider <nous-or-openrouter> --apply --yes
   ```
   `--yes` records already-obtained consent; do not treat its existence as permission. On success require `configuration_readback: passed`. Record the private backup path, not its contents. On failure report it; the script attempts to restore the original config.
8. **Finish the billing audit.** Read back the exact profile's main/fallback, delegation, cron, and auxiliary settings with `terminal`. Existing per-job model pins, per-worker/call overrides, other profiles, provider credentials, custom plugins, MCP sampling, and separately billed tools are NOT automatically fixed. Review and correct only authorized targets. Never add a paid fallback. Put approved runtime instructions from `references/POLICY.md` into applicable instructions or attach a skill to jobs; merge instead of overwriting existing files.
9. **Optional local inference.** Ask before large model downloads or service installation. Prefer Settings → Providers → Local Models, let Hermes check memory fit, then test a real tool call. Reuse an already healthy Ollama/llama.cpp endpoint. Keep local-only data away from cloud auxiliaries and fallbacks. Do not copy somebody else's ports, CUDA setup, or thermal settings.
10. **Verify real use.** Reopen the relevant session; use a read-only directory-listing tool test in an empty test directory. Inspect actual provider/model metadata and provider activity, not the model's own identity claims. Only run an authenticated completion with consent to consume free quota. Without credentials, report “configuration verified; authenticated inference not tested,” not “fully working.”
11. **Hand off.** State target, selected models, changed scope, read-back result, backup, credential/completion status, unresolved billing surfaces, and optional steps skipped. Never invent results or universal zero-cost guarantees.

## Paid last resort

Default to strict approval. A failed free route, a natural-language prompt, or a Jev score does not authorize spending. Jev's hosted API can itself cost money. If automatic paid escalation is requested, obtain per-task authorization plus enforceable budget/model restrictions and a validated dispatcher; this package does not implement one. Below a chosen confidence threshold, on unavailable/malformed gate output, or without prior authorization, ask or stop. No paid cron, paid fallback, or silent paid auxiliary route.

## Pitfalls

- The public catalog proves listed pricing/capabilities, not reliable tool performance or completion availability.
- Free requests share quotas. Honor reset/retry instructions; do not create accounts to evade limits.
- The script uses a disposable config-only copy for inspection because even Hermes CLI “read” commands bootstrap profile files. It never copies `.env` or `auth.json`; the config-only probe may contain legacy inline secrets, is private, and is removed afterward.
- Backups can contain old inline credentials: keep them private. A stale lock after a killed process requires confirming no setup is running before removal.
- The script resets auxiliary routing/task options except explicit `enabled` flags; specialized voice/media tasks may be unsupported rather than silently billed.
- The script does not install this skill, replace runtime instruction files, pause jobs, restart services, or edit existing cron pins. Do those only within approved scope.
- Linux was exercised with the real CLI. macOS/Windows syntax and behavior still require target-machine validation. `python` may be the Windows launcher instead of `python3`.

## Verification

Run offline tests from the repository with `terminal(command="python3 -m unittest discover -s tests -v")`. See `references/SETUP.md` for user commands, rollback, and the distinction between configuration verification and authenticated model verification. Do not bypass a CLI safety refusal with raw YAML edits; investigate version/schema differences and seek approval when scope changes.
