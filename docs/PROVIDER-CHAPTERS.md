## 3. Nous Portal: free models through the official Hermes provider

### What you can get free

Nous Portal has a real **Free plan**. The official plan page lists **$0, free models only, and $0 monthly credits**: <https://portal.nousresearch.com/manage-subscription>.

That means access to eligible zero-priced routes—not a free balance for Claude/GPT or every other paid model. The Nous-hosted search/image/browser/speech Tool Gateway is a separate entitlement. Do not enable or rely on paid hosted tools merely because the chat model is free.

Public API documentation: <https://portal.nousresearch.com/api-docs>.

OpenAI-compatible inference base URL:

```text
https://inference-api.nousresearch.com/v1
```

### Create an account and connect Hermes

1. Open <https://portal.nousresearch.com/> and create/sign into your own account.
2. Inspect the plan page and choose **Free** if you want no subscription charge. Do not select Plus/Super/Ultra just to follow this guide.
3. In Hermes, run `hermes model`, choose **Nous Portal**, and finish the browser/device login.
4. Select an exact currently free, tool-capable model—not just any model with “Hermes” in its name.
5. Decline paid Tool Gateway opt-ins unless you deliberately want that separate service and understand its billing.
6. Start a new chat and verify the actual provider/model metadata.

The convenient `hermes setup --portal` onboarding also configures/offers hosted tools; it is not a command that magically makes every Portal model and tool free. Review every selection. Official integration guide: <https://hermes-agent.nousresearch.com/docs/integrations/nous-portal>.

For a route verified in the public catalog on 31 October 2026:

```bash
hermes config set model.provider nous
hermes config set model.default 'stepfun/step-3.7-flash:free'
hermes config set model.base_url 'https://inference-api.nousresearch.com/v1'
```

Authenticate using the provider picker first. Do not paste tokens into those commands or change only the model while leaving a different provider's endpoint/credential overrides attached.

**Re-check a route you configured earlier.** The public catalog is the free-route list, not a mirror of everything your account can call: a model can stop being listed while remaining callable for the account that already uses it, and a listed model can still be unavailable to you.

### Free entries observed in the public catalog

The following exact IDs had explicit zero pricing and advertised tools at the check:

- `ornith/ornith-1.5-122b:free`
- `reflection/beam-1.0-501b-a23b:free`
- `stepfun/step-3.7-flash:free`
- `upstage/solar-mini4:free`

This is a catalog observation, not a benchmark or a guarantee your account can immediately call every entry. Model retirement and capacity restrictions still apply. Step 3.7 Flash advertised image and video input and Ornith 1.5 122B advertised image input; the other two listed routes were text-only. Test actual vision/tool behavior before depending on it.

**The free list churns.** Earlier editions of this guide listed `meituan/longcat-2.0:free` and `meituan/longcat-2.5-preview:free`, and then the two `poolside` Laguna free routes. On **31 October 2026** a re-read of the public catalog listed the four IDs above, and the two `poolside` Laguna routes were **no longer listed at all** — a route configured in an earlier session can vanish from the catalog while remaining callable for the account that already uses it. Treat the catalog as the live source and re-check it rather than copying any list, including this one.

Public catalog: <https://inference-api.nousresearch.com/v1/models>.

A historical configured fallback can outlive a model. In this inventory, `stepfun/step-5-preview:free` was configured but absent from the current free catalog. Do not copy stale routes blindly.

### Reuse the API in your own applications

If your Portal dashboard permits API-key creation on your chosen free plan, generate a key there and use the inference base URL above with an exact free model. An OAuth login inside Hermes is not itself an API key you should copy into unrelated tools. Keep both credentials private.

**Fresh-account free-plan API-key issuance was not tested here.** The general API docs discuss credits/subscriptions, while the plan page explicitly offers free models. If the dashboard requests a payment before issuing a key, stop rather than spending just to follow this guide; check the current account entitlements/support or use the supported OAuth route inside Hermes and another verified free API for external apps.

The API docs currently list Free limits of **50 requests/minute and 500,000 tokens/minute**. Those are rate ceilings, not a grant of unlimited monthly tokens. Check account-specific limits and eligibility. Unauthenticated generation can return payment requirements; that does not turn x402/USDC into a free route. This guide does not enable payment protocols.

### Pin other work deliberately

If Nous is your chosen free provider, select free Nous routes for delegation, cron, and auxiliary slots too. For example, the cron fleet defaults are:

```bash
hermes config set cron.model_provider nous
hermes config set cron.model 'stepfun/step-3.7-flash:free'
```

Existing pinned jobs are still separate. For vision, choose a currently advertised image-capable free route rather than assigning a text-only model. Keep fallback chains explicitly free/local; authenticate a separate OpenRouter backup before adding it.

## 5. FreeLLMAPI: combine your legitimate free allowances behind one local API

### What this is—and what it is not

FreeLLMAPI is a **self-hosted router**, not a company handing you unlimited model credits. You bring provider keys/allowances, enable suitable routes, and it presents an OpenAI-compatible endpoint with routing and fallback.

Use the project actually installed in this setup:

- Source: <https://github.com/tashfeenahmed/freellmapi>
- Install guide: <https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/install/01-install.md>
- Releases: <https://github.com/tashfeenahmed/freellmapi/releases/latest>
- API guide: <https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/api/01-rest-api.md>

There are similarly named forks, including an unrelated PHP implementation. Do not mix their installation or API instructions.

The router is free/open source. The project's **optional paid Premium live catalog** is distinct: its README describes a delayed monthly catalog snapshot for free installs and a current feed for paying users. You do not need to buy Premium to run the router. Aggregate “billions of tokens” headlines are theoretical sums across providers—not an entitlement for every new user, a tested capacity on this machine, or a production SLA.

### Choose one installation path

**Desktop:** use the official release for your supported platform. Open its dashboard from the tray. Inspect the listening address/port; desktop releases can use a different port from the server default.

**Docker/server:** install Docker/Compose through the official instructions for your OS first, then follow the project's own install guide: <https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/install/01-install.md>. On Linux/macOS/WSL that guide downloads an installer script. Download it, read what it does, and run it yourself rather than piping a remote script straight into a shell. It executes remote code and requires Docker. It is optional; manual Docker/source installation is documented upstream too. Keep the default loopback-only binding. Do not overwrite an existing FreeLLMAPI `.env`, encryption key, or database while “reinstalling.”

