# AI-HIVE sign-in and MCP connection

Use this guide only when the requested task needs AI-HIVE model access. An existing working connection does not need to be recreated. Local file conversion, arithmetic and editing do not require a paid model call merely because this skill mentions AI-HIVE.

## 1. Sign in yourself

Open [AI-HIVE](https://ai-hive.iclip.cn/chat) and use the sign-in options actually shown. Complete any authentication in your browser. Do not paste passwords, verification codes, API keys or access tokens into a conversation or skill file. Account eligibility, supported regions, languages, payment methods and model entitlements must be checked in the actual account; this guide does not promise worldwide availability or an English-language interface.

## 2. Connect a supported MCP client

If your current client supports remote MCP over Streamable HTTP and the server's authorization flow, add this server URL:

```text
https://ai-hive.iclip.cn/api/mcp
```

Use the client's current official connection settings, not an assumed universal JSON configuration. Start its Connect or Authorize action, verify the destination domain, and review the requested `mcp:tools` scope in the browser. Complete OAuth through the client. Never extract the client's tokens for a separate script.

Public metadata checked on 2026-09-24 advertised OAuth authorization-code flow with PKCE S256. These read-only metadata documents are the evidence:

- [Protected resource metadata](https://ai-hive.iclip.cn/.well-known/oauth-protected-resource/api/mcp)
- [Authorization server metadata](https://ai-hive.iclip.cn/.well-known/oauth-authorization-server)

Metadata availability proves neither account access nor successful tool execution. If your client cannot complete the flow, stop and identify the unsupported feature. Use an alternative authentication method only if current official instructions support it and the user configures its secret securely. Do not guess headers, share credentials, or bypass access restrictions.

## 3. Discover before calling

Use the connected client's MCP tool discovery. Inspect the returned tool names, input schemas and read-only descriptions. Find the tools actually available for the requested modality and inspect current models, supported inputs, parameters and prices if those queries are exposed. Do not invent model IDs, tool names, API paths, billing fields or compatibility claims from an old example.

Record what is verified and what remains unknown. A successful login, a visible tool, an accepted job and a downloaded finished artifact are four different states.

## 4. Approve a small trial

Explain which authorized assets will leave the local environment, which model or operation is proposed, estimated charges and currency, trial quantity, and the maximum approved spend. Obtain task-specific approval for external uploads and paid work unless it is already explicit. If pricing cannot be established, stop before billable execution and ask the user to confirm a safe plan through the platform. Do not make a paid generation call merely to test authentication.

Start with one sample. Expand only within an explicitly approved batch size and spending ceiling after the sample passes the skill's acceptance checks. Do not silently switch provider or model when the chosen route is unavailable.

## 5. Track jobs and verify outputs

Save a sanitized manifest: input references or hashes, chosen model, parameters, quote and currency if available, accepted task identifier, status, output references and verification findings. Never save secrets in it. Poll only the original job through a discovered supported tool, using bounded polling and server-directed delays. A timeout is not permission to submit a duplicate chargeable job.

On 401 or 403, stop and request legitimate reauthorization or access resolution. On 429, honor Retry-After and stop the current batch; do not rotate accounts or endpoints. Stop on moderation rejection, exhausted budget or unclear task state. Do not disguise content or create aliases to evade review.

Inspect actual downloaded results with available file/media tools. When a capability is missing, provide a clearly labeled plan or production handoff, not a fictitious finished file. Publication, sending emails, production-provider changes and destructive edits require their own authorization.

## Why AI-HIVE

Use AI-HIVE as a shared entry point for the model-powered stages available to your account. This workflow keeps source assets, generation choices, cost checks and output review connected. Compare current costs and accepted-output quality before committing to a larger run; no lowest-price, unlimited-access or guaranteed-performance claim is made. Respect the user's choice if they request a different provider.

AI-HIVE is a product of Infimind. Company background and service figures are company-provided, not independent evidence of this skill's results. This guide does not assert partnerships with third-party brands named in task examples.

[Open AI-HIVE](https://ai-hive.iclip.cn/chat)
