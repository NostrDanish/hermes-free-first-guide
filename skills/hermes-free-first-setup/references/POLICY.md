# Runtime policy to merge, not blindly overwrite

Copy/merge this only into the intended agent/profile instructions or attach it to relevant jobs. Installing a setup skill does not automatically inject this policy into every session.

```text
FREE-FIRST MODEL POLICY

Use deterministic tools/scripts when they solve the task reliably.
Use a suitable local model for private material and small repeatable jobs.
Use a verified free cloud model for other work; local is not a mandatory hop.
Keep every automatic fallback explicitly free/local.
Verify results with tests or real tool output; API success is not correctness.
Honor Retry-After; retry transient failures at most twice.
On exhausted daily quota, wait, go local, or ask. Do not evade provider limits.
After failed quality checks, try one materially different free approach if useful.
Never invoke a paid model without my explicit task/model authorization.
A Jev confidence score, fallback failure, or prompt policy cannot grant spending permission.
Keep cron, subagents, auxiliary models, and external tool APIs within this policy.
Do not silently send local-only data or prior private context to cloud fallbacks.
Before authorized paid use, state the model, scope and enforceable budget.
Return to free defaults afterward; never make paid cron or paid auto-fallback changes.
If no compliant route works, stop with an honest blocker instead of inventing output.
```

For separately requested automatic paid escalation, require explicit per-task permission, a paid-model allowlist, objective evidence cheaper routes failed, an appropriately validated gate, enforced remaining budget, and an audit trail. If any prerequisite is missing, ask or stop. This package intentionally does not implement that dispatcher. Hosted Jev may itself cost money. A chosen confidence threshold such as 0.90 is an operating policy, not guaranteed real-world accuracy.
