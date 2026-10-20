# Provider access: verified scope and free-use classification

Checked 20 October 2026. This is a redacted inventory of provider families/configuration and publicly documented access terms—not a dump of credentials or a claim that every account has remaining quota.

| Provider family | Evidence on the author's setup | Free-use classification | What is NOT established |
|---|---|---|---|
| Nous Portal | Current main route is `nous` / `poolside/laguna-s-2.1:free`; public catalog exposes explicit zero-priced routes | Genuine Free plan for free models; paid models/tools are separate | Fresh-account API-key issuance and an authenticated completion were not retested |
| OpenRouter | Explicit free-model fallback entries configured; public catalog checked | Genuine zero-priced model routes, subject to account quotas | Account quota and authenticated availability were not retested |
| FreeLLMAPI | Self-hosted service running; protected `/v1/models` returns 401 without a key; source matches official v0.16.5-era commit `5540efa` | Free self-hosted router; upstream free allowances must be verified individually; optional live catalog is paid | No unified key or database credentials were read; connected-upstream readiness and authenticated routing were not tested |
| Pollinations | Custom provider endpoint configured | Earned/awarded Quest Pollen can fund real API use; finite credits, not unlimited zero-price inference | Current Pollen balance and model eligibility were not read |
| NanoGPT | Several configured aliases/credential slots resolve to the same provider family | Paid PAYG or subscription-included API use; current pricing lists a free model on the web only | Multiple aliases do not prove multiple free API quotas or independent providers |
| Cheaper Inference | Custom OpenAI-compatible provider configured | Discounted paid usage; current public page requires funding from $5 | No recurring free API entitlement was established |
| Ollama/local models | Local Ollama model catalog reachable; customized Qwen coder tag present | Local inference: no hosted model API bill | This does not make cloud tools free, nor validate every local tool-calling workflow |

The project may also have built-in/provider-plugin choices for other services. Installed adapters are not the same as connected keys, available quota, or a free plan. The guide separately explains useful FreeLLMAPI upstreams (Groq, Gemini, Mistral, Cerebras, NVIDIA, Cloudflare, Cohere, and Hugging Face) without claiming all are enabled here.

## Important findings

- Nous' official plan page lists **Free: $0, free models only, $0 monthly credits**. Paid hosted-tool access must not be inferred from a free text model.
- Nous' public catalog listed seven zero-priced, tool-advertising `:free` entries at this check. Configured historical fallback names can disappear; a configured `stepfun/step-5-preview:free` route was not in the current public free catalog and is not recommended as a fresh setup default.
- FreeLLMAPI's own latest README separates its free monthly-snapshot catalog from an optional paid live feed. Its aggregate token headline is not an entitlement or measured capacity for this installation.
- Current NanoGPT pricing says its free model is **web only**. Its API subscription allowance is paid-plan usage, not a generally free API.
- Current Hugging Face Inference Providers pricing gives free accounts **no included monthly credits**. Older free-provider lists can be stale.
- NVIDIA's FAQ describes hosted API prototyping credits as trial credits. Do not present them as a permanent unlimited free allowance.

## Primary sources

- https://portal.nousresearch.com/manage-subscription
- https://portal.nousresearch.com/api-docs
- https://inference-api.nousresearch.com/v1/models
- https://openrouter.ai/api/v1/models
- https://github.com/tashfeenahmed/freellmapi
- https://nano-gpt.com/pricing
- https://pollinations.ai/
- https://gen.pollinations.ai/docs
- https://cheaperinference.com/
- https://huggingface.co/docs/inference-providers/pricing
- https://docs.api.nvidia.com/nim/docs/faq