**Source:** check the repository's current Node/npm requirements, install/build as documented, and run the built server. This inventory's package declares Node `>=20.18.0 <25.0.0` and npm `>=10.0.0`. A system service is preferable to leaving an important gateway attached to a temporary terminal session. The author's installation uses a user service; other operating systems should use their supported supervisor or the desktop app.

The usual server dashboard is <http://127.0.0.1:3001/> and the usual model API base is:

```text
http://127.0.0.1:3001/v1
```

These are local addresses on the machine running the gateway. On a phone, another PC, or inside a container, `localhost` means that device/container—not your desktop. Use a secured deployment/tunnel when remote access is genuinely needed; do not casually expose the unified key or publish a public proxy.

### First-run setup and the three different secrets

1. Open your local dashboard. Server installs have their supported first-run administrator setup; the desktop app has a different local sign-in flow.
2. Complete any setup-code/password prompts locally. Do not paste passwords or setup codes into an AI chat.
3. Open **Keys** and add your upstream providers one at a time. Use your own legitimate accounts and the correct provider IDs.
4. Copy the gateway's **unified API key** from its trusted local UI into the application that will call the gateway.
5. Configure/test one model before enabling a wide automatic chain.

Do not confuse:

| Secret | Purpose | Goes where |
|---|---|---|
| Upstream provider key | Authenticates Groq/Gemini/OpenRouter/etc. | FreeLLMAPI's local Keys UI/store |
| Unified API key | Authenticates your applications to FreeLLMAPI | Hermes custom-provider/key settings or your app's secret source |
| Encryption key | Protects the local encrypted credential store | Gateway deployment secret/config, backed up privately |

The administrator password/session is another credential, not the model API key. Never retrieve the unified key by dumping the database into chat. Use the supported dashboard/credential flow. A new installation can generate a different unified key; an old one then fails authentication even when the URL is correct.

### Add useful free upstreams

Start with one or two that you can genuinely access, for example a Groq free account, eligible Gemini free-tier API, Mistral Free mode, or exact OpenRouter `:free` models. See the provider-by-provider signup instructions below. Verify regional eligibility, limits, data terms, and whether the account is actually on a free plan.

- Add the key in the matching **Keys** entry.
- Enable only appropriate models in **Models**.
- Test a short completion and structured tool call in the gateway playground.
- Inspect **Analytics** and the served-provider/route metadata.
- Keep experimental/trial and paid/credit-spending lanes separated.

Adding a key does not make every model at that provider free. An expired trial is not a transient error to retry forever. Do not create extra accounts or rotate keys to evade provider terms or quota limits.

### Build a genuinely free-only chain

The gateway's own routing policy matters as much as Hermes' fallback list. Review enabled models, named chains, custom providers, routing strategies, and model-specific capabilities. Disable paid routes and unintended external extras. Do not include subscription/PAYG NanoGPT or Cheaper Inference just because they are installed elsewhere in Hermes.

The model ID `auto` is FreeLLMAPI's router and is only as safe as its enabled upstream chain. It is **not** the same service as `openrouter/auto`, and is not an independent proof of zero cost. Optional decision-model routing can itself invoke another service; keep it off until its pricing and limits are verified.

The free snapshot catalog can be stale. Reconcile it with current first-party terms—especially services whose free offerings changed, such as Hugging Face hosted inference. Do not buy a catalog subscription automatically to “fix” model availability.

### Connect Hermes to FreeLLMAPI

In `hermes model`, choose a **Custom Endpoint** or add a named custom provider through provider settings:

```text
Provider name: freellmapi
Base URL:      http://127.0.0.1:3001/v1
API key:       your local gateway's unified key, entered only in the trusted key UI
Model:         a tested fixed model, or auto after auditing the gateway's chain
```

Discover models if the supported UI offers it. Do not paste a key into `config.yaml` or into a command-line argument visible to other processes. A manually named provider must exist before aliases like `freellmapi/auto` can work.

A settings-only provider shape to recognize is:

```yaml
providers:
  freellmapi:
    name: FreeLLMAPI
    base_url: http://127.0.0.1:3001/v1
    model: auto
    key_env: HERMES_FREELLMAPI_API_KEY
    discover_models: true
```

`HERMES_FREELLMAPI_API_KEY` is an example credential-variable name, not a secret. Your actual configured name may differ. Add the credential through the supported local setup/secret-source flow so that it matches the provider's `key_env`. The snippet is not a whole-file replacement or permission to bypass config protections.

### Add Nous as a gateway upstream only when explicitly supported

The installed FreeLLMAPI source did **not** register a native `nous` adapter. Keep Nous directly in Hermes, or use a supported **Custom OpenAI-compatible upstream** with the Nous inference URL, your own eligible Portal API key, and exact verified free model IDs. Do not give a generic OpenRouter adapter a Nous key or invent a `nous` platform ID.

### Verify the gateway without leaking a key

Use its trusted playground/client or a credential-aware local application. The expected checks are:

- Gateway is running on the intended interface/port.
- Authentication succeeds using the unified key—not an admin-session token.
- The selected upstream actually completes a request.
- The structured tool call works, and Analytics identifies a compliant served route.
- Under a controlled outage, only approved free/local backups are selected.

An unauthenticated `/v1/models` request returning **401** proves the protected server is responding, not that the unified key is invalid. That is the non-secret reachability check performed here. No unified key, credential database, or authenticated upstream routing was inspected for this guide.

The project describes itself as personal experimentation/learning software. Respect that and each provider's terms. For an important production service, free-tier availability and this router do not supply a production guarantee.

## 6. Other provider families actually configured here

These are part of the stack inventory, but not all are free API providers.

### Pollinations: real API use funded by Quest Pollen

- Home: <https://pollinations.ai/>
- Keys: <https://enter.pollinations.ai/keys>
- Quests: <https://enter.pollinations.ai/quests>
- API documentation: <https://gen.pollinations.ai/docs>
- OpenAI-compatible base: `https://gen.pollinations.ai/v1`

1. Create/sign into your account and inspect the wallet/available Quests.
2. Complete legitimate offered Quests or other supported free-credit activities. Rewards and eligibility can change; no fixed free balance is promised here.
3. Create a secret API key with restricted models, expiry, and a spending budget.
4. Add a Hermes custom provider with the base URL above and a currently eligible model from its live catalog. The configured example on this machine was `openai/gpt-5.4-nano`; that is a priced route funded by Pollen, not automatically a zero-price model.
5. Verify the wallet debit and remaining free/earned balance before batch use. Stop when the approved allowance ends; do not enable automatic top-ups.

