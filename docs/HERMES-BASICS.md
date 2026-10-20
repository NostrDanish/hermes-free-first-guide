## 0. What Hermes is, what you need, and what to set up first

**Hermes Agent is the application. Nous Portal, OpenRouter, and other services are model/API providers. FreeLLMAPI is an optional router in front of providers. Ollama/llama.cpp are local inference engines.** These are separate layers; installing one does not automatically create accounts or free allowances at the others.

```text
YOU → Hermes Agent → Nous free model
                  → OpenRouter free model
                  → FreeLLMAPI → enabled/eligible upstream provider
                  → local model
                  → explicitly authorized paid model (optional)

OTHER APPS/SCRIPTS → the same supported APIs with their own approved credentials
```

### What Hermes can do

With a suitable tool-capable model and approved tools, Hermes can read/write files, run commands, research the web, work with repositories, keep reusable skills and memory, delegate work, schedule jobs, and connect to messaging platforms. It also offers optional browser, voice, vision, and media tools.

**Free software does not mean every tool backend is free.** A free text model can still call a paid search, image, browser, memory, transcription, or cloud-compute service if you configure one. Review those separately.

### Minimum practical setup

1. Install Hermes from its official distribution.
2. Connect **one** real free route—Nous Portal Free or a verified OpenRouter free model.
3. Verify a harmless real tool call.
4. Set free-only automatic fallbacks and pin background/auxiliary work.
5. Add FreeLLMAPI and more legitimate allowances only when you need them.
6. Add local inference if you want offline/private model work or a separate quota-independent backup.

**The provider chapters are alternative/optional connection paths, not a sequence of commands to run blindly.** Choose the primary route you actually want (Nous, OpenRouter, an audited gateway, or local); provider-specific examples later in the book should be adapted to that choice. You do not need accounts at every provider, a GPU, Docker, a swarm, a paid subscription, or every plugin just to begin. Each additional service adds limits, data policies, failure modes, and maintenance.

### What the author's installation actually contains

The redacted inventory found Nous as the main provider, explicit OpenRouter free fallbacks, an active FreeLLMAPI service, Pollinations/NanoGPT/Cheaper Inference custom-provider families, and a reachable local Ollama instance. Several aliases point at the same provider family; they are not separate sources of free capacity.

The full inventory and evidence limits are in `docs/PROVIDER-STATUS.md` in the repository. This guide includes those families and useful additional FreeLLMAPI upstreams. It does not claim every registered adapter has a valid key, remaining allowance, or tested completion.

**Two important findings:** current NanoGPT pricing puts its free model on the web only; current Hugging Face hosted Inference Providers gives free accounts no included monthly credits. Do not put either API into a strict-free chain based only on an old list.

### Keep a simple provider worksheet

For each route, record only non-secret facts:

| Field | Example |
|---|---|
| Provider and protocol | Nous Portal / OpenAI-compatible chat completions |
| Base URL | Its official endpoint, not a copied guess |
| Model ID | Exact verified free entry |
| Access type | Zero-price model, recurring allowance, trial, earned credits, subscription, or paid |
| Limits/reset | Current account-specific ceilings and reset time |
| Data policy | Whether this workload may leave the machine and how data can be used |
| Verification | Catalog only, authenticated completion, tool call, or failure test |

Never record API-key values in a shared worksheet, screenshot, repo, or guide.

### Learn these Hermes controls first

```bash
hermes                 # Start the terminal interface
hermes desktop         # Start the desktop interface when installed/supported
hermes model           # Choose/authenticate a model provider
hermes tools           # Inspect and choose tool backends
hermes skills list     # Inspect installed reusable workflows
hermes profile list    # Inspect available profiles
hermes cron list       # Inspect scheduled jobs and pins
hermes config check    # Check configuration issues
hermes doctor          # Diagnose installation/runtime issues
```

Inside a chat, `/model` opens model selection; named aliases can provide shortcuts. A new default does not necessarily replace the model in an already-open conversation. Read the model/provider display rather than assuming a change applied everywhere.

CLI documentation: <https://hermes-agent.nousresearch.com/docs/user-guide/cli>.

### Work safely on real files

Start in an empty test directory or disposable repository. Ask for a read-only task first, then a tiny edit, then verify the file yourself through real tool output. Keep command approvals enabled; a less capable free model should not receive broader permissions to compensate for weak reasoning. Use version control/backups before allowing important edits or destructive operations.

Security guide: <https://hermes-agent.nousresearch.com/docs/user-guide/security>.

### Skills, memory, and project instructions

- **Skills** package reusable procedures and scripts. Load only relevant ones; a giant pile of unrelated instructions increases prompt size and can hurt smaller models.
- **Memory** stores ongoing facts/preferences; do not use it as a secret manager.
- **Project instructions** such as `AGENTS.md`/`.hermes.md` apply within their documented scope. Merge the free-first policy into existing instructions instead of overwriting them.
- **Profiles** separate settings/workflows, but are not a hard OS security sandbox. Some authentication can be shared across profiles; review the actual secret/provider behavior before claiming strong separation.

References: <https://hermes-agent.nousresearch.com/docs/user-guide/features/skills>, <https://hermes-agent.nousresearch.com/docs/user-guide/features/memory>, <https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files>, and <https://hermes-agent.nousresearch.com/docs/user-guide/profiles>.

### Web, browser, speech, and media without accidental bills

Use a local browser/backend when it fits. Where available, a local/self-hosted search backend, local speech recognition, or local speech synthesis can avoid a hosted API bill. They still have installation/runtime costs and network behavior to review. Do not assume an account at Nous, Pollinations, or another aggregator grants every media tool for free.

Inspect `hermes tools` and provider terms before enabling a backend. For example, “free speech output” from an online service is not offline/private speech. Prefer an actual local backend when the data must remain local.

Tool guide: <https://hermes-agent.nousresearch.com/docs/user-guide/features/tools>. Browser guide: <https://hermes-agent.nousresearch.com/docs/user-guide/features/browser>. Web-search guide: <https://hermes-agent.nousresearch.com/docs/user-guide/features/web-search>.

### Telegram and other messaging platforms

Get ordinary local chat working first. Then follow the official Telegram guide: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram>.

Create your own bot through BotFather, enter its token only in the trusted local gateway setup, configure the allowed-user/chat controls, and test the bot from the intended account. Keep the gateway running for messaging and agent-backed scheduled work. Do not publish bot tokens or grant unknown people access to a machine-controlling agent.

Other messaging options: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging>. Remote OAuth/browser callbacks can need SSH forwarding or the documented remote-login flow; do not expose login callbacks casually to the internet.

### Two setup routes in this repository

**Human-led:** follow this handbook's account/setup chapters, then validate the routes and spending policy.

**AI-assisted:** give the portable `hermes-free-first-setup` skill to an agent. It must inventory providers, distinguish free/allowance/trial/paid access, guide secure account connection, and obtain approval before changes. The supplied script configures publicly verifiable Nous or OpenRouter free defaults; it does not automatically create accounts, read keys, install every provider, or prove a custom FreeLLMAPI chain is free.

Do not let an AI force everything onto OpenRouter if you chose Nous or already have a working gateway. Prefer the verified route you actually want, and configure other routes alongside it rather than silently replacing it.
