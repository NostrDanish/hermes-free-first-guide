# Hermes Agent: the Free-First Setup Guide

**Local when useful. Free cloud for the heavy lifting. Paid only by explicit choice—or a deliberately approved, tightly bounded last resort.**

A shareable, independent setup guide. Documentation and OpenRouter catalog checked **20 October 2026**. Model availability, limits, and UI labels can change. This is not a promise of unlimited free inference.

## Contents

1. The strategy and what “free” means
2. Install Hermes
3. Connect OpenRouter and choose a free model
4. Configure free-only fallbacks and aliases
5. Add optional local models
6. Keep background work and auxiliary calls free
7. Install the routing policy
8. Use paid models deliberately
9. Optional Jev decision gates
10. Verify the setup
11. Troubleshooting and privacy
12. Links and maintenance

---

## 1. The strategy

Use this ladder:

```text
Can an ordinary command or script do it reliably?
  YES → run the command/script. No LLM needed.
  NO  → does a suitable local model handle it acceptably?
          YES → local model.
          NO  → capable free cloud model.
                  ↓ service failure
                another explicitly free route, or wait/local/stop.
                  ↓ task still fails objective checks
                ask before paid inference.
```

**The free cloud model can still be your everyday default.** “Local first” does not mean forcing every request through a weak or slow local model before allowing a better free model. Use local for private material and small, repeatable jobs; use free cloud directly for demanding agent work.

### Three different kinds of “free”

| Route | What it actually means | Trade-off |
|---|---|---|
| Local model | No hosted inference bill; runs on your hardware | Electricity, hardware, storage, and speed still matter |
| Free cloud model | Provider currently lists the route at zero price | Quotas, availability, and third-party data handling |
| Subscription/OAuth model | Included in an existing plan or allowance | Not universally free; subscription and usage limits still exist |

An open-weight model is not automatically free to access through somebody else's API. A free browser playground is not necessarily a free API. Promotional credits are not permanent free service.

### Pick the spending mode

**Recommended: strict approval.** Paid models run only when you explicitly select or authorize one. Exhausted free quota means wait, go local, or ask—not silently spend.

**Optional: preauthorized last resort.** You may later authorize a bounded escalation mechanism for a specific task. That requires enforcement outside an ordinary prompt: allowed models, provider-side spending limits, validation, and an audit trail. A confidence score alone is not spending permission.

**These are separate mechanisms:**

- **Fallback:** switches routes after an API/service error.
- **Quality escalation:** moves to a stronger model after a result fails tests or other objective checks.

Hermes' fallback chain is not a judge of whether an otherwise successful answer was correct.

## 2. Install Hermes

Official project: <https://github.com/NousResearch/hermes-agent>

Installation instructions: <https://hermes-agent.nousresearch.com/docs/getting-started/installation>

### Desktop

Download from <https://hermes-agent.nousresearch.com/> and follow the instructions for your platform. You do not need an expensive GPU for free cloud models.

### Linux, supported macOS, or Windows through WSL2

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

This executes downloaded code. Review the installer first if that does not match your security policy. Do not run the installer as root merely for convenience. Follow the installer's shell/PATH instructions or reopen your terminal.

Then:

```bash
hermes --version
hermes setup
hermes doctor
```

Native Windows and Termux have separate installation paths in the official docs. The shell examples below target Bash on Linux/macOS/WSL; use the desktop UI where shell syntax differs.

### Existing installation? Back up first

Find your active files:

```bash
hermes config path
hermes config env-path
```

On a POSIX shell:

```bash
HERMES_DATA="${HERMES_HOME:-$HOME/.hermes}"
cp -p "$HERMES_DATA/config.yaml" "$HERMES_DATA/config.yaml.before-free-first"
```

Keep that backup private: older configurations might contain credentials. Do not share your whole Hermes directory, `.env`, `auth.json`, logs, or session database.

These changes affect the active profile. Other profiles, remote gateways, and existing pinned jobs have their own settings; audit them separately.

## 3. Connect OpenRouter and choose a free model

### Create your own key

1. Open <https://openrouter.ai/> and create an account.
2. Create a key at <https://openrouter.ai/settings/keys>.
3. In a real terminal, run `hermes model` and choose **OpenRouter**, or add the key through Hermes' provider/key settings.
4. Enter the key only in the trusted local setup UI—not in an AI chat, screenshot, shared config, or public repository.
5. Choose a free model from the picker, or use its exact model ID.