The current docs use canonical `publisher/model` names. Some old short aliases still work, but use the live catalog rather than assuming legacy `openai` aliases are permanent. Keep secret keys out of browser frontend code. For apps used by other people, use the documented **Connect User Wallets/BYOP** authorization so each user knowingly authorizes their own scoped spending. A publishable app key identifies the app; it is not an unlimited free secret key.

### NanoGPT: distinguish the web free model from paid API allowances

- Pricing: <https://nano-gpt.com/pricing>
- API information: <https://nano-gpt.com/api>
- Base URL used here: `https://nano-gpt.com/api/v1`

The public pricing page currently says **one free model on the web only**. API access is PAYG or included with the paid Pro subscription. Pro is advertised at **$12/month** with **60 million included input tokens per week**, subject to its current included-model and usage rules.

Therefore the configured NanoGPT routes in this stack are **not evidence of a generally free API**. If you already pay for a plan, an included route may cost no additional amount until the allowance is exhausted, but the subscription itself is paid. Confirm the exact model's inclusion and disable spending past the cap where the provider offers that setting.

Several local provider names/aliases can point to this same company. Do not count them as separate free providers or encourage multi-account quota evasion. Keep this family out of strict zero-cost automatic fallbacks unless a specific account/model has a verified zero-cost entitlement and enforceable stop condition.

### Cheaper Inference: discounted paid access, not free API

- Home/pricing: <https://cheaperinference.com/>
- Base URL: `https://api.cheaperinference.com/v1`

The provider is configured here, but its public page advertises usage-based paid inference with funding from **$5**. No recurring free API entitlement was established. Treat it as an optional paid-last-resort provider only after explicit authorization. A promotion, if separately offered to a particular account, is a finite allowance—not a permanent free tier.

### Local Ollama and Hermes-managed llama.cpp

These are genuinely useful no-hosted-inference-bill options. The local Ollama server here responded and listed a customized Qwen coder model plus an embedding model; that observation is not an instruction to download the same custom tag on another machine.

Use the local-model chapter for hardware-fit checks and setup. No online provider key is needed for ordinary loopback-only Ollama/managed local inference. Your GPU vendor does not restrict which hosted APIs you can use: using NVIDIA's hosted API does not require buying an NVIDIA GPU.

### Other logged-in subscriptions and tool services

ChatGPT/Codex, xAI/SuperGrok, Copilot, Portal paid plans, and similar subscriptions may provide included usage. They are not universally free API access just because an OAuth login works. A model-provider credential, a browser credential vault, and a tool connector are different integrations. Verify the actual entitlement before enabling them, and keep them out of strict-free unattended chains.

## 7. More free allowances you can add directly or through FreeLLMAPI

These are useful upstream options—not a claim that every one is connected and working on the author's machine. Create your own account and review first-party terms before adding a key. Availability, country restrictions, models, quotas, and allowed production use differ.

| Provider | How to get access | What to call it honestly | Hermes / gateway connection |
|---|---|---|---|
| Groq | Create a console account and API key | Rate-limited free-plan API on eligible models; account/organization limits apply | Custom OpenAI-compatible endpoint `https://api.groq.com/openai/v1`, or FreeLLMAPI `groq` |
| Google Gemini | Create an API key in Google AI Studio; choose a model with an applicable Free Tier | Eligible free-tier API; free-tier data terms may differ from paid | Hermes Gemini provider, or FreeLLMAPI `google` |
| Mistral | Create Studio account/key in Free mode, no credit card required per current quickstart | Included free-mode usage within account limits; PAYG is separate | Custom endpoint `https://api.mistral.ai/v1`, or FreeLLMAPI `mistral` |
| Cerebras | Create a cloud console account/key and inspect Limits | Currently documented Free Trial tier; do not promise permanent unlimited access | Custom endpoint `https://api.cerebras.ai/v1`, or FreeLLMAPI `cerebras` |
| NVIDIA API Catalog | Sign into build.nvidia.com and generate a model API key | Hosted prototyping/trial credits; not a perpetual zero-price guarantee | Hermes NVIDIA provider, or FreeLLMAPI `nvidia`; use the endpoint from the model page |
| Cloudflare Workers AI | Create account, obtain account ID and suitably scoped Workers AI API token | Daily free allocation on supported models/plans; paid overage exists on paid plans | Supported Cloudflare adapter/custom endpoint; ensure the installed gateway version supports it |
| Cohere | Create an evaluation key in its dashboard | Free evaluation/trial usage with limits; production keys are paid | Supported native/compatible adapter; do not assume every FreeLLMAPI build includes it |
| Hugging Face Inference Providers | Create account/token, then inspect billing | Current free accounts have **no included monthly credits**; subscription credits and purchases are paid | Useful model-download source and paid/included inference route, not a default free API lane |

### Groq: account → key → one tested model

Open <https://console.groq.com/keys> and create your own key. Inspect <https://console.groq.com/settings/limits> and the current model catalog. Put the key in the Groq entry in FreeLLMAPI, or in Hermes' custom-provider key setup with the base URL in the table. Test one currently available tool-capable model; do not assume all models share the same request/token caps.

Official limits: <https://console.groq.com/docs/rate-limits>. Limits are at organization level, not per key. Upgrading to a paid Developer plan is not part of this free setup.

### Gemini: choose the free API tier, not just a free website

Get a key at <https://aistudio.google.com/apikey>. Review <https://ai.google.dev/gemini-api/docs/pricing> for the exact model/capability you intend to use and its Free Tier column. Some models/features have no free tier. Read the data-use terms: free API input/output may be used differently from paid service data. Do not send secrets or private business data merely because a key was free to create.

Add the key through Hermes' Gemini setup or the gateway's Google entry. Leave paid billing/upgrades off unless authorized. Check your project limits; a free AI Studio interface is not proof every API endpoint is free.

### Mistral: current Free mode setup

Follow <https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key>. Create the account at <https://console.mistral.ai/>, open **API Keys**, name a key, set expiry/scope, and store it privately. The official guide says Free mode requires no credit card. Inspect your organization's included usage and limits rather than repeating old “one billion tokens” claims.

Limits/billing controls: <https://docs.mistral.ai/admin/billing-usage/usage-limits>. Keep pay-as-you-go disabled if you want usage to stop at the free allowance. Add the key to the gateway's Mistral entry or the compatible endpoint in Hermes, then test only a model available to your account.

