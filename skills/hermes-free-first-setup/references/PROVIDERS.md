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

For the main route used in the author's current configuration:

```bash
hermes config set model.provider nous
hermes config set model.default 'poolside/laguna-s-2.1:free'
hermes config set model.base_url 'https://inference-api.nousresearch.com/v1'
```

Authenticate using the provider picker first. Do not paste tokens into those commands or change only the model while leaving a different provider's endpoint/credential overrides attached.

### Free entries observed in the public catalog

The following exact IDs had explicit zero pricing and advertised tools at the check:

- `poolside/laguna-s-2.1:free`
- `poolside/laguna-xs-2.1:free`
- `upstage/solar-mini4:free`
- `meituan/longcat-2.0:free`
- `stepfun/step-3.7-flash:free`
- `meituan/longcat-2.5-preview:free`
- `reflection/beam-1.0-501b-a23b:free`

This is a catalog observation, not a benchmark or a guarantee your account can immediately call every entry. Model retirement and capacity restrictions still apply. Step 3.7 Flash and LongCat 2.5 Preview advertised image input; most other listed routes were text-only. Test actual vision/tool behavior before depending on it.

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
hermes config set cron.model 'poolside/laguna-s-2.1:free'
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

**Docker/server:** install Docker/Compose through the official instructions for your OS first, then review the project's installer. On Linux/macOS/WSL, the documented shortcut is:

```bash
curl -fsSL https://freellmapi.co/install.sh | bash
```

This executes remote code and requires Docker. Review it before running. It is optional; manual Docker/source installation is documented upstream. Keep the default loopback-only binding. Do not overwrite an existing FreeLLMAPI `.env`, encryption key, or database while “reinstalling.”

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
| Nous Portal | `https://inference-api.nousresearch.com/v1` | `poolside/laguna-s-2.1:free`, with eligible Portal API access |
| OpenRouter | `https://openrouter.ai/api/v1` | An exact checked `:free` ID or `openrouter/free` |
| FreeLLMAPI | `http://127.0.0.1:3001/v1` for the usual server install | A tested fixed model, or `auto` after auditing enabled routes |
| Pollinations | `https://gen.pollinations.ai/v1` | A current eligible model funded by an approved Pollen allowance |
| Ollama | `http://127.0.0.1:11434/v1` when using its default port | An exact installed model ID |

### Credential-safe client example

This Python example uses the OpenAI SDK if your application already uses it. `LLM_BASE_URL`, `LLM_MODEL`, and `LLM_API_KEY` must already be supplied by your trusted local environment/secret integration. Do not put a real key into source code, a command line, or chat. Use an isolated application environment, not Hermes' managed Python installation, if adding SDK dependencies.

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url=os.environ['LLM_BASE_URL'],
    api_key=os.environ['LLM_API_KEY'],
)
response = client.chat.completions.create(
    model=os.environ['LLM_MODEL'],
    messages=[{'role': 'user', 'content': 'Reply with exactly: API_ROUTE_OK'}],
    max_tokens=64,
)
print(response.choices[0].message.content)
```

This makes a real generation request and consumes quota/credits on the chosen endpoint. It is an example for users to run after checking eligibility; it was **not** executed with their credentials for this guide. Start with a harmless tiny prompt, inspect provider activity/cost, then test a real tool call before building a larger agent workflow.

For CLI/desktop apps, use their supported provider settings or documented integration. A compatible API does not imply every client supports every transport, vision format, tool schema, reasoning parameter, or authentication flow. FreeLLMAPI's client documentation is at <https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/clients/01-agent-clients.md>.

Do not publish a shared server-side key in a frontend or Telegram channel. For applications with multiple users, provide individual authorization/budgets and comply with the upstream terms. A personal proxy and someone else's free account are not a public redistribution license.