Hermes normally stores API credentials in its `.env` credential file; settings go in `config.yaml`. External secret-manager integration is optional: <https://hermes-agent.nousresearch.com/docs/user-guide/secrets>.

A generic browser password vault does not automatically wire a provider key into Hermes. Use the provider setup flow or a documented secret-source integration.

### Suggested starting model

The following model was listed with zero prompt/completion price and tool support in the live OpenRouter catalog when this guide was checked:

```text
nvidia/nemotron-3-ultra-550b-a55b:free
```

Model page: <https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b:free>

After authenticating through the wizard, these commands make the selection explicit:

```bash
hermes config set model.provider openrouter
hermes config set model.default 'nvidia/nemotron-3-ultra-550b-a55b:free'
hermes config set model.base_url 'https://openrouter.ai/api/v1'
```

Open a **new chat** afterward. An existing chat may retain its earlier model until you switch it explicitly.

This is a starting choice, not a permanent “best model” claim or a successful inference benchmark. If it disappears, use the discovery steps below.

### Prefer not to choose a specific model?

Use **OpenRouter's Free Models Router**:

```text
openrouter/free
```

Docs: <https://openrouter.ai/docs/guides/routing/routers/free-router>

It filters for request capabilities, then randomly selects from eligible free models. It is not a guaranteed best-model selector. It can be convenient for starting out; a fixed model is easier to evaluate and troubleshoot.

**Do not confuse `openrouter/free` with `openrouter/auto`. The auto router is not a free-only guarantee.**

### Find currently free, tool-capable models

Browse <https://openrouter.ai/models?pricing=free>.

For a machine-readable check, run this in a terminal with Python 3. It queries the public catalog without an API key and makes no inference requests:

```bash
python3 - <<'PY'
import json
from decimal import Decimal, InvalidOperation
from urllib.request import urlopen

with urlopen('https://openrouter.ai/api/v1/models', timeout=30) as response:
    models = json.load(response)['data']

for model in sorted(models, key=lambda item: item['id']):
    pricing = model.get('pricing', {})
    if not {'prompt', 'completion'} <= pricing.keys():
        continue
    try:
        free = all(Decimal(str(value)) == 0 for value in pricing.values())
    except (InvalidOperation, ValueError, TypeError):
        continue
    tools = 'tools' in model.get('supported_parameters', [])
    if free and tools:
        print(model['id'], 'context:', model.get('context_length', '?'))
PY
```

Checking every listed price avoids assuming that zero text-token prices imply zero price for every other listed component. Catalog metadata still does not establish availability, reliable tool use, or zero cost for separately enabled plugins/tools.

Other entries observed in the checked catalog included:

- `poolside/laguna-s-2.1:free`
- `nvidia/nemotron-3-super-120b-a12b:free`
- `google/gemma-4-31b-it:free`
- `minimax/minimax-m3.1-flash:free`

Do not append `:free` to an arbitrary paid model and assume it works. The exact free variant must exist in the catalog.

### Understand the quotas before you build automations

At verification time, OpenRouter's published free-variant limits were:

| All-time credits purchased | Requests/minute | Requests/day |
|---|---:|---:|
| Less than 10 credits | 20 | 50 |
| At least 10 credits | 20 | 1,000 |

Check your actual account at <https://openrouter.ai/docs/api/reference/limits>; exceptions and policy changes can apply. A credit purchase is **optional and costs money**—it is not necessary to describe the basic setup as free. More keys/accounts do not bypass the shared limits.

**One agent task can consume many requests:** tool loops, compression, retries, and subagents all add traffic. Fifty requests does not mean fifty substantial coding tasks.

## 4. Configure free-only fallbacks and aliases

### Convenient names

```bash
hermes config set model.aliases.free 'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free'
hermes config set model.aliases.freebackup 'openrouter/poolside/laguna-s-2.1:free'
hermes config set model.aliases.freerouter 'openrouter/openrouter/free'
```

The doubled `openrouter/openrouter/free` is intentional: the first part names the Hermes provider; the remaining `openrouter/free` is the OpenRouter model ID.

Inside a chat:

```text
/model free
/model freebackup
/model freerouter
```

### Free-only fallback chain

The interactive route is:

```bash
hermes fallback
```

Choose only verified free routes. Inspect the result:

```bash
hermes fallback list
```

Or set this explicit starter chain with the CLI:

```bash
hermes config set fallback_providers '[{"provider":"openrouter","model":"poolside/laguna-s-2.1:free"},{"provider":"openrouter","model":"openrouter/free"}]'
```

**That command replaces your existing chain.** Back it up first and retain any needed local/free entries deliberately. Check any legacy entry as well:

```bash
hermes config get fallback_providers
hermes config get fallback_model
```

If an old `fallback_model` is unwanted, remove it:

```bash
hermes config unset fallback_model
```

**Never add a paid model “at the end just in case.”** Automatic error fallback does not wait for a natural-language instruction to approve spending. The same rule applies to an upstream proxy/router's own fallback configuration.

All these cloud fallbacks still share OpenRouter's account-level quota. They help with individual model outages, not an exhausted daily allowance. A local fallback or another legitimately available free provider is a separate route.

Docs: <https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers>

## 5. Add optional local models

You can skip this entire section and use free cloud models without local hardware investment.

### Easiest: Hermes-managed llama.cpp

1. Open **Settings → Providers → Local Models**.
2. Click **Install runtime**.
3. Choose a tool-capable model the memory-fit indicator says will fit your machine.
4. Download it and click **Use**.
5. Open a new chat and perform the real tool test in section 10.
6. To keep free cloud as your daily default, select OpenRouter again afterward.

The terminal equivalent begins with `hermes model` → **Local models**.

Docs: <https://hermes-agent.nousresearch.com/docs/user-guide/local-models>

Hermes manages engine selection, GPU offload, and model fitting. This is the simplest cross-vendor path; do not install CUDA on an AMD system. Do not copy somebody else's VRAM, context, port, or thermal settings blindly.

The managed provider is `llamacpp`. To add a local alias, copy the **exact installed model ID** shown by Hermes:

```bash
hermes config set model.aliases.local 'llamacpp/EXACT_INSTALLED_MODEL_ID'
```

`EXACT_INSTALLED_MODEL_ID` is a placeholder; replace it before running the command. Then `/model local` selects it. The alias selects a model; it is not by itself proof that the local runtime is configured and running.

You may also add the installed model using `hermes fallback add` → the local provider. Remember: cloud fallback from a local primary sends conversation data off the machine. Leave cloud fallbacks out of an offline/private profile.

### Already using Ollama?

Reuse it instead of installing a second inference stack.

- Download: <https://ollama.com/download>
- Model library: <https://ollama.com/library>
- Hermes manual guide: <https://hermes-agent.nousresearch.com/docs/guides/local-ollama-setup>

Check the service:

```bash
ollama --version
ollama list
curl --fail-with-body http://127.0.0.1:11434/api/tags
```

Use Hermes' **Custom Endpoint** setup with:

```text
Base URL: http://127.0.0.1:11434/v1
Model:    the exact model ID from ollama list
API key:  empty or a dummy value if the setup screen requires one
```

The usual Ollama port is `11434`; a particular installation may use something else. Discover the actual endpoint rather than copying a custom port from another person's machine. Do not start a competing server on an occupied port.

A model being good at code generation does not establish reliable structured tool calling. Also check the configured context window: model weights fitting in VRAM does not mean a long agent prompt plus KV cache will fit. Start with a small tool-capable model and measure.

**Keep local servers bound to loopback unless you intentionally secure LAN access.** An unauthenticated local endpoint should not be exposed to the internet.

## 6. Keep background work and auxiliary calls free

Your main chat model is not the only possible source of charges.

### Audit these places

| Component | Free-first rule |
|---|---|
| Main model | Explicit free or local provider/model |
| Main fallback chain | Free/local entries only |
| Compression, titles, vision, approvals, MCP helpers | Inspect assignments and per-task fallback chains |
| Delegated subagents | Pin free/local or enforce safe inheritance |
| Cron fleet default | Pin independently from interactive chat |
| Individual cron jobs | Inspect existing provider/model pins |
| Other profiles and Kanban workers | Audit their own defaults and per-task overrides |
| MCP sampling and third-party plugins | Check model overrides, independent billing, and external API costs |
| Search, images, cloud browsers, speech, memory services | Separate services can cost money even with a free chat model |