### Cerebras: inspect the actual Free Trial tier

Start at <https://cloud.cerebras.ai/>. Create the API key, select an allowed model, and read the console's **Limits** page. The current official table labels the free lane **Free Trial** and publishes request/token ceilings. Do not present it as an unlimited ongoing production service. Add to the matching gateway/custom endpoint and bound output tokens to avoid quota overestimation.

Official limits: <https://inference-docs.cerebras.ai/support/rate-limits>.

### NVIDIA: hosted trials are independent of your local GPU

Start at <https://build.nvidia.com/explore/discover>, choose a model, and follow **Get API Key**. Review any eligibility and trial-credit balance/expiry. Use the model page's current base URL, model ID, and capability requirements.

Quickstart: <https://docs.api.nvidia.com/nim/docs/api-quickstart>. FAQ: <https://docs.api.nvidia.com/nim/docs/faq>. The FAQ distinguishes browser previews from remote API calls that consume trial credits. Self-hosted NIM/enterprise licenses are a different product and are not required to call the hosted API.

### Cloudflare: keep the account on a fail-closed free allocation

Create/sign into <https://dash.cloudflare.com/>. Find **Workers AI**, obtain your account ID, and create an appropriately scoped API token. Use its official compatibility/REST instructions or a supported gateway adapter. Do not invent a normal `/v1` URL without the required account path.

Pricing: <https://developers.cloudflare.com/workers-ai/platform/pricing/>. The current documented free allocation is **10,000 Neurons/day**. Neurons are compute units, not tokens. The Free plan stops at its limit; paid-plan usage above the allocation can bill. Verify model eligibility and plan details before enabling a route.

### Cohere and Hugging Face: special limits, not a free-for-all

Cohere evaluation keys are available at <https://dashboard.cohere.com/api-keys>; current docs describe evaluation keys as free/limited and production keys as paid. Trial keys are limited to **1,000 API calls/month** in the published rate-limit guide: <https://docs.cohere.com/docs/rate-limits>. Respect evaluation-use restrictions and check each model.

Hugging Face remains useful for downloading open weights, but its current hosted Inference Providers pricing page lists **no monthly credits for free accounts**: <https://huggingface.co/docs/inference-providers/pricing>. Do not enable its hosted route in a strict-free chain based on an outdated aggregator catalog. Local use of downloaded models is separate from hosted inference billing.

## 8. Use the same APIs in your own scripts and other applications

### The four settings every compatible client needs

```text
API protocol: OpenAI-compatible chat completions (when the provider supports it)
Base URL:     the actual provider or local gateway /v1 endpoint
Model:        an exact, eligible model ID for that endpoint
Credential:   that endpoint's own API key from a trusted local secret source
```

A model ID that works on OpenRouter is not automatically valid on Nous or FreeLLMAPI. An OAuth token from one service is not a general API key for another. A local gateway's unified key is not an upstream provider key.

| Route | Base URL | Example selection |
|---|---|---|
| Nous Portal | `https://inference-api.nousresearch.com/v1` | `stepfun/step-3.7-flash:free`, with eligible Portal API access |
| OpenRouter | `https://openrouter.ai/api/v1` | An exact checked `:free` ID or `openrouter/free` |
| FreeLLMAPI | `http://127.0.0.1:3001/v1` for the usual server install | A tested fixed model, or `auto` after auditing enabled routes |
| Pollinations | `https://gen.pollinations.ai/v1` | A current eligible model funded by an approved Pollen allowance |
| Ollama | `http://127.0.0.1:11434/v1` when using its default port | An exact installed model ID |

### Credential-safe client example

This Python example uses the OpenAI SDK if your application already uses it. `LLM_BASE_URL`, `LLM_MODEL`, and `LLM_API_KEY` must already be supplied by your trusted local environment/secret integration. Do not put a real key into source code, a command line, or chat. Use an isolated application environment, not Hermes' managed Python installation, if adding SDK dependencies.

```python
import os
from openai import OpenAI

base_url = os.environ.get("LLM_BASE_URL")
api_key = os.environ.get("LLM_API_KEY")
model = os.environ.get("LLM_MODEL")
if not (base_url and api_key and model):
    raise SystemExit("Set LLM_BASE_URL, LLM_API_KEY and LLM_MODEL first.")

client = OpenAI(base_url=base_url, api_key=api_key)
response = client.chat.completions.create(
    model=model,
    messages=[{'role': 'user', 'content': 'Reply with exactly: API_ROUTE_OK'}],
    max_tokens=64,
)
print(response.choices[0].message.content)
```

This makes a real generation request and consumes quota/credits on the chosen endpoint. It is an example for users to run after checking eligibility; it was **not** executed with their credentials for this guide. Start with a harmless tiny prompt, inspect provider activity/cost, then test a real tool call before building a larger agent workflow.

For CLI/desktop apps, use their supported provider settings or documented integration. A compatible API does not imply every client supports every transport, vision format, tool schema, reasoning parameter, or authentication flow. FreeLLMAPI's client documentation is at <https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/clients/01-agent-clients.md>.

Do not publish a shared server-side key in a frontend or Telegram channel. For applications with multiple users, provide individual authorization/budgets and comply with the upstream terms. A personal proxy and someone else's free account are not a public redistribution license.

## 18. OpenCode: three different things under one name

Read this before adding OpenCode. "OpenCode" is a coding-agent client, a pay-as-you-go model service (Zen), a paid seat (Go), and a set of free console rows. They have different access rules and different privacy terms. Only some of them can serve a Hermes session.

- Client and Zen home: <https://opencode.ai/> and <https://opencode.ai/zen>
- Go (seat) pricing and models: <https://opencode.ai/v2/docs/console/go/> and <https://opencode.ai/v2/docs/console/models>
- Console provider list: <https://opencode.ai/v2/docs/providers>
- Skill for the client: <https://github.com/NostrDanish/opencode-skill>
- **Referral program: none found.** `/referral` returned 404 and no affiliate page was found on the pages read 31 October 2026, so this chapter uses plain links.

### Zen: pay per request, with a few free rows

Zen bills per request at list price with no markup, and the account is topped up in advance. It is a **paid** route that happens to carry some rows labelled Free. Those Free rows are the ones worth looking at; the rest of the catalog is ordinary paid inference.

The pricing page read 29 October 2026 mentions a payment-processing fee of $1.23 per $20 top-up. That is a real cost, so read the current terms before topping up.

