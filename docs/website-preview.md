# Permanent academic website previews

This site publishes production via GitHub Pages at
`https://andreachiocca.github.io/`. Cloudflare Pages is used for isolated
review deployments. Never merge a design PR merely to inspect its layout.

## Infrastructure and permissions

- Cloudflare Pages project: `academic-website-preview` (Direct Upload).
- GitHub environment: `website-preview-AC`.
- Environment secrets (names only): `CLOUDFLARE_API_TOKEN` and
  `CLOUDFLARE_ACCOUNT_ID`.
- Token scope: Cloudflare account / Pages / Edit on the owning account.
- GitHub Actions permissions: `contents: read`, `pull-requests: read`.
- Fork PRs do not receive the deployment environment.
- Preview builds always resolve the open PR via GitHub API and check out its
  exact head commit, **not** the default branch or synthetic merge commit.
- The workflow cannot deploy a closed PR or a PR from a fork.

## Initial enablement

1. Review and merge infrastructure PR #28 when its checks pass. Do **not**
   merge design PR #27.
2. In GitHub > Actions > **Preview website on Cloudflare Pages**, click
   **Run workflow**.
3. Select `master` as the workflow branch and enter `27` in the
   **Number of the open PR to preview** field.
4. Run the workflow. It fetches PR #27's current head SHA and checks out
   `design/technical-editorial-phase-1`; it never builds `master` as its
   site source.
5. Inspect the deployment log and then:
   `https://pr-27.academic-website-preview.pages.dev/`
   `https://pr-27.academic-website-preview.pages.dev/it/`
6. Future same-repository PR updates also trigger previews automatically.

The `academic-website-preview.pages.dev` root is a separate Cloudflare
production deployment and is *not* the design preview alias. Check the `pr-27`
subdomain for the design review.

## Indexing and metadata

The GitHub workflow builds with `_config_preview.yml` plus a dynamically
created URL override for the PR-specific alias. Production analytics and Google
site verification are disabled. Preview HTML emits
`<meta name="robots" content="noindex, nofollow, noarchive">`. The build also
creates `_site/_headers` with `X-Robots-Tag: noindex, nofollow, noarchive`
for Cloudflare Pages static assets. Preview `robots.txt` leaves crawling
allowed so compliant search engines can see the `noindex` directives.
These controls reduce discoverability, but the preview remains publicly
accessible by URL; use Cloudflare Access if restricted access is needed.

The standard English and Italian verification scripts use `SITE_ORIGIN` for
preview builds, and preserve their original production behavior when unset.
`scripts/verify_preview.py` additionally checks the PR-specific canonical
URLs, CSS, noindex controls and eight primary English/Italian routes.

## Troubleshooting

- Missing secrets: check names under GitHub > Settings > Environments >
  `website-preview-AC`. The secret values are never printed.
- Cloudflare 403/404: confirm the token's Pages Edit permission and project
  name; check which Cloudflare account owns the Pages project.
- GitHub build failure: inspect the first failing step before deployment.
- Missing PR alias: ensure the deploy step succeeded and Cloudflare generated
  the `pr-N` branch deployment. Avoid assuming the URL exists before deployment.
- An unrelated `Workers Builds: andreachiocca-github-io` status came from a
  separate Cloudflare Workers Git integration, not this Direct Upload Pages
  project. If its automatic Git builds were disconnected, push a new PR commit
  to check whether the obsolete status no longer appears; do not disconnect
  the `academic-website-preview` Pages project.