### Subagent default

A conservative starting point:

```bash
hermes config set delegation.provider openrouter
hermes config set delegation.model 'nvidia/nemotron-3-ultra-550b-a55b:free'
hermes config set delegation.fallback_providers '[]'
hermes config set delegation.max_concurrent_children 2
```

Here `[]` deliberately disables the delegation fallback chain. You can add tested free-only backups later. Explicit per-call or worker overrides still need auditing. Parallel children consume quota faster, so start small.

### Cron fleet default

```bash
hermes config set cron.model_provider openrouter
hermes config set cron.model 'nvidia/nemotron-3-ultra-550b-a55b:free'
hermes cron list
```

This keeps unpinned cron jobs on the chosen free model even while you manually use a paid model in chat. It does **not** overwrite already pinned jobs.

For one existing job:

```bash
hermes cron edit JOB_ID --provider openrouter --model 'nvidia/nemotron-3-ultra-550b-a55b:free'
```

Replace `JOB_ID` with the real identifier. A pinned cron job does not use the general model fallback chain under the currently documented behavior; a failed free route should fail rather than spend elsewhere.

For deterministic checks, prefer `--no-agent` script jobs. Example shape, after you have created and tested the script under your active Hermes data directory's `scripts/`:

```bash
hermes cron create 'every 1h' --name disk-check --script disk_check.py --no-agent --deliver local
```

The script must already exist. Empty stdout is silent; stdout is delivered without an LLM. Do not schedule a model to ask whether a file changed when a file comparison can answer directly. Agent-backed scheduled execution needs the gateway running; see the cron docs for your deployment.

Docs: <https://hermes-agent.nousresearch.com/docs/user-guide/features/cron>

### Auxiliary models

Open the Models settings and expand **auxiliary**. Inspect all slots—not just compression. Current docs say `auto` first uses the configured main route, follows explicitly configured fallback policy, and does not invent another logged-in provider when a main provider is explicitly selected.

But if you manually switch the main chat to a paid model, `auto` may follow it. **Pin the auxiliary slots you want to remain free independently.** Clear stale custom endpoints/credentials when changing routes; the picker handles this more safely than changing only a model string.

Example for compression on a clean slot:

```bash
hermes config set auxiliary.compression.provider openrouter
hermes config set auxiliary.compression.model 'nvidia/nemotron-3-ultra-550b-a55b:free'
```

Repeat through the UI for titles and other relevant tasks. Vision needs an actually vision-capable route; if none is available free, fail or ask rather than silently use a paid vision model.

Docs: <https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models>

## 7. Install the routing policy

Save the following instructions in your applicable global/project instructions or ask Hermes to create a `free-first-routing` skill and attach it to relevant automations. Context-file behavior is documented at <https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files>.

**Merge with existing instructions; do not overwrite your whole `SOUL.md` or `AGENTS.md`.** A project file alone will not automatically govern unrelated cron jobs and every other profile.

### Copyable strict-approval policy

```text
FREE-FIRST MODEL POLICY

1. Prefer deterministic tools/scripts when they solve the task reliably.
2. Use a suitable local model for private data and small repeatable work.
3. Use the configured free cloud model for other work. Local is not a
   mandatory extra hop before a capable free model.
4. Use only verified free/local routes in automatic fallback chains.
5. Verify results with tests, real tool output, or other objective checks.
   Do not equate an HTTP success with a correct answer.
6. On transient failures, honor Retry-After and retry at most twice.
   On exhausted daily quota, wait, go local, or ask. Do not rotate keys
   or accounts to evade limits.
7. After a failed quality check, try one materially different free/local
   approach if useful. Do not loop endlessly through the same failure.
8. Never invoke a paid model unless I explicitly choose or authorize it.
   A router confidence score does not grant permission to spend.
9. Keep cron, subagents, auxiliary models, and external tool APIs within
   the same policy. Never silently send private/local-only data to cloud.
10. Before paid use, name the provider/model, explain the failed free
    alternatives, and state the allowed scope and spending ceiling.
    If cost cannot be estimated, say so.
11. After authorized paid work, return to the free default. Do not change
    global defaults or recurring jobs to paid as a side effect.
12. If no compliant route works, stop with an honest blocker. Never invent
    execution results to make the free route look successful.
```