Hermes reads it as two built-in providers: `opencode-zen` (`OPENCODE_ZEN_API_KEY`, base `https://opencode.ai/zen/v1`) and `opencode-go` (`OPENCODE_GO_API_KEY`, base `https://opencode.ai/zen/go/v1`). Add the key yourself in the trusted key UI; never paste it into chat or into `config.yaml`.

### The Free console rows do not transfer to Hermes

OpenCode's own documentation states that the free-tier chat models on the Console require the OpenCode client. Hermes is a different client. **Do not wire a Console free row into Hermes and call it a free API route.** From another client, the Console offers paid models or the Go seat.

There is no keyless free OpenCode route in Hermes: the relay stopped serving anonymous free-tier requests, so that provider was removed upstream. Select `opencode-zen` or `opencode-go` instead, and pay for it knowingly.

### Go: a paid seat that does work with Hermes

Go is a monthly subscription, and it does work with Hermes if your agent is current — Hermes is a validated client from v0.21.6, which sends the session header older builds do not send.

- Go is $10 a month, Go Plus $40 a month, Go Teams $20 per member a month (Go page read 31 October 2026).

Go's model list includes a few rows marked Free for a limited time. "Free" is not one privacy policy there: Beam Free is not used for training and data is kept 30 days, while Iceman Contributor Free is free in exchange for permission to train on prompts and completions. Read the row you actually select.

Go's accounting works like this: a 5-hour window counts as 20% of the monthly allowance, a week as 50%, the month as 100%, and each model has its own dollar cap. On the $10 Go plan GLM-5.3-Flash is counted to $60 a month at $0.15/$0.50 per million tokens, and Grok 4.7 under 200k tokens is counted to $15 a month at $2/$6. Those are Go's internal accounting prices, not a bill on top of the subscription, until you pass the cap.

### Two caveats to keep

**OpenCode Go's privacy class is unknown.** No data-retention or training page was read for the Go tier. Do not claim it does not train.

**The DeepSeek zero-data-retention agreement that was valid through 31 October 2026 has expired.** Treat Go's privacy as unknown until a fresh provider check says otherwise, and do not send private material on it.

**If you only wanted a free coding agent, stay on the Nous or OpenRouter free routes.** Open Go when you have already decided to pay $10 a month.

## 19. OmniRoute: the free self-hosted gateway versus the paid hosted API

OmniRoute is two different products sharing one name. The first is a **self-hosted, MIT-licensed AI gateway** that routes to providers you connect yourself. The second is the **hosted Cheaper Inference API**, which is ordinary paid usage-based inference. They are not interchangeable.

- Gateway project: <https://github.com/cheaper-inference/OmniRoute>
- Product site: <https://omniroute.online/>
- Hosted paid API base: `https://api.cheaperinference.com/v1`
- **Referral program: the hosted side uses `?ref=`** (see chapter 25). The self-hosted gateway is open source and has no referral.

### The self-hosted gateway is the free part

It runs on your own machine, needs Node ≥ 22.22.2, and serves an OpenAI-compatible endpoint on `http://127.0.0.1:20128/v1` with a dashboard at `http://127.0.0.1:20128/dashboard`.

```bash
npm install -g omniroute
omniroute
```

**It grants you no tokens.** Routing works only after you connect upstream accounts in its dashboard — your own provider keys, your own OAuth logins, or genuinely keyless upstreams. Install the gateway before you believe it is "free"; then connect at least one eligible upstream and check what that upstream charges.

Ask before installing a second local router on a machine that already runs one (FreeLLMAPI, for example), and do not overwrite its data directory. Docker and desktop builds are documented upstream.

Hermes side: provider `omniroute`, `OMNIROUTE_API_KEY`, optional `OMNIROUTE_BASE_URL`. Take the key from Dashboard → Endpoints and add it yourself with `hermes auth add omniroute`; never paste it into chat.

### Routing IDs, and one known failure

| Model ID | What it does |
|---|---|
| `auto` | Builds a combination from the providers you connected |
| `auto/coding` | Quality-first for code |
| `auto/cheap` | Cheapest token first |
| `auto/fast` | Lowest latency |
| `auto/subscription` | Plan quota only; fails closed |

