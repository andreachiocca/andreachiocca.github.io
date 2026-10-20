# Permanent pull-request website previews

The production website remains on GitHub Pages. The separate Cloudflare Pages
project `academic-website-preview` hosts review builds from pull requests.

## One-time setup

1. Create a free Cloudflare account and a **Pages** project named
   `academic-website-preview` (Direct Upload, not connected to Git).
2. Create a Cloudflare API token with **Account / Cloudflare Pages / Edit**
   permission scoped to your account.
3. In GitHub repository Settings > Environments, create `website-preview`.
4. Add environment secrets `CLOUDFLARE_API_TOKEN` and
   `CLOUDFLARE_ACCOUNT_ID`.
5. Re-run **Preview website on Cloudflare Pages** for PR #27 (or push a new
   commit to its branch).

For PR #27 the expected branch alias is:
`https://pr-27.academic-website-preview.pages.dev/`

Each PR number receives a stable alias, updated when the PR branch changes.
This is not a production deployment. Do not merge a PR merely to preview it.

## Notes

The preview build uses `_config_preview.yml` to disable production analytics
and verification metadata. Cloudflare must be configured before the workflow
can deploy. Keep the preview URL out of public navigation. Preview deployments
are publicly accessible unless Cloudflare Access is configured.

The current canonical URL configuration is set to the project's default
`pages.dev` domain; metadata may point to the project's default domain rather
than its PR-specific alias. Before promoting this as a production-quality
preview workflow, validate generated absolute links, robots policy, and
assets on the PR alias. The production site is unaffected.