**This is behavioral guidance, not a billing firewall.** The stronger controls are free-only model selections, independent background pins, provider-side budgets/model restrictions where supported, and separation from paid credentials.

For the strongest practical spending separation, keep paid access in a different Hermes profile or separate deployment. Merely adding aliases does not restrict what a fully privileged process can do. A profile is organizational separation, not an OS security sandbox; review shared secret sources and use a separate OS user/container if hard isolation matters.

Profiles: <https://hermes-agent.nousresearch.com/docs/user-guide/profiles>

## 8. Use paid models deliberately

You do not need to configure a paid provider to complete the free setup.

If you want one later:

1. Connect it through `hermes model` using your own account.
2. Verify its exact model ID, billing terms, and limits.
3. Do not add it to any automatic fallback list.
4. Prefer a separate paid profile, or explicitly select it for a bounded session/task.
5. Return to `/model free` afterward if using the same profile.

An existing ChatGPT, Copilot, or other subscription can offer an included route, but it is still a subscription—not universally free API access. Do not assume any service accepts another service's OAuth token.

Optional alias pattern:

```bash
hermes config set model.aliases.paidreview 'PROVIDER/EXACT_MODEL_ID'
```

Both parts are placeholders. Configure the provider first and replace them with real supported values. Then select `/model paidreview` deliberately.

A useful authorization looks like:

> Use my configured paid reviewer for this one review only. Do not change defaults or cron jobs. Keep total spend within my provider-side budget; if you cannot establish the cost, ask before proceeding.

**Avoid promising an exact dollar ceiling based on a prompt alone.** Enforce budgets at the provider or an explicitly budget-aware dispatcher. Long-context model switches can trigger a full uncached reread of the conversation.

## 9. Optional Jev decision gates

Jev supplies typed judgments—yes/no, a choice, or a score. It can help decide:

- whether a failure appears transient from the supplied evidence;
- whether a result passed a stated quality rubric;
- whether to retry, stop, or request human review;
- which allowed free/local route is appropriate.

It does not inspect your machine by magic. Gather logs, test results, and task constraints first, then submit only the evidence needed for the decision.

### Cost warning

**Jev is optional and its hosted API is not automatically free.** A free playground does not make automated API access free. At verification time, the linked independent hosted gateway advertised prepaid API access. Skip it for a strict zero-inference-bill setup unless you have separately verified a free allowance or functioning local backend.

- Official TypeSafe site: <https://typesafe.ai/>
- Official docs: <https://docs.typesafe.ai/>
- Community MCP implementation: <https://github.com/codaaiteam/jev-mcp>
- Independent gateway's MCP guide: <https://jevtypesafeai.com/integrations/mcp>
- Independent gateway pricing: <https://jevtypesafeai.com/pricing>

The community repository identifies the linked playground/gateway as independent and not affiliated with TypeSafe AI. Check whom you are trusting with your prompts and keys.

### Optional Hermes MCP setup

Use Hermes' MCP settings/add flow. Install Node.js/npm if you do not already have `npx` available. For the linked implementation:

```text
Name:    jev
Command: npx
Args:    -y github:codaaiteam/jev-mcp
```

Pass `TYPESAFE_API_KEY` to the server from a local secret source, using a reference rather than writing the key into shareable config. Hermes supports `${TYPESAFE_API_KEY}` references in MCP configuration. The setup's key must match the backend: hosted `jv_live_` keys belong to the independent gateway; official TypeSafe credentials use its official API. Let the documented adapter select the endpoint, or configure the correct one explicitly.

Use the Hermes MCP UI/CLI instead of blindly replacing your YAML. The shape to recognize—not a whole-file replacement—is:

```yaml
mcp_servers:
  jev:
    command: npx
    args: ["-y", "github:codaaiteam/jev-mcp"]
    env:
      TYPESAFE_API_KEY: "${TYPESAFE_API_KEY}"
    sampling:
      enabled: false
```

After trying the documented upstream command, pin a reviewed revision/version for reproducibility instead of silently following future upstream changes. Begin a new Hermes session so the tools are discovered.