Hermes has a known empty-stream failure with some OmniRoute `auto/*` aliases over the OpenAI-compatible endpoint (upstream issue #7111, reported against OmniRoute 3.8.46 and since closed upstream). **Prefer a concrete catalog id** from `GET /v1/models` when `auto` returns nothing; a direct `curl` to `/v1/chat/completions` can still succeed.

`auto` is only as free as the upstreams you enabled. Connecting a paid key inside OmniRoute spends money even when Hermes' own default stays on a free route.

### The hosted side is paid

The hosted Cheaper Inference API is usage-based and needs funding from $5. It is a separate product from the gateway, and it is described honestly in chapter 25.

## 20. Routstr: pay per request in sats, no account

Routstr is a decentralised inference network paid per request in Bitcoin over Lightning or Cashu. Its own documentation puts "No Account / Private" opposite a normal API's "KYC / Account", and describes use without accounts or identity checks. **Treat that as the provider's stated design, not as a guarantee that every upstream it routes to is KYC-free** — the upstream lab still receives your prompt.

- Docs: <https://docs.routstr.com/client/introduction/> and <https://docs.routstr.com/client/payments/>
- Public node that answered `/v1/models` on 31 October 2026: `https://routstr.ft.hn/v1` (23 models listed)
- Easy door: <https://chat.routstr.com/>
- Provider skill and plugin: <https://github.com/NostrDanish/hermes-routstr-provider>
- **Referral program: none found.** `/referral` returned 404 and no affiliate page was found. Plain links only.

### How the money works

You fund a session with a Lightning invoice or a Cashu token, you get an `sk-` key, and you refund the change when you stop. **The key is the balance.** Leave a large balance on a node and you have left sats in someone else's hot wallet. Say your spend cap out loud before you paste a key: on Routstr the cap is the sats you deposited.

The URL in Routstr's own docs, `https://api.routstr.com/v1`, returned 404 on `/v1/models` when checked on 31 October 2026. **Use a node whose `/v1/models` you have just opened yourself.** Keys are node-local: a key minted on one node will not authenticate against another.

### Connect it

```yaml
providers:
  routstr:
    name: routstr
    base_url: https://routstr.ft.hn/v1
    model: glm-5.3-flash
    discover_models: true
    api_mode: chat_completions
    key_env: HERMES_CUSTOM_ROUTSTR_API_KEY
```

Add the key yourself: set `HERMES_CUSTOM_ROUTSTR_API_KEY` in the Hermes `.env` file (mode 600), or export it in the shell before starting Hermes. `hermes auth` is not required for this plugin, and `hermes auth status routstr` may still report logged out. Do not switch `model.default` off your free-first route. **Do not send a test completion to "see if it works"** — that spends sats. Inadequate balance comes back as HTTP 402, which is a billing answer, not a Hermes bug.

`routstrd clients add --hermes` is a different path that writes a legacy inline key into `config.yaml`. Prefer the plugin plus the environment variable.

## 21. More free upstreams you can add today

This chapter covers the additional providers that are worth a key, with what each one's free offer actually is. All are reachable from Hermes through a custom OpenAI-compatible provider row, and several already ship as built-in provider slugs. Create your own account and read the first-party terms before adding a key.

**A plugin or a built-in slug does not give you an account.** It makes the provider selectable. The account, the key, and the entitlement are yours.

| Provider | Signup | Friction | Free offer | Base URL | Slug |
|---|---|---|---|---|---|
| Nous Portal | <https://portal.nousresearch.com/> | account; no card for the Free plan | permanent free plan, $0, free models only | `https://inference-api.nousresearch.com/v1` | `nous` (built in) |
| OpenRouter | <https://openrouter.ai/settings/keys> | account; no card | permanent zero-priced `:free` models | `https://openrouter.ai/api/v1` | `openrouter` (built in) |
| Groq | <https://console.groq.com/keys> | account; no card | Developer-plan allowance with per-organization limits | `https://api.groq.com/openai/v1` | custom row |
| Mistral | <https://console.mistral.ai/> | account; no card for Free mode | included monthly usage, then pay-as-you-go | `https://api.mistral.ai/v1` | custom row |
| NVIDIA NIM | <https://build.nvidia.com/explore/discover> | account | "Free serverless APIs for development" | per-model page URL | `nvidia` (built in) |
| Cloudflare Workers AI | <https://dash.cloudflare.com/> | account | 10,000 Neurons/day free, resets 00:00 UTC | account-scoped URL | custom row |
| LLM7.io | <https://dash.llm7.io/> | email token, no card for the free tier | permanent free tier, 100,000 tokens/day | `https://api.llm7.io/v1` | custom row |
| Ollama Cloud | <https://ollama.com/signup> | email or Google/GitHub | hosted open models; home page claims zero data retention | per-account endpoint | `ollama-cloud` (built in) |
| Kilo Code | <https://app.kilo.ai/> | account; explicitly no credit card | free routing tier | per-plan endpoint | `kilocode` (built in) |
| Google Gemini | <https://aistudio.google.com/apikey> | Google account | free tier on selected models only | `https://generativelanguage.googleapis.com/v1beta` | `gemini` (built in) |
| Hugging Face | <https://huggingface.co/join> | account | **no monthly credits for free accounts** | `https://router.huggingface.co/v1` | `huggingface` (built in) |
| Pollinations | <https://enter.pollinations.ai/keys> | account | Quest Pollen you earn — a finite balance, not a free pool | `https://gen.pollinations.ai/v1` | `pollinations` (plugin) |

Rows marked **custom row** need a `providers.<slug>` entry in `config.yaml` before the picker shows them. A model-provider plugin file alone does not create the row. Set the row with `hermes config set`, never by hand-editing YAML, and never change `model.default` while registering.

**Read the Free offer column as a category, not a promise.** A **permanent free plan** or **zero-priced route** is billed at $0 for the listed models. An **allowance** is a metered developer-plan quantity that resets and can be exhausted. **Included monthly usage** is a Studio benefit that ends in pay-as-you-go. A **trial** is time-limited and needs a verified payment method. **Earned credits** are a finite balance you have to earn first. **Local/offline** means it runs on your own machine. These are not interchangeable, and a provider can change its category without notice.

**"No card" describes the signup form on the date it was read, not a permanent promise.** These descriptions reflect the first-party pages read on 31 October 2026. Region, sanctions, payment-method, and account-review policies still apply and vary by country, so treat "email signup" or "no card" as what the form asked for on that date — never as a guaranteed no-KYC route.

### Groq

Create a key at <https://console.groq.com/keys>. Rate limits are **per organization, not per key**, so a second key does not give you a second allowance. The limits page tells you to open your own account limits page for the exact numbers, and the summary table on that page is attached to the Developer-plan base limits — read your own account rather than trusting a copied number. Cached tokens do not count toward the limits.

Base URL `https://api.groq.com/openai/v1`. Free-tier terms were not restated on the documentation pages read on 31 October 2026, so verify the allowance in your console before relying on it.

### Mistral

The Studio quickstart says you can activate Free mode and make a key without a credit card. Free mode is included monthly usage shown on your own limits page; pay-as-you-go then draws prepaid credits past that. **Leave pay-as-you-go off if you want the call to stop at the allowance.** Do not repeat old "one billion tokens" claims.

### NVIDIA NIM

The build page offers "Free serverless APIs for development". You do not need an NVIDIA GPU to call it, and owning one does not make the hosted API free. Use the base URL and model ID from the model page you picked, and note that trial use is logged — do not send personal or confidential data.

### Cloudflare Workers AI

The pricing page, updated 20 October 2026, gives **10,000 Neurons per day at no charge**, resetting at 00:00 UTC. A Neuron is a compute unit, not a token, so do not compare it with a token quota. On Workers Paid, usage above the allocation bills $0.011 per 1,000 Neurons. The endpoint is **not** a plain `/v1` path — use the account-scoped URL from their docs, and do not put this route on a paid Cloudflare account and then forget.

### LLM7.io

A permanent free tier confirmed on the vendor's own page read 31 October 2026: **100,000 tokens/day, 250 requests/hour, 60 requests/minute, 1 request/second**, with a `default` model id and a key from <https://dash.llm7.io/>. Card or crypto appear only as top-up methods, not as a condition of the free tier. `GET https://api.llm7.io/v1/models` responds without a key. Treat it as a small independent service: pin it to one job, not to the whole agent.

### Ollama Cloud and Kilo Code

Ollama Cloud signs up with an email or Google/GitHub, shows a bot check, and shows no phone or card field. Its home page claims "your prompts are never stored or trained on", and hosted open models are served from their infrastructure rather than your machine — local Ollama stays the private option. Kilo Code explicitly advertises a free tier with no credit card; note that it is an AI coding platform as much as an inference API, and read what its free tier actually routes to.

### Gemini, Hugging Face, Pollinations

**Gemini**'s free tier covers selected models only; per the pricing page read 30 October 2026, Gemini 3.8 Flash is free of charge on the free tier and Gemini 4 Argon is not. Free-tier content may be used to improve Google's products, and Google Search grounding is not on the free tier. A free AI Studio interface is not proof that every API endpoint is free.

**Hugging Face** Inference Providers lists **no monthly credits for free accounts**; you purchase credits or upgrade to PRO at $2/month. Keep it as a source of downloadable open weights, not as a free inference lane in a strict-free chain.

**Pollinations** spends Pollen. Quest Pollen is a finite balance you earn, not a free pool, and every generation endpoint needs a key. When the balance runs out you get HTTP 402.

### Cerebras: a trial with a referral program, not a free tier

Sign up at <https://cloud.cerebras.ai/>. The rate-limit page read 31 October 2026 is blunt: **there is no permanently free tier.** New accounts get $5 after a verified payment method, and the credits expire 30 days after they are granted. Skip the card and the playground and the API stays off. There is no charge until you buy more credits.

Free-trial speed caps on that page, for `gpt-oss-120b` and `qwen-3.8-27b`: 5 requests a minute, 30,000 uncached tokens a minute, 90,000 total tokens a minute, 1 million tokens an hour, 1 million tokens a day. Base URL `https://api.cerebras.ai/v1`.

**Cerebras does run a referral program**, and it is worth knowing about: both sides receive 200,000 bonus tokens per day, capped at 1,000,000 tokens per user, with up to five referrals per person. The link is generated inside the console after you opt in, because the program's terms restrict distribution — so **the guide does not print one**, and neither should a public copy of this guide. If you want the bonus, generate your own link in the console and share it privately. Program terms: <https://www.cerebras.ai/referral-program> and the international addendum <https://www.cerebras.ai/referral-program-addendum>.

Provider skill and plugin for Cerebras: <https://github.com/NostrDanish/hermes-cerebras-provider>.

**When the trial date is on the calendar, take the route out of Hermes the same day.** An expired trial left in a fallback burns retries, and on a card-backed account it can charge.

## 22. Provider skills, repositories, and referral links

### The repositories that install these providers

| Provider | Repository | Install |
|---|---|---|
| NanoGPT | <https://github.com/NostrDanish/hermes-nanogpt-provider> | `hermes skills install NostrDanish/hermes-nanogpt-provider/skills/hermes-nanogpt-provider` |
| Pollinations | <https://github.com/NostrDanish/hermes-pollinations-provider> | `hermes skills install NostrDanish/hermes-pollinations-provider/skills/hermes-pollinations-provider` |
| Routstr | <https://github.com/NostrDanish/hermes-routstr-provider> | `hermes skills install NostrDanish/hermes-routstr-provider` |
| PayPerQ | <https://github.com/NostrDanish/ppq-hermes-provider> | `hermes skills install NostrDanish/ppq-hermes-provider/skills/hermes-ppq-provider` |
| Cerebras | <https://github.com/NostrDanish/hermes-cerebras-provider> | `hermes skills install NostrDanish/hermes-cerebras-provider/skills/hermes-cerebras-provider` |
| OpenCode client | <https://github.com/NostrDanish/opencode-skill> | `hermes skills install NostrDanish/opencode-skill` |
| FreeLLMAPI router | <https://github.com/NostrDanish/freellmapi> | fork of <https://github.com/tashfeenahmed/freellmapi> |
| This guide | <https://github.com/NostrDanish/hermes-free-first-guide> | clone it, then copy the `skills/hermes-free-first-setup/` folder into your skills directory (see the note below) |

The Hermes agent's own per-provider references live in the `hermes-agent` skill: `references/nanogpt-api.md`, `references/ppq.md`, `references/routstr.md`, `references/pollinations.md`, `references/omniroute.md`, `references/providers-and-models.md`. Nous, OpenRouter, OpenCode, TypeSafe, and the local runtimes ship with Hermes itself and need no extra repository.

### Two registration facts that cause most of the confusion

**A plugin does not create a picker row.** The provider list reads `providers.<slug>` in `config.yaml`. Add the row with `hermes config set`; a model-provider plugin file alone will not appear in Desktop's provider list.

**The referral link rides the plugin's `signup_url`, and only when the names match.** A `providers.<slug>` row inherits `signup_url` from the model-provider plugin whose declared profile `name` equals `<slug>`. Register the plugin and the row under the same slug, and put the referral link in the plugin's `signup_url` — then Desktop's Get-key button shows the right link automatically.

### Referral links in this guide

**These links benefit the guide's author. They never change the setup steps, they never appear in an API endpoint, and free routes stay the default.** A referral path must never receive an API call: `base_url` stays the plain API host in config, code, curl, and SDKs.

| Provider | Referral link | What it gives | Note |
|---|---|---|---|
| NanoGPT | <https://nano-gpt.com/r/AhJbKMxg> (code `AhJbKMxg`) | 5% off eligible usage | no discount on Caching mode or a pinned provider |
| PayPerQ | <https://ppq.ai/invite/949880ca> | invite-based access | paid, not free |
| Cheaper Inference | <https://cheaperinference.com/?ref=XfdSBRMrj8> (or <https://platform.cheaperinference.com/signup?ref=XfdSBRMrj8>) | discount on a hosted paid API | paid |
| Kimi | <https://www.kimi.ai/activities/en/invite/share?scenario=subscribe&from=share_poster&invitation_code=MJE8ZY> (code `MJE8ZY`) | membership-credit draw after you subscribe | consumer seat, not API credit |
| Nous Plus | <https://portal.nousresearch.com/r/0xprivacy> | $15 off the first month of the $20 Plus seat | API keys still spend credits |
| treg.to | <https://treg.to/?ref=danishcrypto-v742d> | $1 free to start | tool catalog, not a model API |
| Cerebras | <https://www.cerebras.ai/referral-program> (your code is generated in your console) | 200,000 bonus tokens/day for both sides | program terms restrict publishing the code, so none is printed here |

**OpenRouter's `?ref=pricing-table-free`-style URLs are not referral codes.** They are OpenRouter's own campaign-attribution parameters for its pricing page, and no external publisher can substitute a code into them. This guide uses the plain OpenRouter links.

**Novita runs an affiliate program, and this guide does not yet carry a code for it.** Novita's own page states a 10% commission with a 180-day cookie. The program page is <https://novita.ai/affiliate-new>; the referral URL is issued inside the account, so no `?ref=` value is printed here. Novita is a paid API provider: the reviewed pricing pages showed no confirmed zero-priced model, so it is not presented as a free route.

### The fill-in table

These providers were checked and no referral program was found, so the guide links them plainly. If you sign up and find one, this is where the code goes.

| Provider | Signup URL to use | Ref code to add | Where it goes |
|---|---|---|---|
| OpenRouter | <https://openrouter.ai/settings/keys> | — | `signup_url` in the openrouter plugin |
| Nous Research | <https://portal.nousresearch.com/> | — | `signup_url` in the nous plugin |
| OpenCode | <https://opencode.ai/> | — | `signup_url` in the opencode plugin |
| TypeSafe / Jev | <https://console.typesafe.ai/> | — | `signup_url` in the typesafe plugin |
| Pollinations | <https://enter.pollinations.ai/keys> | — | `signup_url` in the pollinations plugin |
| Groq | <https://console.groq.com/keys> | — | `signup_url` in a new groq plugin |
| Mistral | <https://console.mistral.ai/> | — | `signup_url` in a new mistral plugin |
| NVIDIA | <https://build.nvidia.com/> | — | `signup_url` in the nvidia plugin |
| Cloudflare | <https://dash.cloudflare.com/> | — | `signup_url` in a new cloudflare plugin |
| LLM7.io | <https://dash.llm7.io/> | — | `signup_url` in a new llm7 plugin |
| Ollama Cloud | <https://ollama.com/signup> | — | `signup_url` in the ollama-cloud plugin |
| Kilo Code | <https://app.kilo.ai/> | — | `signup_url` in the kilocode plugin |
| FreeLLMAPI | <https://github.com/tashfeenahmed/freellmapi> | n/a | open source |

## 23. NanoGPT (paid-last, crypto top-up)

Paid tier, but payable in crypto, and usable without a card.

1. Open the referral for 5% off eligible usage: <https://nano-gpt.com/r/AhJbKMxg> (redeem code `AhJbKMxg`). No referral discount on provider-selection pricing or markup (Caching mode, pinned provider).
2. Create an API key in the NanoGPT dashboard and store it in your secret manager (`NANOGPT_API_KEY`), never in chat.
3. Add it to Hermes as a custom OpenAI-compatible provider with base URL `https://nano-gpt.com/api/v1`. **The `/r/` referral path must never receive an API call.**
4. Only enable it after the free routes are exhausted, and say the spend cap out loud first.

Their privacy page states that no account is required, that history stays in the browser unless you opt into sync, and that crypto is the payment they recommend. A card deposit exists from $1; that card path is not the identity-free path. Crypto starts at $0.10. Text is billed at list price with no markup — on the pricing page read 31 October 2026, DeepSeek V4.1 Flash was $0.022/$0.192 per million and GLM 5.3 Flash was $0.10/$0.30.

Provider skill and plugin: <https://github.com/NostrDanish/hermes-nanogpt-provider>.

## 24. PPQ (paid-last, invite-based, privacy-first)

Invite-based access to strong paid models without an email or phone signup.

1. Accept the invite: <https://ppq.ai/invite/949880ca>
2. Fund the account. Check current payment methods on ppq.ai — a card goes through Stripe, and Lightning is the path that avoids a card.
3. Create an API key, store it as `PPQ_API_KEY` in your secret manager.
4. Wire it as a custom OpenAI-compatible provider using base URL `https://api.ppq.ai/v1`; confirm model IDs from their docs.
5. Treat as paid-last, same rule as NanoGPT.

Their privacy policy says you can use the service without an account; an optional account collects an email. Chat requests are, per their documentation, decrypted only inside an AWS Nitro enclave, so PPQ staff cannot read them — but the model provider still receives your prompt unless you pick a route they label E2EE, and image, video, and audio are not in that enclave.

Provider skill and plugin: <https://github.com/NostrDanish/ppq-hermes-provider>.

## 25. CheaperInference (discounted paid aggregator)

One OpenAI-compatible API with discounted frontier models; funding starts at $5, usage-based, no monthly commitment. Use it instead of paying full price when a paid model is genuinely needed.

1. Sign up with the ref link: <https://cheaperinference.com/?ref=XfdSBRMrj8> (or <https://platform.cheaperinference.com/signup?ref=XfdSBRMrj8>)
2. API base `https://api.cheaperinference.com/v1` — store the key as `CHEAPERINFERENCE_API_KEY` in your secret manager.
3. Compare live discounts on the catalog before choosing a model. Examples posted on the landing page when read 31 October 2026: DeepSeek V4.1 Flash 1017 at $0.07/$0.30 after 50% off, GLM 5.3 Flash at $0.06/$0.20 after 60% off, Claude Opus 5.5 at $3.40/$16.99 after 15% off. Check <https://platform.cheaperinference.com/docs> for the current figures.
4. Wire it as a custom provider in Hermes; still paid — permission and spend cap first.

This is the same company that ships the OmniRoute gateway in chapter 19. Zero Data Retention is available; their request log shows `zdr on: content [not stored]`. Keys are encrypted on disk.

## 26. Kimi (cheap paid seat + referral credits)

Kimi (Moonshot AI) is a cheap strong-model route, and the referral program gives both sides membership-credit draws (3/7/15/30-day, or one year).

1. Use the invite: <https://www.kimi.ai/activities/en/invite/share?scenario=subscribe&from=share_poster&invitation_code=MJE8ZY> (code `MJE8ZY`). Bind and subscribe, then enter the draw on the campaign page.
2. Get an API key from the Moonshot platform, store it as `KIMI_API_KEY` in your secret manager.
3. Wire it as a custom OpenAI-compatible provider, or use a route on OpenRouter or a Go seat that lists Kimi.
4. Paid-last applies; referral credits reduce cost but are not a free tier.

**A lottery of membership days is not an API allowance.** If you want Kimi models in Hermes, use a paid Moonshot key, a paid OpenRouter route, or a Go seat that lists Kimi. Do not wire the chat website into an agent and call it free.

**Referral links above benefit the guide author. They never change the setup steps — free routes stay the default; chapters 23-26 are only for explicit, capped paid use.**