Tool names differ across implementations. This repository documents `jev_check`, `jev_classify`, `jev_score`, `jev_gate`, and `jev_decide`; another installation might expose `jev_route`. Use the tools your installation actually lists.

### The confidence rule

A conservative policy can require **confidence ≥ 0.90** before taking an already authorized automatic routing action. Treat that as your operating threshold, not proof of 90% accuracy on every task. Test calibration on your own representative cases.

If the tool returns `probability`, determine what proposition it describes. For “can free solve this?”, a low probability is not the same thing as low confidence in the judgment. Do not blindly compare every numeric field against `0.90`.

### Paid last resort, safely

The logic should look like this; it is policy pseudocode, **not** an installed dispatcher:

```text
if user explicitly chose an available paid model:
    run only the authorized scope, subject to the budget
elif deterministic/local/free route passes the objective checks:
    return that result
elif explicit per-task automatic-paid permission exists
     and all allowed cheaper routes failed the relevant checks
     and a validated gate recommends escalation at confidence >= 0.90
     and the model is on the paid allowlist
     and the dispatcher/provider enforces the remaining budget:
    run the bounded paid step; validate it; record spend and reason
else:
    stop or ask for approval
```

If Jev is unavailable, returns malformed output, or lacks a meaningful confidence value, **fail closed to asking**. Never let the gate manufacture spending authorization. Installing MCP tools alone does not install a cost-enforcing router or automatic model-switch hook.

For most people, the strict manual-approval mode is simpler and sufficient.

## 10. Verify the setup

### Inspect settings

```bash
hermes --version
hermes config get model
hermes fallback list
hermes config get delegation
hermes config get cron
hermes cron list
hermes config get auxiliary
hermes config check
hermes doctor
```

Inspect locally. Review/redact any output before sharing it, especially from old configs with inline credentials. `config check` helps catch mistakes; it is not a certificate that every feature is free.

### Test one real cloud completion

```bash
hermes chat --provider openrouter \
  --model 'nvidia/nemotron-3-ultra-550b-a55b:free' \
  --oneshot -q 'Reply with exactly: FREE_ROUTE_OK'
```

This consumes quota. Check Hermes' provider/model metadata and your provider activity at <https://openrouter.ai/activity>. A model claiming its own identity in generated text is not verification.

### Test real tool calling

In an empty test directory, ask:

> Use a terminal or file tool to list this directory. Report what the tool actually returned. Do not modify any files.

**Pass:** an actual tool call and corresponding result appear. A prose description or printed JSON pretending to be a tool call does not pass.

Repeat after selecting `/model local`. Confirm in Hermes' model/provider display that it is local. For privacy-sensitive testing, ensure auxiliary calls, fallback chains, and tools are local too; local inference by itself does not make web browsing offline.

### Confirm the spending behavior

- All primary and auxiliary fallback entries are free/local.
- Cron fleet default is independent from the current chat model.
- No existing job or worker has an unexpected paid pin.
- Paid provider credentials are absent from the strict-free deployment, or controls are deliberately configured.
- No paid external tools or upstream router policies bypass your intended budget.
- A simulated outage in a disposable profile stops or takes a free/local route; it does not call paid inference.

Do outage tests in a disposable profile, not by damaging your working key. If you do not test failure handling, label it untested.

### What was verified for this guide

- Official Hermes documentation and OpenRouter free-routing/limit documentation were retrieved.
- The public OpenRouter catalog was queried; suggested entries were checked for zero listed pricing and advertised tool support.
- CLI help was checked on Hermes `v0.22.2+2232.g86fa9e6`.
- Fifteen core configuration commands were executed successfully against a disposable `HERMES_HOME`, including aliases, the JSON fallback list, delegation settings, cron defaults, and compression overrides.
- The resulting config was parsed and key types/values were asserted.
- The exact catalog-discovery example was executed, Bash snippets passed syntax checks, the YAML example parsed, and all 31 unique shared links returned HTTP 200 during the check.

**Not performed:** fresh OS installation, authenticated completion benchmarks for every suggested model, a new local-model download, a new Jev installation, or a live paid-escalation failure test. Your active configuration was not modified to produce this guide.

## 11. Troubleshooting and privacy

| Symptom | Likely explanation | What to do |
|---|---|---|
| HTTP 401 | Missing/rejected credential, sometimes wrong endpoint | Reconnect in provider settings; do not print the key |
| HTTP 402 | Credit/key limit, negative balance, or a paid route/component | Inspect error metadata and actual route; do not automatically top up |
| HTTP 403 | Budget, access policy, or a WAF/bot wall | Inspect response type; an HTML challenge is not proof the key is invalid |
| HTTP 429 | Account quota or upstream capacity | Honor `Retry-After`; use local/wait; don't create accounts to evade quotas |
| HTTP 404/model missing | Retired ID or wrong base URL | Refresh the catalog; select the exact currently listed ID |
| Free model can't use tools | Missing/weak tool support or server parser issue | Test actual structured tool calls, not chat fluency |
| Ollama/local connection refused | Server down, wrong host/port, or container-localhost confusion | Verify endpoint/service; inside containers, localhost is the container |
| Slow local first response | Weight loading or prompt prefill | Use a smaller model, reduce unneeded tool/prompt load, inspect memory fit |
| Context/memory errors | Prompt/KV cache exceeds the configured window or memory | Choose an appropriate model/context; don't force a huge window blindly |
| Default changed but current chat did not | Existing session retained its choice | Start a new chat or explicitly switch it |
| Paid activity despite free main model | Aux, pinned jobs, subagents, external tools, or upstream fallbacks | Audit every billing surface in section 6 |

### Privacy rules

- Free cloud inference sends prompts to third parties. Read OpenRouter's settings and each upstream provider's data policy before sending sensitive data.
- A cloud fallback can transmit prior conversation context, not just your last sentence.
- Local-only work requires local auxiliary routes and appropriately restricted tools too.
- Never share keys, `.env`, `auth.json`, private logs, or session databases.
- If a real key has already been pasted into chat or published, rotate/revoke it. Deleting the message is not enough.
- Keep normal command approvals enabled. “Free model” does not mean “safe to grant unlimited system access.”

## 12. Links and maintenance

### Core setup

- Hermes home/downloads: <https://hermes-agent.nousresearch.com/>
- Source: <https://github.com/NousResearch/hermes-agent>
- Installation: <https://hermes-agent.nousresearch.com/docs/getting-started/installation>
- Models and auxiliary slots: <https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models>
- Configuration: <https://hermes-agent.nousresearch.com/docs/user-guide/configuration>
- Fallbacks: <https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers>
- Local models: <https://hermes-agent.nousresearch.com/docs/user-guide/local-models>
- Profiles: <https://hermes-agent.nousresearch.com/docs/user-guide/profiles>
- Secrets: <https://hermes-agent.nousresearch.com/docs/user-guide/secrets>
- Security: <https://hermes-agent.nousresearch.com/docs/user-guide/security>
- Full documentation index: <https://hermes-agent.nousresearch.com/docs/llms.txt>

### Free cloud

- OpenRouter keys: <https://openrouter.ai/settings/keys>
- Free models: <https://openrouter.ai/models?pricing=free>
- Public catalog: <https://openrouter.ai/api/v1/models>
- Free router: <https://openrouter.ai/docs/guides/routing/routers/free-router>
- Free variants: <https://openrouter.ai/docs/guides/routing/model-variants/free>
- Limits: <https://openrouter.ai/docs/api/reference/limits>
- Activity: <https://openrouter.ai/activity>

### Optional local/automation/routing

- Ollama: <https://ollama.com/download>
- Hermes + Ollama: <https://hermes-agent.nousresearch.com/docs/guides/local-ollama-setup>
- Cron: <https://hermes-agent.nousresearch.com/docs/user-guide/features/cron>
- Delegation: <https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation>
- TypeSafe: <https://typesafe.ai/>
- TypeSafe docs: <https://docs.typesafe.ai/>
- Community Jev MCP: <https://github.com/codaaiteam/jev-mcp>

### Maintain it without turning it into a hobby

Recheck model availability and free pricing when a model stops working or before enabling a new automation. After Hermes upgrades, inspect fallback behavior and auxiliary settings. Review provider activity after significant changes. Avoid installing a proxy, swarm, or extra router until you can name the problem it solves.

**The minimum useful setup is Hermes + one OpenRouter key + a verified free model + free-only fallbacks + explicit paid permission. Local inference and Jev are optional additions, not prerequisites.**
